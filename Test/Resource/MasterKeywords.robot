*** Settings ***
Library             SeleniumLibrary
Library         OperatingSystem
Library        ../Core/DynamicTestCases.py
Library         String


*** Variables ***
${BROWSER}  chrome
${URL}  https://max.mobilesolutions.net/
${SELENIUM_SPEED}   0.5 seconds
${utcglobal}    None
${pdfinvoicePATH}  D:\\File
${ATTPdfReaderConsoleApplicationexe}   C:\\Users\\gaucho.agregado\\Documents\\GitHub\\ATTPdfParser\\ATTPdfReaderConsoleApplication\\bin\\Debug\\netcoreapp3.1\\ATTPdfReaderConsoleApplication.exe
${csvfilepath}  C:\\Users\\gaucho.agregado\\Documents\\new folder pdf [parser automation\\max-automated-testing\\Test\\Resource
${VerizonPdfReaderConsoleApplicationexe}    C:\\Users\\gaucho.agregado\\Documents\\GitHub\\VerizonPdfParser\\Com.MobileSolutions.VerizonPdfReaderConsoleApplication\\bin\\Debug\\netcoreapp3.1\\Com.MobileSolutions.VerizonPdfReaderConsoleApplication.exe

*** Keywords ***


Setup one test for each item
    ${File}=    Get File  tickets.txt
    @{list}=    Split to lines  ${File}     
    :FOR    ${line} IN  @{list}
    \   Log ${line}
    \   ${Value}=   Get Variable Value  ${line}
    \   Add test case    remove for ticket # ${Value}
    \     ...              sortandCompare    @{files}[${i}]
    

Launch MAX
    open browser    ${URL}  ${BROWSER}
    Set Selenium Speed	${SELENIUM_SPEED}
    Maximize Browser Window    

Login MAX
    [Arguments]     ${username}     ${password}
    Wait Until Element is Visible   xpath=//input[@name='username']     15
    Input Text  xpath=//input[@name='username']     ${username}
    Input Text  xpath=//input[@name='password']     ${password}
    Click Button    xpath=//button[text()='Login']
    Sleep   5
    Wait Until Element Is Visible   xpath=//*[@title='User Menu']   15

Left Menu Click
    [Arguments]     ${title}
    Click Element   xpath=//*[@class='sidebar']/descendant::a[text()='${title}']
    Element Should Be Visible   xpath=//ul[@class='breadcrumb']/descendant::span[contains(text(),'${title}')]

Logout MAX
    Click Element   xpath=//*[@title='User Menu']
    Wait Until Element Is Visible   xpath=//a[contains(text(),'Log Out')]   5
    Click Element   xpath=//a[contains(text(),'Log Out')]
    Page Should Contain    You are now logged out.

Select Customer
    [Arguments]     ${custname}
    
    Wait Until Element Is Visible   xpath=//div[@placeholder='Customer context...']     15
    Click Element   xpath=//div[@placeholder='Customer context...']

    Input Text  xpath=//input[@placeholder='Customer context...']   ${custname}

    Wait Until Element Is Visible   xpath=//input[@placeholder='Customer context...']/following-sibling::ul     5
    Click Element   xpath=//input[@placeholder='Customer context...']/following-sibling::ul

Select Licensee
    [Arguments]     ${licensee}
    Wait Until Element Is Visible   xpath=//div[@placeholder='Licensee context...']     15
    Click Element   xpath=//div[@placeholder='Licensee context...']

    Input Text  xpath=//input[@placeholder='Licensee context...']    ${licensee}

    Wait Until Element Is Visible   xpath=//input[@placeholder='Licensee context...']/following-sibling::ul     5
    Click Element   xpath=//input[@placeholder='Licensee context...']/following-sibling::ul

Create Activation Need Device Ticket and Submit
    Wait Until Element Is Visible   xpath=//a[text()='Tickets']     15
    Click Element   xpath=//a[text()='Tickets']

    Wait Until Element Is Visible   xpath=//span[text()='(Need Device)']/parent::a  10
    Click Element   xpath=//span[text()='(Need Device)']/parent::a

    Wait Until Element Is Visible   xpath=//label[text()='Carrier *']/following-sibling::select     10
    Click Element   xpath=//label[text()='Carrier *']/following-sibling::select

    Wait Until Element Is Visible    xpath=//label[text()='Carrier *']/following-sibling::select/option[contains(text(),'AT&T')]     10
    Click Element   xpath=//label[text()='Carrier *']/following-sibling::select/option[contains(text(),'AT&T')]

    Wait Until Element Is Visible    xpath=//label[text()='Account *']/following-sibling::select/option[contains(text(),'AT&T')]     10
    Click Element   xpath=//label[text()='Account *']/following-sibling::select/option[contains(text(),'AT&T')]

    Wait Until Element Is Visible    xpath=//*[@data-title='2 Year Contract']    10
    #Sleep   5
    #Click Element   xpath=//*[@data-title='2 Year Contract']
    Click Element   xpath=//*[@data-title='2 Year Contract']/descendant::input/following-sibling::span

    Click Element   xpath=//button[text()='Submit']

    Wait Until Element Is Visible   xpath=//*[contains(text(),'iPhone 12')]/following-sibling::*/descendant::select[@name='deviceColors']   10
    Click Element   xpath=//*[contains(text(),'iPhone 12')]/following-sibling::*/descendant::select[@name='deviceColors']

    Click Element   xpath=//*[contains(text(),'iPhone 12')]/following-sibling::*/descendant::select[@name='deviceColors']/option[@label='Black']

    Click Element   xpath=//*[contains(text(),'iPhone 12')]/following-sibling::*/descendant::select[@name='deviceStorageOptions']

    Click Element   xpath=//*[contains(text(),'iPhone 12')]/following-sibling::*/descendant::select[@name='deviceStorageOptions']/option[@label='64GB']


    Click Element   xpath=//*[contains(text(),'iPhone 12')]/following-sibling::*/descendant::button[contains(text(),'Add to Cart')]


    #Execute JavaScript    window.document.evaluate("//a[contains(text(),'Next')])[1]", document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue.scrollIntoView(true);
    Execute JavaScript    window.document.evaluate("(//a[contains(text(),'Next')])[1]", document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue.click();
    
    #Click Element   xpath=(//a[contains(text(),'Next')])[1]



    Wait Until Element Is Visible  xpath=//input[@name='lineName']  10
    Input Text  xpath=//input[@name='lineName']     auto_user1


    Click Element   xpath=//div[@name='organizationStructure0']
    Sleep   3
    Input Text  xpath=//div[@name='organizationStructure0']/descendant::input   Quanta Marine

    Click Element  xpath=//span[text()='Quanta Marine']

    Wait Until Element Is Visible   xpath=//div[@name='organizationStructure1']   10
    Click Element   xpath=//div[@name='organizationStructure1']
    Input Text  xpath=(//div[@name='organizationStructure1']/descendant::input)[1]   Quanta Marine

    Click Element   xpath=(//span[text()='Quanta Marine'])[2]

    Click Element   xpath=//div[@name='organizationStructure2']
    Input Text  xpath=(//label[contains(text(),'Division/Cost Code *')]/following-sibling::*/div/descendant::input)[1]  Quanta

    Click Element   xpath=(//span[contains(text(),'Quanta')])[5]

    Click Element   xpath=(//a[contains(text(),'Next')])[2]


    Click Element   xpath=(//a[contains(text(),'Next')])[3]


    Click Element   xpath=//input[@name='attentionTo']

    Input text  xpath=//input[@name='attentionTo']  testqa

    Click Element   xpath=//label[text()='Shipped by *']/following-sibling::select
    Click Element   xpath=//label[text()='Shipped by *']/following-sibling::select/option[@value='2']


    Click Element   xpath=//button[contains(text(),'Submit Order')]



Fulfillment Officer Update Ticket To Complete
    [Arguments]     ${ticket}

    
    Wait Until Element Is Visible   xpath=//a[text()='Tickets']     15
    Click Element   xpath=//a[text()='Tickets']

    Wait Until Element Is Visible   xpath=//a[text()='All']     15
    Click Element   xpath=//a[text()='All']

    Wait Until Element Is Visible   xpath=//span[text()='${ticket}']   15
    Click Element   xpath=//span[text()='${ticket}']/parent::td/preceding-sibling::td/a

    Wait Until Element Is Visible   xpath=//a[contains(text(),'${ticket}')]   15
    Click Element   xpath=//a[contains(text(),'${ticket}')]


    Wait Until Element Is Visible   xpath=//a[contains(text(),'Update')]    15
    Click Element   xpath=//a[contains(text(),'Update')]



    Page Should Contain     Carrier Portal Procurement Option
    Page Should Contain Element     xpath=//select[@name='carrierPortalProcurementOptionSelectBox']


    Input Text  xpath=(//textarea[@name='notes'])[1]    This is test notes for activation need device ticket



    Click Element   xpath=//select[@name='ticketStatusId']
    Click Element   xpath=//select[@name='ticketStatusId']/option[@value='COMPLETE']
    Input text  xpath=//input[@name='confirmationNumber']  12345678
    Click Element   xpath=//label[text()='Yes']/input
    Click Element   xpath=//select[@name='carrierPortalProcurementOptionSelectBox']
    Click Element   xpath=//select[@name='carrierPortalProcurementOptionSelectBox']/option[@label='OPUS']


    Input text  xpath=//input[@name='orderNumber']  12345678
    Input text  xpath=//input[@name='iccidSim']     (910) 638-5797
    Input text  xpath=//input[@name='deviceIdentifier']     12345678
    Click Element   xpath=//div[@name='shippingProvider']
    Click Element   xpath=//span[text()='FedEx']
    Input text  xpath=//input[@name='shippedOn']    09/09/2022
    Input text  xpath=//input[@name='trackingNumber']  45454545

 
    Click Element   xpath=//a[text()='Activation']
    Input text  xpath=//input[@name='newPhoneNumber']     (910) 638-5777

    Click Element   xpath=//button[@type='submit']



Fulfillment Officer Update Ticket To Complete Without Selecting Carrier Portal
    [Arguments]     ${ticket}

    
    Wait Until Element Is Visible   xpath=//a[text()='Tickets']     15
    Click Element   xpath=//a[text()='Tickets']

    Wait Until Element Is Visible   xpath=//a[text()='All']     15
    Click Element   xpath=//a[text()='All']

    Wait Until Element Is Visible   xpath=//span[text()='${ticket}']   15
    Click Element   xpath=//span[text()='${ticket}']/parent::td/preceding-sibling::td/a

    Wait Until Element Is Visible   xpath=//a[contains(text(),'${ticket}')]   15
    Click Element   xpath=//a[contains(text(),'${ticket}')]


    Wait Until Element Is Visible   xpath=//a[contains(text(),'Update')]    15
    Click Element   xpath=//a[contains(text(),'Update')]


    Input Text  xpath=(//textarea[@name='notes'])[1]    This is test notes for activation need device ticket



    Click Element   xpath=//select[@name='ticketStatusId']
    Click Element   xpath=//select[@name='ticketStatusId']/option[@value='COMPLETE']
    Input text  xpath=//input[@name='confirmationNumber']  12345678
    Click Element   xpath=//label[text()='Yes']/input

    Input text  xpath=//input[@name='orderNumber']  12345678
    Input text  xpath=//input[@name='iccidSim']     (910) 638-5797
    Input text  xpath=//input[@name='deviceIdentifier']     12345678
    Click Element   xpath=//div[@name='shippingProvider']
    Click Element   xpath=//span[text()='FedEx']
    Input text  xpath=//input[@name='shippedOn']    09/09/2022
    Input text  xpath=//input[@name='trackingNumber']  45454545

 
    Click Element   xpath=//a[text()='Activation']
    Input text  xpath=//input[@name='newPhoneNumber']     (910) 638-5777

    Click Element   xpath=//button[@type='submit']

Verify Ticket Status is Complete
    Wait Until Element Is Visible   xpath=//span[text()='Complete']     20

Customer Menu - Users
    Click Element   xpath=(//li/div/span/a[text()='Users'])[1]

Customer Menu - Create User
    Click Element   xpath=//a/span[text()='Create User']
    Wait Until Element Is Visible   xpath=//input[@name='firstName']    20
    Input Text  xpath=//input[@name='firstName']    Gaucho
    Input Text  xpath=//input[@name='lastName']    Agregado
    Input Text  xpath=//input[@name='userName']    gbagregado
    Click Element   xpath=//div[@name='roleId']
    Sleep   2
    Click Element   xpath=//div[@name='roleId']/descendant::span[text()='End User QUANTA CORP']
    Click Element   xpath=//label[text()='Licensee']/following-sibling::select
    Click Element   xpath=//label[text()='Licensee']/following-sibling::select/option[contains(text(),'Mobile Solutions')]
    Click Element   xpath=//input[contains(@placeholder,'Select Customer')]
    Input Text  xpath=//input[contains(@placeholder,'Select Customer')]     Quanta
    Click Element   xpath=//span[text()='Quanta']
    Click Element   //button[contains(text(),'Create No Invite')]

