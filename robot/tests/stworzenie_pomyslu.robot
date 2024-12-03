
*** Settings ***
Library           SeleniumLibrary
Resource          ../resources/stworzenie_pomyslu.robot
Resource    ../resources/switch_user.robot
Resource    ../resources/recall_object.robot
Resource    ../resources/common_buttons.robot
Resource    ../resources/common_operator.robot
Resource    ../resources/content.robot


*** Variables ***
${BROWSER}        chrome
${URL}            https://avanticdev.gas.pgnig.pl
${USER_USER}       user
${PASS_USER}       qwer
${USER_ARCHITECT}       architect
${USER_DIRECTOR}       director

*** Test Cases ***
Logowanie i stworzenie pomysłu
    Open Browser    ${URL}    ${BROWSER}
    Maximize Browser Window
    Loguj user
    Switch to Pomysly







