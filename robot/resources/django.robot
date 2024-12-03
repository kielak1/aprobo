
*** Settings ***
Library    SeleniumLibrary
Library    Process
Library    OperatingSystem

*** Keywords ***
Run Django Command
    [Arguments]    ${command}
    Log    Running command: ${command}
    Log    CURDIR: ${CURDIR}/
    ${full_command}    Set Variable    python ../manage.py ${command}
    Log    Full command: ${full_command}
    Run Process    python    ../manage.py    ${command}    cwd=${CURDIR}/..

Usun zakup
    Run Django Command    delete_one_purchase

Popsuj umowe
    Run Django Command    popsuj_umowe

Obiekty na rade
    Run Django Command    obiekty_na_rade
    