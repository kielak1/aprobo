*** Settings ***
Library    SeleniumLibrary
Resource    ../resources/procesuj_potrzebe.robot
Resource    ../resources/stworzenie_pomyslu.robot
Resource    ../resources/switch_user.robot
Resource    ../resources/recall_object.robot
Resource    ../resources/common_buttons.robot
Resource    ../resources/common_operator.robot
Resource    ../resources/content.robot
Resource    ../resources/pomysl_tester.robot
Resource    ../resources/potrzeba_tester.robot
Resource    ../resources/django.robot
Resource    ../resources/procesuj_zakup.robot

*** Variables ***
${BROWSER}        chrome
${URL}            https://avanticdev.gas.pgnig.pl
#${NEED_NUMBER}   2863
   
*** Test Cases ***
Zakupy
    Usun zakup
    Open Browser    ${URL}    ${BROWSER}
    Maximize Browser Window

    Loguj tester
    Stworz pomysl
    Proceduj potrzebe
    Procesuj zakup



