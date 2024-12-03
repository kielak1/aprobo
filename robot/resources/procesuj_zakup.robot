*** Settings ***
Library  SeleniumLibrary
Library  String
Library  Collections
Library  BuiltIn

*** Keywords ***

Procesuj zakup
  WyLoguj
  Loguj user
  Przywolaj potrzebe
  Wybierz wedlug pozycji  id_ezz_do_powiazania  1
  Kliknij i potwierdz  link_EZZ
  Save Purchase Number
  Wybierz wedlug pozycji  id_odlinkowany_purchase  1
  Kliknij i potwierdz  unlinkj_purchase
  Wybierz wedlug pozycji  id_podlinkowany_purchase  1
  Kliknij i potwierdz  link_purchase
  Save Purchase Number
  Przywolaj Zakup
  Kliknij checkbox  id_odtworzeniowy
  Kliknij checkbox  id_rozwojowy
  Wybierz wedlug pozycji  id_pilnosc  1
  Wybierz wedlug pozycji  id_sposob_wyceny  1
  Wprowadz tekst  id_waluta  USD
  Wprowadz tekst  id_budzet_opex_netto  1300  
  Wprowadz tekst  id_budzet_capex_netto  5400
  Wprowadz tekst  id_komentarz  Jestem z tobą na tyle szczera, że muszę cię zapewnić o mojej niezachwianej uczciwości.
  #Wprowadz tekst  id_planowany_termin_platnosci  75 dni po otrzymaniu faktury
  Wprowadz tekst  id_id_sap  44990  
  # Wybierz wedlug pozycji  id_zgodnosc_mapy  1
  Wprowadz tekst  id_dostawca  Frank Herbert, Kapitularz Diuną
  # Wait Until Element Is Visible  id_crip_id
  # Scroll Element Into View  id_crip_id
  # Select From List By Value  id_crip_id  4
  # Select From List By Value  id_crip_id  3
  # Wait Until Element Is Visible  id_acceptors
  # Scroll Element Into View  id_acceptors
  # Select From List By Value  id_acceptors  1
  # Select From List By Value  id_acceptors  2
  Wprowadz tekst  id_komentarz  Frank Herbert, Kapitularz Diuną
  Wprowadz tekst  id_link_do_ezz  https://lubimyczytac.pl/cytaty/72579/ksiazka/kapitularz-diuna
  
  # Kliknij i potwierdz  gotowe
  # WyLoguj
  # Loguj director
  # Przywolaj zakup
  # Wprowadz tekst  id_komentarz_akceptujacego  O co chodzi
  # Kliknij i potwierdz  popraw
  # WyLoguj
  # Loguj user
  # Przywolaj zakup
  # Kliknij i potwierdz  gotowe
  # WyLoguj
  # Loguj director
  # Przywolaj zakup
  # Kliknij i potwierdz  akcept
  
  WyLoguj
  Loguj user
  Przywolaj zakup
  Kliknij i potwierdz  wezz
  Kliknij i potwierdz  Zakupbgnig
  Kliknij i potwierdz  Zakupstandardowy
  Kliknij i potwierdz  wrealizacji
  Kliknij i potwierdz  zakonczony
  Kliknij i potwierdz  wrealizacji
  Kliknij i potwierdz  anulowany
  Kliknij i potwierdz  wrealizacji
  WyLoguj
  # Loguj director
  # Przywolaj zakup
  # Kliknij i potwierdz  cofnij_akceptacje
  # WyLoguj
  # Loguj user
  # Przywolaj zakup
  # Kliknij i potwierdz  gotowe
  # WyLoguj
  # Loguj director
  # Przywolaj zakup
  # Kliknij i potwierdz  akcept
  # WyLoguj
  # Loguj user
  # Przywolaj zakup
  # Kliknij i potwierdz  Zakupstandardowy
  # Kliknij i potwierdz  wrealizacji
  # Kliknij i potwierdz  zakonczony
