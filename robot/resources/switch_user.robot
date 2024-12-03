*** Settings ***
Library     SeleniumLibrary
Library     String
Library     Collections
Library     BuiltIn

*** Keywords ***

Wyloguj
    [Documentation]  Test wylogowania
    Sleep  1s
    Wait Until Element Is Visible    xpath=//a[@class='nav-link dropdown-toggle' and contains(text(),'Konto')]  10s
    Sleep  1s
    Scroll Element Into View    xpath=//a[@class='nav-link dropdown-toggle' and contains(text(),'Konto')]
    Click Element    xpath=//a[@class='nav-link dropdown-toggle' and contains(text(),'Konto')]
    Wait Until Element Is Visible    xpath=//a[contains(text(),'wyloguj')]  10s
    Click Element    xpath=//a[contains(text(),'wyloguj')]




Loguj user
    Wait Until Element Is Visible       xpath=//a[text()='Konto']   10s
    Scroll Element Into View      xpath=//a[text()='Konto'] 
    Click Element    xpath=//a[text()='Konto']
    Wait Until Element Is Visible    xpath=//a[text()='Zaloguj']    10s
    Click Element    xpath=//a[text()='Zaloguj']
    Wait Until Page Contains Element    id=id_username    10s
    Input Text    id=id_username    user
    Input Text    id=id_password    qwer
    Click Button    xpath=//input[@type='submit' and @value='Zaloguj']
    Wait Until Page Contains Element    xpath=//a[@class='nav-link' and contains(text(),'user')]    10s

Loguj acceptor
    Wait Until Element Is Visible       xpath=//a[text()='Konto']   10s
    Scroll Element Into View      xpath=//a[text()='Konto'] 
    Click Element    xpath=//a[text()='Konto']
    Wait Until Element Is Visible    xpath=//a[text()='Zaloguj']    10s
    Click Element    xpath=//a[text()='Zaloguj']
    Wait Until Page Contains Element    id=id_username    10s
    Input Text    id=id_username    acceptor
    Input Text    id=id_password    qwer
    Click Button    xpath=//input[@type='submit' and @value='Zaloguj']
    Wait Until Page Contains Element    xpath=//a[@class='nav-link' and contains(text(),'acceptor')]    10s

Loguj architect
    Wait Until Element Is Visible       xpath=//a[text()='Konto']   10s
    Scroll Element Into View      xpath=//a[text()='Konto'] 
    Click Element    xpath=//a[text()='Konto']
    Wait Until Element Is Visible    xpath=//a[text()='Zaloguj']    10s
    Click Element    xpath=//a[text()='Zaloguj']
    Wait Until Page Contains Element    id=id_username    10s
    Input Text    id=id_username    architect
    Input Text    id=id_password    qwer
    Click Button    xpath=//input[@type='submit' and @value='Zaloguj']
    Wait Until Page Contains Element    xpath=//a[@class='nav-link' and contains(text(),'architect')]    10s

Loguj director
    Wait Until Element Is Visible       xpath=//a[text()='Konto']   10s
    Scroll Element Into View      xpath=//a[text()='Konto'] 
    Click Element    xpath=//a[text()='Konto']
    Wait Until Element Is Visible    xpath=//a[text()='Zaloguj']    10s
    Click Element    xpath=//a[text()='Zaloguj']
    Wait Until Page Contains Element    id=id_username    10s
    Input Text    id=id_username    director
    Input Text    id=id_password    qwer
    Click Button    xpath=//input[@type='submit' and @value='Zaloguj']
    Wait Until Page Contains Element    xpath=//a[@class='nav-link' and contains(text(),'director')]    10s

Loguj tester
    Wait Until Element Is Visible       xpath=//a[text()='Konto']   10s
    Scroll Element Into View      xpath=//a[text()='Konto'] 
    Click Element    xpath=//a[text()='Konto']
    Wait Until Element Is Visible    xpath=//a[text()='Zaloguj']    10s
    Click Element    xpath=//a[text()='Zaloguj']
    Wait Until Page Contains Element    id=id_username    10s
    Input Text    id=id_username    tester
    Input Text    id=id_password    qwer
    Click Button    xpath=//input[@type='submit' and @value='Zaloguj']
    Wait Until Page Contains Element    xpath=//a[@class='nav-link' and contains(text(),'tester')]    10s

