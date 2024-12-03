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
Umowy
    Popsuj umowe
    Open Browser    ${URL}    ${BROWSER}
    Maximize Browser Window
  

    Open Browser    https://avanticdev.gas.pgnig.pl/contracts/edit_purchase_short/?purchase_id=1432    ${BROWSER}
    Maximize Browser Window
    Wait Until Page Contains    Logowanie
    Loguj User
  
    Click Element    xpath=//a[starts-with(text(),'Moduły')]
    Wait Until Element Is Visible    xpath=//a[contains(text(),'Umowy')]   
    Click Element    xpath=//a[starts-with(text(),'Umowy')]
    Wait Until Element Is Visible    //a[@class='nav-link dropdown-toggle' and contains(text(),'Uzupełnij')]    timeout=10s
    Mouse Over    xpath=//a[contains(text(),'Uzupełnij')]
    Click Element      //a[@class='nav-link dropdown-toggle' and contains(text(),'Uzupełnij')]


    Wait Until Element Is Visible    xpath=//a[contains(text(),'Czy obsługiwana')]
    Mouse Over    xpath=//a[contains(text(),'Czy obsługiwana')]
    Wait Until Element Is Visible    //li/a[@class='dropdown-item' and @href='/contracts/czyobslugiwane' and contains(text(),'Wszystkie działy')]    timeout=10s
    Click Element      //li/a[@class='dropdown-item' and @href='/contracts/czyobslugiwane' and contains(text(),'Wszystkie działy')]  
   
    Wait Until Element Is Visible    //a[contains(@href, 'edit_contract_short/?contract_id=')]    timeout=10s
    
    # Znajdź pierwszy element odpowiadający kryteriom i zapisz jego href
    ${contract_element}=    Get WebElement    //a[contains(@href, 'edit_contract_short/?contract_id=')]
    ${href}=    Get Element Attribute    ${contract_element}    href

    # Wyciągnij numer kontraktu z href
    ${CONTRACT_NUMBER}=    Set Variable    ${href.split('=')[1]}
    Log    Numer kontraktu to: ${CONTRACT_NUMBER}
    Set Global Variable    ${CONTRACT_NUMBER}    ${CONTRACT_NUMBER}
    # Kliknij w link
    Click Element    ${contract_element}

    ${locator}=    Set Variable    //div[contains(., 'Umowa') and contains(., '${CONTRACT_NUMBER}')]
    Wait Until Element Is Visible    ${locator}    timeout=10s

        # Wybierz wartość "Nie" w kontrolce select
    Wait Until Element Is Visible    id=id_obslugiwana    timeout=10s
    Select From List By Value    id=id_obslugiwana    False

    # Możesz dodać tutaj dalsze kroki testowe

    Kliknij  Submit

    Przywolaj Umowe

       # Sprawdź, czy wybrana wartość jest równa "Nie"
    ${selected_value}=    Get Selected List Value    id=id_obslugiwana
    Should Be Equal    ${selected_value}    False

 
