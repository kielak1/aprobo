*** Settings ***
Library    SeleniumLibrary
Resource    ../resources/procesuj_potrzebe.robot
Resource    ../resources/stworzenie_pomyslu.robot
Resource    ../resources/switch_user.robot
Resource    ../resources/django.robot
Resource    ../resources/procesuj_zakup.robot
Resource    ../resources/recall_object.robot
Resource    ../resources/common_buttons.robot
Resource    ../resources/common_operator.robot
Resource    ../resources/content.robot

*** Variables ***
${BROWSER}        chrome
${URL}            https://avanticdev.gas.pgnig.pl

   
*** Test Cases ***
Od pomyslu do potrzeby
    Usun zakup
    Open Browser    ${URL}    ${BROWSER}
    Maximize Browser Window

    Loguj user
    Switch to Pomysly
    Wyloguj 

    Loguj user
    Procesuj potrzebe
    Procesuj zakup

