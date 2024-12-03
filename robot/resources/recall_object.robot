*** Settings ***
Library     SeleniumLibrary
Library     String
Library     Collections
Library     BuiltIn

*** Keywords ***

Przywolaj potrzebe

    Wait Until Element Is Visible      xpath=//a[starts-with(text(),'Moduły')]    10s
    Click Element    xpath=//a[starts-with(text(),'Moduły')]
    Wait Until Element Is Visible        xpath=//a[starts-with(text(),'Potrzeby')]   10s
    Click Element    xpath=//a[starts-with(text(),'Potrzeby')]
  #  Wait Until Element Is Visible    xpath=//a[contains(text(),'Nowy pomysł')]     10s
    
    Wait Until Element Is Visible    xpath=//a[contains(@class, 'nav-link dropdown-toggle') and contains(text(), 'Potrzeby')]    10s
    Click Element    xpath=//a[contains(@class, 'nav-link dropdown-toggle') and contains(text(), 'Potrzeby')]

    Wait Until Element Is Visible    xpath=//a[@class='dropdown-item' and contains(text(),'Wszystkie potrzeby')]    10s
    Click Element    xpath=//a[@class='dropdown-item' and contains(text(),'Wszystkie potrzeby')]

     # Wprowadzenie zapamiętanego numeru potrzeby w pole tekstowe
    Wait Until Element Is Visible    id=id_id    10s
    Input Text    id=id_id    ${NEED_NUMBER}
    # Kliknięcie przycisku Filtruj
    Wait Until Element Is Visible    xpath=//button[contains(@class, 'btn btn-primary') and text()='Filtruj']    10s
    Click Button    xpath=//button[contains(@class, 'btn btn-primary') and text()='Filtruj']
    # Kliknięcie na link do edycji pomysłu zawierający zapamiętany numer
    ${edit_link_xpath}=    Set Variable    //a[contains(@href, 'edit_need_short/?need_id=${NEED_NUMBER}')]
    Wait Until Element Is Visible    ${edit_link_xpath}    10s
    Click Element    ${edit_link_xpath} 
    Wait Until Element Is Visible    xpath=//div[contains(text(), 'Potrzeba')]


Przywolaj pomysl
   Click Element    xpath=//a[starts-with(text(),'Moduły')]
    Click Element    xpath=//a[starts-with(text(),'Pomysły')]
   # Wait Until Element Is Visible    xpath=//a[contains(text(),'Nowy pomysł')] 
    
    Wait Until Element Is Visible    xpath=//a[contains(@class, 'nav-link dropdown-toggle') and contains(text(), 'Pomysły')]    10s
    Click Element    xpath=//a[contains(@class, 'nav-link dropdown-toggle') and contains(text(), 'Pomysły')]

    Wait Until Element Is Visible    xpath=//a[@class='dropdown-item' and contains(text(),'Wszystkie pomysły')]    10s
    Click Element    xpath=//a[@class='dropdown-item' and contains(text(),'Wszystkie pomysły')]

     # Wprowadzenie zapamiętanego numeru pomysłu w pole tekstowe
    Wait Until Element Is Visible    id=id_id    10s
    Input Text    id=id_id    ${IDEA_NUMBER}
    # Kliknięcie przycisku Filtruj
    Wait Until Element Is Visible    xpath=//button[contains(@class, 'btn btn-primary') and text()='Filtruj']    10s
    Click Button    xpath=//button[contains(@class, 'btn btn-primary') and text()='Filtruj']
    # Kliknięcie na link do edycji pomysłu zawierający zapamiętany numer
    ${edit_link_xpath}=    Set Variable    //a[contains(@href, 'edit_idea_short/?idea_id=${IDEA_NUMBER}')]
    Wait Until Element Is Visible    ${edit_link_xpath}    10s
    Click Element    ${edit_link_xpath}      
    Wait Until Element Is Visible    xpath=//div[contains(text(), 'pomysł')]


Przywolaj Zakup
   Click Element    xpath=//a[starts-with(text(),'Moduły')]
    Click Element    xpath=//a[starts-with(text(),'Zakupy')]
   # Wait Until Element Is Visible    xpath=//a[contains(text(),'Nowy pomysł')] 
    
    Wait Until Element Is Visible    xpath=//a[contains(@class, 'nav-link dropdown-toggle') and contains(text(), 'Zakupy')]    10s
    Click Element    xpath=//a[contains(@class, 'nav-link dropdown-toggle') and contains(text(), 'Zakupy')]

    Wait Until Element Is Visible    xpath=//a[@class='dropdown-item' and contains(text(),'Wszystkie zakupy')]    10s
    Click Element    xpath=//a[@class='dropdown-item' and contains(text(),'Wszystkie zakupy')]

     # Wprowadzenie zapamiętanego numeru pomysłu w pole tekstowe
    Wait Until Element Is Visible    id=id_id    10s
    Input Text    id=id_id    ${PURCHASE_NUMBER}
    # Kliknięcie przycisku Filtruj
    Wait Until Element Is Visible    xpath=//button[contains(@class, 'btn btn-primary') and text()='Filtruj']    10s
    Click Button    xpath=//button[contains(@class, 'btn btn-primary') and text()='Filtruj']
    # Kliknięcie na link do edycji pomysłu zawierający zapamiętany numer
    ${edit_link_xpath}=    Set Variable    //a[contains(@href, 'edit_purchase_short/?purchase_id=${PURCHASE_NUMBER}')]
    Wait Until Element Is Visible    ${edit_link_xpath}    10s
    Click Element    ${edit_link_xpath}      
    Wait Until Element Is Visible    xpath=//div[contains(text(), 'Zakup')]


