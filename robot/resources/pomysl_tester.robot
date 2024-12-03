*** Settings ***
Library    SeleniumLibrary
Library    String
Library    Collections
Library    BuiltIn

*** Keywords ***

Stworz pomysl
    Nowy pomysl z reki
    Wybierz wedlug etykiet    id_priorytet    wysoki
    Wprowadz tekst    id_subject    ${idea_subject}
    Wprowadz tekst    id_opis    ${idea_opis}
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
    Kliknij     Zapisz
    Save Idea Number
    Wyloguj
    Loguj tester
    Przywolaj pomysl
    Wait Until Element Is Visible    xpath=//div[contains(text(),'nowa')]    10s    
    Kliknij i potwierdz    realizuj
    Wait Until Element Is Visible    xpath=//div[contains(text(),'realizowana')]    10s
    Kliknij i potwierdz    analiza
    Wait Until Element Is Visible    xpath=//div[contains(text(),'analiza')]    10s

    Kliknij i potwierdz    rada
    Wait Until Element Is Visible    xpath=//div[contains(text(),'rada architektury')]    10s
    Wait Until Element Is Visible    xpath=//div[contains(text(),'niegotowe')]    10s
   

    # Wait Until Page Contains    Czy dotyczy architektury?    10s
    # Kliknij i potwierdz    arch_yes
    Kliknij i potwierdz    gotowe
    Wait Until Page Contains    do akceptacji      10s
    Kliknij i potwierdz    akcept
    Wait Until Page Contains    zaakceptowane   10s
    Kliknij i potwierdz    Need
    Wait Until Page Contains    Potrzeba   10s
    Save Need Number
    Kliknij i potwierdz    realizuj
    Wait Until Page Contains    realizowana   10s
   # Wait Until Element Is Visible    xpath=//div[contains(text(),'status potrzeby: realizowana')]    110s
    Kliknij    Submit
    Wait Until Page Contains    ${IDEA_NUMBER}     10s
    Przywolaj potrzebe
