


*** Settings ***
Library           SeleniumLibrary
Resource          ../resources/lista_umow_do_kontynuacji.robot

*** Variables ***
${BROWSER}        chrome
${URL}            https://avanticdev.gas.pgnig.pl
${USER_USER}       user
${PASS_USER}       qwer

*** Test Cases ***

Logowanie i wyświetlenie listy umów do kontynuacji
    Open Browser    ${URL}    ${BROWSER}
    Maximize Browser Window
    Title Should Be    AvanTIc
    Login User
    Select Continuity Of Services
    Logout