Przywolaj Umowe
   Click Element    xpath=//a[starts-with(text(),'Moduły')]
    Click Element    xpath=//a[starts-with(text(),'Umowy')]
   # Wait Until Element Is Visible    xpath=//a[contains(text(),'Nowy pomysł')] 
    
    Wait Until Element Is Visible    xpath=//a[contains(@class, 'nav-link dropdown-toggle') and contains(text(), 'Umowy')]    10s
    Click Element    xpath=//a[contains(@class, 'nav-link dropdown-toggle') and contains(text(), 'Umowy')]

    Wait Until Element Is Visible    xpath=//a[@class='dropdown-item' and contains(text(),'Wszystkie umowy')]    10s
    Click Element    xpath=//a[@class='dropdown-item' and contains(text(),'Wszystkie umowy')]

     # Wprowadzenie zapamiętanego numeru pomysłu w pole tekstowe
    Wait Until Element Is Visible    id=id_id    10s
    Input Text    id=id_id    ${CONTRACT_NUMBER}
    # Kliknięcie przycisku Filtruj
    Wait Until Element Is Visible    xpath=//button[contains(@class, 'btn btn-primary') and text()='Filtruj']    10s
    Click Button    xpath=//button[contains(@class, 'btn btn-primary') and text()='Filtruj']
    # Kliknięcie na link do edycji pomysłu zawierający zapamiętany numer
    ${edit_link_xpath}=    Set Variable    //a[contains(@href, 'edit_contract_short/?contract_id=${CONTRACT_NUMBER}')]
    Wait Until Element Is Visible    ${edit_link_xpath}    10s
    Click Element    ${edit_link_xpath}      
    Wait Until Element Is Visible    xpath=//div[contains(text(), 'Umowa')]


Save Idea Number
    [Documentation]    Save the generated idea number for later use
 #   Wait Until Element Is Visible       xpath=//div[@id='pomysl']  10s
   Wait Until Element Is Visible    xpath://div[contains(text(), 'Pomysł')]    10s
    # Get the inner HTML of the element containing "Potrzeba"
    ${element_text}=    Get Element Attribute    xpath://div[contains(text(), 'Pomysł')]    innerHTML
    Log    Pełna zawartość elementu: ${element_text}
    
    # Split the text using ">" as the separator and log the parts
    ${parts}=    Split String    ${element_text}    >
    Log    Wynik pierwszego podziału: ${parts}
    # Select the second part and log it
    ${second_part}=    Set Variable    ${parts}[1]
    Log    Drugi człon po pierwszym ">": ${second_part}
    
    # Split the second part using "<" as the separator and log the parts
    ${number_parts}=    Split String    ${second_part}    <
    Log    Wynik drugiego podziału: ${number_parts}
    
    # Extract the number and log it
    ${number}=    Set Variable    ${number_parts}[0]
    Log    Wyodrębniona liczba między znacznikami <b>: ${number}
    
    # Set the extracted number as a global variable
    Set Global Variable    ${IDEA_NUMBER}    ${number}
    Log    Ustawiono zmienną globalną NEED_NUMBER: ${IDEA_NUMBER}


    # ${idea_text}=    Get Text    xpath=//div[@id='pomysl']
    # ${IDEA_NUMBER}=    Set Variable    ${idea_text.split("pomysł")[1].split("</b>")[0].replace("|", "").strip()}
    # Set Global Variable    ${IDEA_NUMBER}    ${IDEA_NUMBER}

Save Need Number
    [Documentation]    Save the generated need number for later use
    # Wait until the element containing "Potrzeba" is visible
    Wait Until Element Is Visible    xpath://div[contains(text(), 'Potrzeba')]    10s
    
    # Get the inner HTML of the element containing "Potrzeba"
    ${element_text}=    Get Element Attribute    xpath://div[contains(text(), 'Potrzeba')]    innerHTML
    Log    Pełna zawartość elementu: ${element_text}
    
    # Split the text using ">" as the separator and log the parts
    ${parts}=    Split String    ${element_text}    >
    Log    Wynik pierwszego podziału: ${parts}
    
    # Select the second part and log it
    ${second_part}=    Set Variable    ${parts}[3]
    Log    Drugi człon po pierwszym ">": ${second_part}
    
    # Split the second part using "<" as the separator and log the parts
    ${number_parts}=    Split String    ${second_part}    <
    Log    Wynik drugiego podziału: ${number_parts}
    
    # Extract the number and log it
    ${number}=    Set Variable    ${number_parts}[0]
    Log    Wyodrębniona liczba między znacznikami <b>: ${number}
    
    # Set the extracted number as a global variable
    Set Global Variable    ${NEED_NUMBER}    ${number}
    Log    Ustawiono zmienną globalną NEED_NUMBER: ${NEED_NUMBER}






