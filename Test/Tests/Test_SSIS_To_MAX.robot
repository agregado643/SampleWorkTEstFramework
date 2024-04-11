*** Settings ***
Documentation  Database Testing in Robot Framework
Library    DatabaseLibrary
Library    ../Resource/pysqltest.py
Library    OperatingSystem
Library     String
Library  Process
Resource     ../Resource/FileUtility.robot
Suite setup    Parse PDF Invoice
Resource   ../Resource/MasterKeywords.robot

*** Test Cases ***
Launch Test Template by RobotFramework
    Log    Placeholder test required by Robot Framework

*** Keywords ***

processinvoice
    [Arguments]     @{colvalues}
    ${utclocal}=   getUTCnow
    ${parser}=  Set Variable If
    ...     '@{colvalues}[11]'=='att'   ${ATTPdfReaderConsoleApplicationexe}
    ...     '@{colvalues}[11]'=='verizon'   ${VerizonPdfReaderConsoleApplicationexe}

    ${result} =     Run Process    ${parser}      ${pdfinvoicePATH}\\@{colvalues}[0]
    Run Keyword If  'Pdf processed successfully' in '''${result.stdout}'''  check existing InvoiceNumber    @{colvalues}[1]
    
    move_zipfile_to_ssis    @{colvalues}[11]
    callsqlserveragentjob   @{colvalues}[11]

    Verify InvoiceProcessing job is succeeded   @{colvalues}[11]    ${utclocal}       

    # VerifyInvoiceSummaryData    @{colvalues}

    # VerifyTotalLinesInMax     @{colvalues}[1]     @{colvalues}[12]

    # ${contents}   Get File    ${csvfilepath}\\InvoiceLineTestData.csv
    # @{lines}=   Split String  ${contents}  \n
    # :FOR    ${row}     IN      @{lines}
    # \   @{lineresult}=    Split String    ${row}    ,
    # \   Run Keyword IF  '@{lineresult}[0]' == '@{colvalues}[1]'   VerifyLineData   @{lineresult}


VerifyTotalLinesInMax
    [Arguments]     ${InvoiceNumber}    ${expectedtotalcount}     
    ${queryrec}=     getinvoicesummary_data   ${InvoiceNumber}
    ${jsonobj}=     Evaluate    json.loads('''${queryrec}''')     json
    ${invoiceid}=    Set Variable    ${jsonobj[0]['InvoiceId']}
    ${queryrec2}=    getinvoicesline_count     ${InvoiceId}
    ${jsonobj2}=     Evaluate    json.loads('''${queryrec2}''')     json
    Run Keyword And Continue On Failure     Should Be Equal     ${jsonobj2[0]['totalcount']}  ${expectedtotalcount}

VerifyInvoiceSummaryData
    [Arguments]     @{colvalues}
    ${queryrec}=     getinvoicesummary_data   @{colvalues}[1]
    ${jsonobj}=     Evaluate    json.loads('''${queryrec}''')     json
    Run Keyword And Continue On Failure     Should Be Equal     ${jsonobj[0]['AccountNumber']}  @{colvalues}[2]
    Run Keyword And Continue On Failure     Should Be Equal     ${jsonobj[0]['PeriodStartDate']}  @{colvalues}[3]
    Run Keyword And Continue On Failure     Should Be Equal     ${jsonobj[0]['PeriodEndDate']}  @{colvalues}[4]
    Run Keyword And Continue On Failure     Should Be Equal     ${jsonobj[0]['BillDate']}  @{colvalues}[5]
    Run Keyword And Continue On Failure     Should Be Equal     ${jsonobj[0]['DueDate']}  @{colvalues}[6]
    Run Keyword And Continue On Failure     Should Be Equal     ${jsonobj[0]['BillPreviousBalance']}  @{colvalues}[7]
    Run Keyword And Continue On Failure     Should Be Equal     ${jsonobj[0]['BillPastDueBalance']}  @{colvalues}[8]
    Run Keyword And Continue On Failure     Should Be Equal     ${jsonobj[0]['BillPaymentReceived']}  @{colvalues}[9]
    Run Keyword And Continue On Failure     Should Be Equal     ${jsonobj[0]['BillBalance']}  @{colvalues}[10]

VerifyLineData
    [Arguments]     @{lineresult}
    ${queryrec}=     getinvoicesline_data   @{lineresult}[0]     @{lineresult}[1]
    ${jsonobj}=     Evaluate    json.loads('''${queryrec}''')     json
    Run Keyword And Continue On Failure     Should Be Equal     ${jsonobj[0]['CapturePrimaryPlanName']}  @{lineresult}[2]
    Run Keyword And Continue On Failure     Should Be Equal     ${jsonobj[0]['TotalCharges']}  @{lineresult}[3]
    Run Keyword And Continue On Failure     Should Be Equal     ${jsonobj[0]['PrimaryPlanMRC']}  @{lineresult}[4]
    Run Keyword And Continue On Failure     Should Be Equal     ${jsonobj[0]['DataUsageMB']}  @{lineresult}[5]
    Run Keyword And Continue On Failure     Should Be Equal     ${jsonobj[0]['TaxesSurchargeCharges']}  @{lineresult}[6]
    Run Keyword And Continue On Failure     Should Be Equal     ${jsonobj[0]['EquipmentCharges']}  @{lineresult}[7]

check existing InvoiceNumber
    [Arguments]     ${invoicenum}
    ${issexist}=    check_if_invoice_exist     ${invoicenum}
    Run Keyword If  ${issexist}==True     clear_invoice     ${invoicenum}

clear_invoice
    [Arguments]     ${invoicenum}
    delete_invoice  ${invoicenum}

Verify Invoice exist
    [Arguments]     ${invoicenum}
    ${issexist}=    check_if_invoice_exist     ${invoicenum}
    Should Be True  ${issexist}

Verify Invoice is reuploaded
    [Arguments]  ${invoicenum}
    ${isexist}=   set variable    False
    : FOR    ${i}    IN RANGE    1    25
        \  ${isexist}=     check_if_invoice_exist    ${invoicenum}
        \  Exit For Loop IF    "${isexist}" == "True"
        \  Sleep   15
    
    Run Keyword If  "${isexist}" == "False"     Fail    Invoice Does Not Exist

Verify InvoiceProcessing job is succeeded
    [Arguments]  ${carrier}     ${utctime}
    ${isjobsucceeded}=   set variable    False
    : FOR    ${i}    IN RANGE    1    25
        \  ${isjobsucceeded}=     check_job_is_done    ${carrier}  ${utctime}
        \  Exit For Loop IF    "${isjobsucceeded}" == "True"
        \  Sleep   15
    
    Run Keyword If  "${isjobsucceeded}" == "False"     Fail    Invoice Processing Job Not Suceeded

verify data in database
    [Arguments]   ${colname}    ${valueexpected}
    ${var}=    getinvoices_data    ${colname}
    Should Be Equal    ${var}   ${valueexpected}