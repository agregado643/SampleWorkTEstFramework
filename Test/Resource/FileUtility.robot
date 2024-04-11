*** Settings ***
Library    ../Core/CommonFunctions.py
Library           Collections
Library           OperatingSystem
Library           String
Library    ../Core/utilitycore.py
Library        ../Core/DynamicTestCases.py
Resource   MasterKeywords.robot

*** Variables ***
${path1}    C:\\new
${path2}    C:\\old

*** Keywords ***
compare outputs
    sortandCompare    ${f1}    ${f2}

Setup one test for each item
    @{dev}=    getMyFiles     D:\\File\\develop
    @{mast}=    getMyFiles    D:\\File\\master   
    ${numItems}=    Get Length    ${dev}    
    :FOR    ${i}    IN RANGE    ${numItems}
    \     Add test case    Item ${i}
    \     ...              checkdiff    @{dev}[${i}]    @{mast}[${i}]

Parse PDF Invoice
    ${contents}   Get File    ${csvfilepath}\\InvoiceSummaryTestData2.csv
    @{lines}=   Split String  ${contents}  \n
    :FOR    ${row}     IN      @{lines}
    \   @{result}=    Split String    ${row}    ,
    \   Run Keyword IF  "@{result}[11]" != "carrier"    Add test case    @{result}[1]
    \   ...              processinvoice  @{result}


Test Invoice Reconciliation
    ${contents}   Get File    ${csvfilepath}\\InvoiceSummaryTestDataForReconciliation.csv
    @{lines}=   Split String  ${contents}  \n
    :FOR    ${row}     IN      @{lines}
    \   @{result}=    Split String    ${row}    ,
    \   Run Keyword IF  "@{result}[11]" != "carrier"    Add test case    @{result}[1]
    \   ...              processinvoice  @{result}

Test From SSIS To Reconciliation
    ${contents}   Get File    ${csvfilepath}\\TestdataReconcilliationDiff7.csv
    @{lines}=   Split String  ${contents}  \n
    :FOR    ${row}     IN      @{lines}
    \   @{result}=    Split String    ${row}    ,
    \   Run Keyword IF  "@{result}[11]" != "carrier"    Add test case    @{result}[1]
    \   ...              processinvoice  @{result}

Test From SSIS To CheckError
    ${contents}   Get File    ${csvfilepath}\\testdataerror1.csv
    @{lines}=   Split String  ${contents}  \n
    :FOR    ${row}     IN      @{lines}
    \   @{result}=    Split String    ${row}    ,
    \   Run Keyword IF  "@{result}[11]" != "carrier"    Add test case    @{result}[1]
    \   ...              processinvoice  @{result}

Test From SSIS To MAX
    ${contents}   Get File    ${csvfilepath}\\TestDataTMobile1Regression.csv
    @{lines}=   Split String  ${contents}  \n
    :FOR    ${row}     IN      @{lines}
    \   @{result}=    Split String    ${row}    ,
    \   Run Keyword IF  "@{result}[11]" != "carrier"    Add test case    @{result}[1]
    \   ...              processinvoice  @{result}

Test From SSIS To Check Result From Erroneous
    ${contents}   Get File    ${csvfilepath}\\testdataerror2.csv
    @{lines}=   Split String  ${contents}  \n
    :FOR    ${row}     IN      @{lines}
    \   @{result}=    Split String    ${row}    ,
    \   Run Keyword IF  "@{result}[11]" != "carrier"    Add test case    @{result}[1]
    \   ...              processinvoice  @{result}

Parse PDF Invoice Only
    ${contents}   Get File    ${csvfilepath}\\InvoiceSummaryTestData2.csv
    @{lines}=   Split String  ${contents}  \n
    :FOR    ${row}     IN      @{lines}
    \   @{result}=    Split String    ${row}    ,
    \   Run Keyword IF  "@{result}[11]" != "carrier"    Add test case    @{result}[1]
    \   ...              processinvoice  @{result}


Test M2M SSIS To Reconciliation

    ${contents}   Get File    ${csvfilepath}\\TestdataReconcilliationDiffm2m.csv
    @{lines}=   Split String  ${contents}  \n
    :FOR    ${row}     IN      @{lines}
    \   @{result}=    Split String    ${row}    ,
    \   Run Keyword IF  "@{result}[11]" != "carrier"    Add test case    @{result}[1]
    \   ...              processinvoice  @{result}
