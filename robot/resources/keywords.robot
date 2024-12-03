*** Settings ***
Library           SeleniumLibrary

*** Keywords ***
Login User
    Click Element    xpath=//a[text()='Konto']
    Wait Until Element Is Visible    xpath=//a[text()='Zaloguj']    10s
    Click Element    xpath=//a[text()='Zaloguj']
    Wait Until Page Contains Element    id=id_username    10s
    Input Text    id=id_username    ${USER_USER}
    Input Text    id=id_password    ${PASS_USER}
    Click Button    xpath=//input[@type='submit' and @value='Zaloguj']
    Wait Until Page Contains Element    xpath=//a[@class='nav-link' and contains(text(),'user')]    10s


Logout
    Click Element    xpath=//a[text()='Konto']
    # Wait Until Element Is Visible    xpath=//a[text()='wyloguj']    10s
    # Click Element    xpath=//a[text()='wyloguj']
    Wait Until Element Is Visible    xpath=//a[starts-with(text(),'wyloguj')]
    Click Element    xpath=//a[starts-with(text(),'wyloguj')]
    Click Element    xpath=//a[text()='Konto']
    Wait Until Element Is Visible    xpath=//a[text()='Zaloguj']    10s 




Select Continuity Of Services
    Click Element    xpath=//a[contains(text(),'Ciągłość serwisów')]
    Wait Until Element Is Visible    xpath=//a[contains(text(),'Ciągłość usług')]
    Mouse Over    xpath=//a[contains(text(),'Ciągłość usług')]
    Wait Until Element Is Visible    xpath=//a[contains(text(),'Wszystkie działy')]
    Click Element    xpath=//a[contains(text(),'Wszystkie działy')]
    Wait Until Element Is Visible    xpath=//div[contains(@class, 'continous-header') and contains(text(), 'Umowy wymagające kontynuacji')]
    Element Should Be Visible    xpath=//div[contains(@class, 'continous-header') and contains(text(), 'Umowy wymagające kontynuacji')]

Switch to Pomysly
    Click Element    xpath=//a[text()='Moduły']
    Wait Until Element Is Visible    xpath=//a[starts-with(text(),'Pomysły')]    
    Click Element    xpath=//a[starts-with(text(),'Pomysły')]
    Wait Until Element Is Visible    xpath=//a[contains(text(),'Nowy pomysł')] 
    Click Element    xpath=//a[contains(text(),'Nowy pomysł')]
    Handle Alert
    Wait Until Element Is Visible    xpath=//div[contains(@style,'background-color: gray') and contains(@style,'color: red') and contains(text(),'status pomysłu: nowa')]    10s
    Set Priority to High
    Set Initiative Field    id_subject    Człowiek cieszy się życiem, kiedy ma swoje miejsce, kiedy wie, gdzie jest jego miejsce w porządku wszechrzeczy
    Set Initiative Field    id_opis    Kiedy usiłujemy ukryć nasze najskrytsze uczucia, zdradzamy się całym sobą. 
    Set Initiative Field    id_produkty    Czym gardzisz? Po tym poznać, kim jesteś naprawdę. 
    Set Initiative Field    id_komentarz    Kiedy usiłujemy ukryć nasze najskrytsze uczucia, zdradzamy się całym sobą. 
    Set Initiative Field    id_uzasadnienie    Bogactwo to narzędzie wolności, ale pogoń za nim to droga do niewolnictwa. 
    Set Initiative Field    id_wlasciciel_biznesowy   Jan z Kolna
    Set Initiative Field    id_osoba_kontakowa_u_klienta    Erazm z Roterdamu
    Select From List By Label   id=id_proponowany_sposob_realizacji      Zakup od Spółek (§ 25)
    Select From List By Label   id=id_rodzaj_inicjatywy   nowa
    Select From List By Label   id=id_client    Oddział Zielona Góra
    Set Number Field    id_orientacynjy_budzet    1010000
    Set Date Field    id_wymagana_data_realizacji    09-09-2025
    Click Button And Accept Alert    xpath=//button[@name='zawies']
    Wait Until Element Is Visible    xpath=//div[contains(text(),'status pomysłu: zawieszona')]    20s
    Save Idea Number
    Log    Pomysł numer: ${IDEA_NUMBER}  

Use Saved Idea Number
    [Documentation]    Wykorzystanie zapisanego numeru pomysłu
    Log    Wykorzystanie numeru pomysłu: ${IDEA_NUMBER}
    # Dalsze kroki używające ${IDEA_NUMBER}...


Handle AlertHandle Alert
    ${alert}=    Get Alert Message
    Log    Alert message: ${alert}
    Accept AlertHandle Alert
    ${alert}=    Get Alert Message
    Log    Alert message: ${alert}
    Accept Alert

Set Priority to High
    Wait Until Element Is Visible    id=id_priorytet    10s
    Select From List By Label    id=id_priorytet    wysoki


Set Initiative Field
    [Arguments]    ${field_id}    ${field_text}
    Wait Until Element Is Visible    id=${field_id}    10s
    Input Text    id=${field_id}    ${field_text}


Set Number Field
    [Arguments]    ${field_id}    ${value}
    Wait Until Element Is Visible    id=${field_id}    10s
    Input Text    id=${field_id}    ${value}

Set Date Field
    [Arguments]    ${field_id}    ${date}
    Wait Until Element Is Visible    id=${field_id}    10s
    Input Text    id=${field_id}    ${date}

Click Button And Accept Alert
    [Arguments]    ${button_xpath}
    Wait Until Element Is Visible    ${button_xpath}    10s
    Click Button    ${button_xpath}
    Handle Alert

Click Button
    [Arguments]    ${button_xpath}
    Wait Until Element Is Visible    ${button_xpath}    10s
    Click Button    ${button_xpath}


Save Idea Number
    [Documentation]    Save the generated idea number for later use
    ${idea_text}=    Get Text    xpath=//div[@id='pomysl']
    ${IDEA_NUMBER}=    Set Variable    ${idea_text.split("pomysł")[1].split("</b>")[0].strip()}
    Set Global Variable    ${IDEA_NUMBER}    ${IDEA_NUMBER}

