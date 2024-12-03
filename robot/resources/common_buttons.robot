*** Settings ***
Library     SeleniumLibrary
Library     String
Library     Collections
Library     BuiltIn

*** Keywords ***

Kliknij i potwierdz
    [Arguments]    ${button_name}
    Wait Until Element Is Visible    xpath=//button[@type='submit' and @name='${button_name}' and (@class='button-normal' or @class='button-danger' or @class='button-proces')]    10s
    Scroll Element Into View     xpath=//button[@type='submit' and @name='${button_name}' and (@class='button-normal' or @class='button-danger' or @class='button-proces' )]
    Click Button      xpath=//button[@type='submit' and @name='${button_name}' and (@class='button-normal' or @class='button-danger' or @class='button-proces' )]
    Handle Alert    ACCEPT

Kliknij     
    [Arguments]    ${button_name}
    Wait Until Element Is Visible    xpath=//button[@type='submit' and (@class='button-normal' or @class='button-proces')and @name='${button_name}']    10s
    Scroll Element Into View    xpath=//button[@type='submit' and (@class='button-normal' or @class='button-proces')and @name='${button_name}']
    Click Button    xpath=//button[@type='submit' and (@class='button-normal' or @class='button-proces')and @name='${button_name}']