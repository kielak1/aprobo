*** Settings ***
Library           SeleniumLibrary

*** Keywords ***
Login User
    Click Element    xpath=//a[text()='Konto']
    Wait Until Element Is Visible    xpath=//a[text()='Zaloguj']    10s
    Click Element    xpath=//a[text()='Zaloguj']
    Wait Until Page Contains Element    id=id_username    10s
    Input Text    id=id_username    ${USER_USER}
    Input Text    id=id_password    ${PASS_USER}
    Click Button    xpath=//input[@type='submit' and @value='Zaloguj']
    Wait Until Page Contains Element    xpath=//a[@class='nav-link' and contains(text(),'user')]    10s


Logout
    Click Element    xpath=//a[text()='Konto']
    # Wait Until Element Is Visible    xpath=//a[text()='wyloguj']    10s
    # Click Element    xpath=//a[text()='wyloguj']
    Wait Until Element Is Visible    xpath=//a[starts-with(text(),'wyloguj')]   10s
    Click Element    xpath=//a[starts-with(text(),'wyloguj')]
    Click Element    xpath=//a[text()='Konto']
    Wait Until Element Is Visible    xpath=//a[text()='Zaloguj']    10s 


Select Continuity Of Services
    Click Element    xpath=//a[contains(text(),'Ciągłość serwisów')]
    Wait Until Element Is Visible    xpath=//a[contains(text(),'Ciągłość usług')]  12s
    Mouse Over    xpath=//a[contains(text(),'Ciągłość usług')]
    Wait Until Element Is Visible    xpath=//a[contains(text(),'Wszystkie działy')]  12s
    Click Element    xpath=//a[contains(text(),'Wszystkie działy')]
    Wait Until Element Is Visible    xpath=//div[contains(@class, 'header_lit') and contains(text(), 'Umowy wymagające kontynuacji')]   12s
    Element Should Be Visible    xpath=//div[contains(@class, 'header_lit') and contains(text(), 'Umowy wymagające kontynuacji')]