Save Purchase Number
    [Documentation]    Save the generated need number for later use
    # Wait until the element containing "Potrzeba" is visible
    Wait Until Element Is Visible    xpath://div[contains(text(), 'Potrzeba')]    10s
    
    # Get the inner HTML of the element containing "Potrzeba"
    ${element_text}=    Get Element Attribute    xpath://div[contains(text(), 'Potrzeba')]    innerHTML
    Log    Pełna zawartość elementu: ${element_text}
    
    # Split the text using ">" as the separator and log the parts
    ${parts}=    Split String    ${element_text}    >
    Log    Wynik pierwszego podziału: ${parts}
    
    # Select the second part and log it
    ${second_part}=    Set Variable    ${parts}[5]
    Log    Drugi człon po pierwszym ">": ${second_part}
    
    # Split the second part using "<" as the separator and log the parts
    ${number_parts}=    Split String    ${second_part}    <
    Log    Wynik drugiego podziału: ${number_parts}
    
    # Extract the number and log it
    ${number}=    Set Variable    ${number_parts}[0]
    Log    Wyodrębniona liczba między znacznikami <b>: ${number}
    
    # Set the extracted number as a global variable
    Set Global Variable    ${PURCHASE_NUMBER}    ${number}
    Log    Ustawiono zmienną globalną PURCHASE_NUMBER: ${PURCHASE_NUMBER}



    # Wait Until Element Is Visible     xpath=//a[contains(@href, '/purchases/wszystkiezakupy/edit_purchase_short/?purchase_id=')]    10s
    # ${element}=    Get Element Attribute    xpath=//a[contains(@href, '/purchases/wszystkiezakupy/edit_purchase_short/?purchase_id=')]    href
    # ${PURCHASE_NUMBER}=    Evaluate    ${element.split('=')[1].split('&')[0]}
    # Set Global Variable    ${PURCHASE_NUMBER}    ${PURCHASE_NUMBER}

Nowy pomysl z reki
    Click Element    xpath=//a[text()='Moduły']
    Wait Until Element Is Visible    xpath=//a[starts-with(text(),'Pomysły')]  10s
    Click Element    xpath=//a[starts-with(text(),'Pomysły')]
    Wait Until Element Is Visible    xpath=//a[contains(text(),'Nowy pomysł')]   10s
    Click Element    xpath=//a[contains(text(),'Nowy pomysł')]
    Handle Alert
    Wait Until Page Contains    nowa    10s
     
 #   Wait Until Element Is Visible    xpath=//div[contains(@style,'background-color: gray') and contains(@style,'color: red') and contains(text(),'nowa')]    10s


Save Meeting Number
    # Oczekujemy na element z numerem Rady Architektury
    Wait Until Page Contains Element    xpath=//div[text()='Rada Architektury:']/following-sibling::div[1]
    ${content}=    Get Text    xpath=//div[text()='Rada Architektury:']/following-sibling::div[1]
    Log    Next Div Content: ${content}
    ${parts}=    Split String    ${content}    -    # Podziel na części, używając " - " jako separatora
    ${numer_rady}=    Strip String    ${parts[0]}    # Usuń spacje z numeru rady
    Set Global Variable    ${numer_rady}    ${numer_rady}    # Zapisz do globalnej zmiennej
    # Wyświetlamy numer rady dla weryfikacji
    Log    Numer Rady Architektury: ${numer_rady}

Przywolaj rade
    Wait Until Element Is Visible    xpath=//a[@class="nav-link dropdown-toggle" and contains(text(), 'Obsługa Rady Architektury')]    10s
    Mouse Over    xpath=//a[@class="nav-link dropdown-toggle" and contains(text(), 'Obsługa Rady Architektury')]
    Click Element    xpath=//a[@class="nav-link dropdown-toggle" and contains(text(), 'Obsługa Rady Architektury')]

    Wait Until Element Is Visible    xpath=//a[contains(text(), 'Lista posiedzeń')]    10s
    Click Element    xpath=//a[contains(text(), 'Lista posiedzeń')]
    Wait Until Element Is Visible    xpath=//a[contains(text(), 'ID')]    10s   
        # Tworzymy dynamiczny XPath z numerem Rady
    ${xpath_rada}=    Set Variable    //a[contains(@href, '/general/edit_rada/') and contains(@href, '${numer_rady}')]
    Log    odnosnik: ${xpath_rada}
    # Oczekujemy, aż link będzie widoczny
    Wait Until Element Is Visible    ${xpath_rada}    10s

    # Klikamy w link
    Click Element    ${xpath_rada}  