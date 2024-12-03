*** Settings ***
Library    SeleniumLibrary
Library    String
Library    Collections
Library    BuiltIn
# Resource    ../resources/procesuj_potrzebe.robot
# Resource    ../resources/stworzenie_pomyslu.robot
Resource    ../resources/switch_user.robot
Resource    ../resources/recall_object.robot
Resource    ../resources/common_buttons.robot
Resource    ../resources/common_operator.robot
# Resource    ../resources/content.robot
# Resource    ../resources/pomysl_tester.robot
# Resource    ../resources/potrzeba_tester.robot
Resource    ../resources/django.robot
# Resource    ../resources/procesuj_zakup.robot

*** Variables ***
${BROWSER}        chrome
${URL}            https://avanticdev.gas.pgnig.pl

*** Test Cases ***
Rada 1
    Open Browser    ${URL}    ${BROWSER}
    Maximize Browser Window
    Loguj tester
    Obiekty na rade

    Mouse Over    xpath=//a[@class="nav-link dropdown-toggle" and contains(text(), 'Obsługa Rady Architektury')]
    Click Element    xpath=//a[@class="nav-link dropdown-toggle" and contains(text(), 'Obsługa Rady Architektury')]
    Wait Until Element Is Visible    xpath=//a[contains(text(), 'Nowe posiedzenie')]    10s    
    Click Element    xpath=//a[contains(text(), 'Nowe posiedzenie')]
    Wait Until Element Is Visible    xpath=//div[contains(text(), 'Omawiane pomysły')]    10s

    Kliknij   otworz
    Save Meeting Number
    Przywolaj rade
 
    Wprowadź Wartość Do Select2   id_attendance_list   architect
    Wprowadź Wartość Do Select2   id_invitations    acceptor
    Wprowadź Wartość Do Select2   id_discussed_ideas    22
    Wprowadź Wartość Do Select2   id_discussed_needs     33
    Wprowadź Wartość Do Select2   id_invitations    director
    Wprowadź Wartość Do Select2   id_invitations    superuser
    Execute JavaScript    window.scroll({ top: 0, left: 0, behavior: 'smooth' });

    Kliknij   zapisz
  #  Kliknij   zapisz

    Verify Option In Select Element    id_invitations    acceptor
    Verify Option In Select Element    id_invitations    director
    Verify Option In Select Element    id_invitations    superuser
     
    Verify Option In Select Element    id_attendance_list     architect
    Close Browser

Rada 2
    Open Browser    ${URL}    ${BROWSER}   
    Maximize Browser Window
    Loguj tester

    Mouse Over    xpath=//a[@class="nav-link dropdown-toggle" and contains(text(), 'Obsługa Rady Architektury')]
    Click Element    xpath=//a[@class="nav-link dropdown-toggle" and contains(text(), 'Obsługa Rady Architektury')]
    Wait Until Element Is Visible    xpath=//a[contains(text(), 'Nowe posiedzenie')]    10s    
    Click Element    xpath=//a[contains(text(), 'Nowe posiedzenie')]
    Wait Until Element Is Visible    xpath=//div[contains(text(), 'Omawiane pomysły')]    10s

    Kliknij   otworz
    Kliknij   dodajdyskutowane

    Save Meeting Number

    Przywolaj rade
 
    Wprowadź Wartość Do Select2    id_attendance_list   director
    Wprowadź Wartość Do Select2    id_invitations    user

    Execute JavaScript    window.scroll({ top: 0, left: 0, behavior: 'smooth' });

    Kliknij   zapisz
 #   Kliknij   zapisz

    Close Browser

Rada 3
    Open Browser    ${URL}    ${BROWSER} 
    Maximize Browser Window
    Loguj tester

    Mouse Over    xpath=//a[@class="nav-link dropdown-toggle" and contains(text(), 'Obsługa Rady Architektury')]
    Click Element    xpath=//a[@class="nav-link dropdown-toggle" and contains(text(), 'Obsługa Rady Architektury')]
    Wait Until Element Is Visible    xpath=//a[contains(text(), 'Nowe posiedzenie')]    10s    
    Click Element    xpath=//a[contains(text(), 'Nowe posiedzenie')]
    Wait Until Element Is Visible    xpath=//div[contains(text(), 'Omawiane pomysły')]    10s

    Kliknij   otworz

    Save Meeting Number

    Przywolaj rade

    Kliknij   z_poprzedniego
    Kliknij   wszyscy
    Kliknij   wyslijagende

    Wprowadź Wartość Do Select2    id_attendance_list   user
    Wprowadź Wartość Do Select2    id_invitations    director
    Wprowadź Wartość Do Select2      id_discussed_ideas    44
    Wprowadź Wartość Do Select2     id_discussed_needs     55

    Execute JavaScript    window.scroll({ top: 0, left: 0, behavior: 'smooth' });

    Kliknij   zapisz
#    Kliknij   zapisz

    Close Browser


*** Keywords ***
Extract Number
    [Arguments]    ${text}    
     ${words}=    Split String    ${text}
     # Wyciągamy trzecie słowo (index 2, bo indexowanie zaczyna się od 0)
    ${trzecie_slowo}=    Set Variable    ${words[2]}
    ${numer}=    Set Variable    ${trzecie_slowo}
    RETURN    ${numer}

