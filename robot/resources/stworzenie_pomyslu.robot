*** Settings ***
Library    SeleniumLibrary
Library    String
Library    Collections
Library    BuiltIn

Resource    text_generator.robot

*** Keywords ***

Switch to Pomysly
    Nowy pomysl z reki
    Wybierz wedlug etykiet    id_priorytet    wysoki
    Wprowadz tekst    id_subject    ${idea_subject}
    ${text_5000}=    Generate Text    5000 
    Wprowadz tekst    id_opis    ${text_5000}
 #   Wprowadz tekst    id_opis    ${idea_opis}
    Wprowadz tekst    id_produkty    ${idea_produkty}
    Wprowadz tekst    id_komentarz    ${idea_komentarz}
    Wprowadz tekst    id_uzasadnienie    ${idea_uzasadnienie}
    Wprowadz tekst    id_wlasciciel_biznesowy    Jan z Kolna
    Wprowadz tekst    id_osoba_kontakowa_u_klienta    Erazm z Roterdamu
    Wybierz wedlug etykiet    id_proponowany_sposob_realizacji    Zakup od Spółek (§ 25)
    Wybierz wedlug etykiet    id_rodzaj_inicjatywy    nowa
    Wybierz wedlug etykiet    id_client    Oddział Zielona Góra
    Wprowadz tekst    id_orientacynjy_budzet    1010000
    Wprowadz tekst    id_wymagana_data_realizacji    09-09-2025
    Kliknij i potwierdz    zawies
    Save Idea Number
    Kliknij i potwierdz    odwies
    Wait Until Element Is Visible    xpath=//div[contains(text(),'nowa')]    10s
    Kliknij    Submit
    # Back to Pomysly
    Przywolaj pomysl
    Wait Until Element Is Visible    xpath=//div[contains(text(),'nowa')]    10s
    Kliknij i potwierdz    realizuj
    Wait Until Element Is Visible    xpath=//div[contains(text(),'realizowana')]    10s
    Kliknij i potwierdz    analiza
    Wait Until Element Is Visible    xpath=//div[contains(text(),'analiza')]    10s
    Wait Until Element Is Visible    xpath=//input[@name='tresc_notatki']    10s
    Input Text    xpath=//input[@name='tresc_notatki']    ${idea_note_text}
    Click Button    xpath=//button[contains(@class, 'button-normal') and text()='Dodaj notatkę']
    Handle Alert
    Wait Until Element Is Visible    xpath=//div[contains(text(),'${idea_note_text}')]    10s
    # przelogowanie na architekta
    Wyloguj
    Loguj architect
    Przywolaj pomysl
     Wait Until Element Is Visible    xpath=//div[contains(text(),'niegotowe')]    10s
    #Wait Until Element Is Visible    xpath=//div[contains(@style, 'background-color: gray; color: black;') and contains(text(), 'niegotowa do akceptacj')]    10s
    Kliknij i potwierdz    arch_no
   #  Wait Until Page Contains    Czy dotyczy architektury?    10s
   #  Wait Until Element Is Visible    xpath=//div[contains(@style, 'background-color: hsl(60, 20%, 82%)')]    10s
    Kliknij i potwierdz    arch_yes
    Kliknij i potwierdz    rada   
    Kliknij i potwierdz    gotowe
    Wait Until Page Contains    do akceptacji    10s
    # przelogowanie na dyrektora
    Wyloguj
    Loguj director
    Przywolaj pomysl
    Wait Until Page Contains     do akceptacji   10s
    Wprowadz tekst    id_komentarz_akceptujacego    ${komentarz_akceptujacego_pomysl}
    Kliknij i potwierdz    popraw
    Wait Until Page Contains     do poprawy   10s
    # przelogowanie na usera
    Wyloguj
    Loguj user
    Przywolaj pomysl
    Wait Until Page Contains     do poprawy  10s
    Kliknij i potwierdz    analiza    
    Wait Until Element Is Visible    xpath=//div[contains(text(),'analiza')]    10s
 

    # Kliknij i potwierdz    rada
    # Wait Until Element Is Visible    xpath=//div[contains(text(),'status pomysłu: rada architektury')]    10s
    # przelogowanie na architekta
    Wyloguj
    Loguj architect
    Przywolaj pomysl

    Kliknij i potwierdz    rada
    Wait Until Element Is Visible    xpath=//div[contains(text(),'rada architektury')]    10s
 

    Wait Until Element Is Visible    xpath=//div[contains(text(), ' do poprawy')]    10s
    Wait Until Element Is Visible    xpath=//div[contains(text(),'rada architektury')]    10s
    Kliknij i potwierdz    gotowe
    Wait Until Page Contains     do akceptacji   10s
    Wyloguj
    Loguj director
    Przywolaj pomysl
    Wait Until Page Contains     do akceptacji     10s
    Kliknij i potwierdz    akcept
    Wait Until Page Contains     zaakceptowane   10s
    # Pomysł jest zaakceptowany
    # Powrót do roli user
    Wyloguj
    Loguj user
    Przywolaj pomysl
    Wait Until Page Contains     zaakceptowane   10s
    Kliknij i potwierdz    Need
    Wait Until Page Contains    Potrzeba    10s
    Save Need Number
    Kliknij i potwierdz    realizuj
    Wait Until Page Contains    realizowana   10s
    Kliknij    Submit
    Wait Until Page Contains    ${IDEA_NUMBER}   10s
    Przywolaj potrzebe
