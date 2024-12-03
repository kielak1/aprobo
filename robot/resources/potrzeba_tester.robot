*** Settings ***
Library    SeleniumLibrary
Library    String
Library    Collections
Library    BuiltIn

*** Keywords ***

Proceduj potrzebe
    Przywolaj potrzebe
    Kliknij i potwierdz  do_akceptacji_infra
    Kliknij i potwierdz  do_akceptacji_siec
    Kliknij i potwierdz  do_akceptacji_uslugi
    Kliknij i potwierdz  do_akceptacji_finanse
    Kliknij i potwierdz  akceptuj_infra
    Kliknij i potwierdz  akceptuj_siec
    Kliknij i potwierdz  akceptuj_uslugi
    Kliknij i potwierdz  akceptuj_finanse
    Kliknij i potwierdz  analiza
    Kliknij i potwierdz  rada
    Kliknij i potwierdz  gotowe
    Kliknij i potwierdz  akcept

    