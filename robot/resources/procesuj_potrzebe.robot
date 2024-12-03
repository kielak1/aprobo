*** Settings ***
Library  SeleniumLibrary
Library  String
Library  Collections
Library  BuiltIn

*** Keywords ***

Procesuj potrzebe
  Przywolaj potrzebe
  #  TUTAJ zaczyna sie wlasciwy test
  Wybierz wedlug etykiet  id_pilnosc  średnia
  Kliknij checkbox  id_rozwojowy
  Kliknij checkbox  id_odtworzeniowy
  Wprowadz tekst  id_link_do_clarity  https://opel.com
  Wprowadz tekst  id_link_do_dokumentacji  ttps://www.onet.pl/
  Kliknij checkbox  id_czy_inicjatywa_dotyczy_aplikacji
  Wybierz wedlug etykiet  id_klasyfikacja_w_sensie_procedury_jakosci  Projekty (III)
  Wprowadz tekst  id_godziny_dostepnosci_rozwiazania  7-15
  Wprowadz tekst  id_oczekiwany_czas_reakcji  48
  Wprowadz tekst  id_oczekiwany_czas_przywrocenia  96
  Kliknij checkbox  id_czy_wymagana_jest_infrastruktura
  Kliknij checkbox  id_czy_zadanie_zostalo_zaplanowane
  Wait Until Element Is Visible  id=id_pozycje_z_planu_CRIP
  Scroll Element Into View  id=id_pozycje_z_planu_CRIP
 
  Wprowadź Wartość Do Select2     id_pozycje_z_planu_CRIP     PL-PGN-ITG-2023-006139
  Wprowadź Wartość Do Select2     id_pozycje_z_planu_CRIP     PL-PKN-ITT-2023-006286

  Kliknij checkbox  id_czy_przedmiotem_zakupu_sa_uslugi_inne_niz_wsparcia
  Wait Until Element Is Visible  id=id_rodzaj_kupowanych_uslug
  Scroll Element Into View  id=id_rodzaj_kupowanych_uslug

  Wprowadź Wartość Do Select2   id_rodzaj_kupowanych_uslug   Doraźne prace konsultanta
  Wprowadź Wartość Do Select2   id_rodzaj_kupowanych_uslug   Prace programistyczne
  
  Kliknij   Zapisz 

  Verify Option In Select Element    id_pozycje_z_planu_CRIP     PL-PGN-ITG-2023-006139 - SIN_Odnowienie licencji i usług wsparcia na potrze 
  Verify Option In Select Element    id_pozycje_z_planu_CRIP     PL-PKN-ITT-2023-006286 - SIN_Zakup Subskrypcji Systemu Runecast  
  Verify Option In Select Element    id_rodzaj_kupowanych_uslug   Doraźne prace konsultanta       
  Verify Option In Select Element    id_rodzaj_kupowanych_uslug    Prace programistyczne       

  Wprowadz tekst  id_capex  48
  Wprowadz tekst  id_opex  48
  Wprowadz tekst  id_numer_zadania_inwestycyjnego  1001
  Wait Until Element Is Visible  id=id_sposob_okreslenia_budzetu
  Scroll Element Into View  id=id_sposob_okreslenia_budzetu
  Select From List By Value  id=id_sposob_okreslenia_budzetu  2
  # teraz symulacja procesu
  Kliknij i potwierdz  do_akceptacji_infra
  Kliknij i potwierdz  do_akceptacji_siec
  Kliknij i potwierdz  do_akceptacji_uslugi
  Kliknij i potwierdz  do_akceptacji_finanse
  Kliknij  Submit
  # przelogowanie na acceptora
  WyLoguj 
  Loguj acceptor
  Przywolaj potrzebe
  Wprowadz tekst  id_komentarz_infrastrukturalny  ${komnentarz_infrastruktura}
  Kliknij i potwierdz  do_poprawy_infra
  Wprowadz tekst  id_komentarz_sieciowy  ${komentarz_siec}
  Kliknij i potwierdz  do_poprawy_siec
  Wprowadz tekst  id_komentarz_uslugowy  ${komentarz_uslug}
  Kliknij i potwierdz  do_poprawy_uslugi
  Wprowadz tekst  id_komentarz_finansowy  ${komentarz_finanse}
  Kliknij i potwierdz  do_poprawy_finanse
  #powrot do roli user aby odpowiedziec na komentarze acceptora
  WyLoguj 
  Loguj user
  Przywolaj potrzebe
  # udzielenie odpowedzi acceptorom
  Wprowadz tekst  id_odpowiedz_na_infrastrukturalny  ${odpowiedz_infrastruktura}
  Kliknij i potwierdz  do_akceptacji_infra
  Wprowadz tekst  id_odpowiedz_na_sieciowy  ${odpowiedz_siec}
  Kliknij i potwierdz  do_akceptacji_siec
  Wprowadz tekst  id_odpowiedz_na_uslugowy  ${odpowiedz_uslugi}
  Kliknij i potwierdz  do_akceptacji_uslugi
  Wprowadz tekst  id_odpowiedz_na_finansowy  ${odpowiedz_finanse}
  Kliknij i potwierdz  do_akceptacji_finanse
  WyLoguj 
  Loguj acceptor
  Przywolaj potrzebe
  Kliknij i potwierdz  akceptuj_infra
  Kliknij i potwierdz  akceptuj_siec
  Kliknij i potwierdz  akceptuj_uslugi
  Kliknij i potwierdz  akceptuj_finanse
  WyLoguj 
  Loguj user
  Przywolaj potrzebe
  Kliknij i potwierdz  analiza
  WyLoguj 
  Loguj architect
  Przywolaj potrzebe
  Kliknij i potwierdz  arch_no
  Kliknij i potwierdz  arch_yes
  # spraWdzenie czy na stronie jest pole z dwoma zagnoiezdzonymi div (weryfikacja czy dla multiple choice nie zniknely wartosci )  - do ulepszenia
  Wait Until Element Is Visible  xpath=//div[@class='read_only_list' and @style='width: 550px; max-height: 120px;']
  ${inner_divs}=  Get WebElements  xpath=//div[@class='read_only_list' and @style='width: 550px; max-height: 120px;']/div
  ${count}=  Get Length  ${inner_divs}
  Should Be Equal As Numbers  ${count}  4
  # dołożenie notatki
  Wait Until Element Is Visible  xpath=//input[@name='tresc_notatki']  3s
  Scroll Element Into View  xpath=//input[@name='tresc_notatki']
  Input Text  xpath=//input[@name='tresc_notatki']  ${need_note_text}
  Click Button  xpath=//button[contains(@class, 'button-normal') and text()='Dodaj notatkę']
  Handle Alert
  Wait Until Element Is Visible  xpath=//div[contains(text(),'${need_note_text}')]  3s
  Kliknij i potwierdz  rada
  Kliknij i potwierdz  gotowe
  WyLoguj 
  Loguj director
  Przywolaj potrzebe
  Wprowadz tekst  id_komentarz_akceptujacego  ${komentarz_akceptujacego_potrzebe}
  Kliknij i potwierdz  popraw
  WyLoguj 
  Loguj user
  Przywolaj potrzebe
  Wprowadz tekst  id_odpowiedz_do_akceptujacego  ${id_odpowiedz_do_akceptujacego_potrzebe}
  Kliknij i potwierdz  analiza 
  WyLoguj 
  Loguj architect
  Przywolaj potrzebe
  Kliknij i potwierdz  rada
  Kliknij i potwierdz  gotowe
  WyLoguj 
  Loguj director
  Przywolaj potrzebe
  Kliknij i potwierdz  akcept
