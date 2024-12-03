*** Settings ***
Library     SeleniumLibrary
Library     String
Library     Collections
Library     BuiltIn

*** Keywords ***

Kliknij checkbox
    [Arguments]    ${checkbox_id}
    Wait Until Element Is Visible    id=${checkbox_id}    10s
    Scroll Element Into View    id=${checkbox_id}
    Click Element    id=${checkbox_id}

Wybierz wedlug etykiet
    [Arguments]    ${element_id}    ${label}
    Wait Until Element Is Visible    id=${element_id}    10s
    Scroll Element Into View    id=${element_id}
    Select From List By Label    id=${element_id}    ${label}

Wprowadz tekst   
    [Arguments]    ${element_id}    ${tekst}
    Wait Until Element Is Visible    id=${element_id}    10s
    Scroll Element Into View    id=${element_id}
    Input Text   id=${element_id}    ${tekst}    

Wybierz wedlug pozycji
    [Arguments]    ${element_id}    ${num}   
    Wait Until Element Is Visible    ${element_id}       10s
    Scroll Element Into View     ${element_id}
    Select From List By Index       ${element_id}     ${num}   
    

Wprowadź Wartość Do Select2
    [Arguments]    ${select_id}    ${input_value}
    
    # Poczekaj, aż element Select2 będzie widoczny i przewiń do niego
    Wait Until Element Is Visible    xpath=//select[@id="${select_id}"]    10s
    Scroll Element Into View    xpath=//select[@id="${select_id}"]
    Execute JavaScript    window.scrollBy(0, 200)
    
    # Otwórz Select2, upewniając się, że otwieramy właściwy komponent
    Execute JavaScript    document.querySelector('#${select_id}').nextElementSibling.querySelector('.select2-selection').click()
    Sleep    0.2s

    # Poczekaj na widoczność pola wyszukiwania Select2 dla danego `select_id`
    Wait Until Element Is Visible    xpath=//select[@id="${select_id}"]/following-sibling::span//input[contains(@class, 'select2-search__field')]    10s
    
    # Wprowadź wartość do pola wyszukiwania
    Input Text    xpath=//select[@id="${select_id}"]/following-sibling::span//input[contains(@class, 'select2-search__field')]    ${input_value}
    Sleep    0.2s  # Zwłoka na załadowanie wyników wyszukiwania

    # Zatwierdź wybór naciskając ENTER
    Press Keys    xpath=//select[@id="${select_id}"]/following-sibling::span//input[contains(@class, 'select2-search__field')]    ENTER
    Sleep    0.2s  # Zwłoka po zatwierdzeniu wyboru

    # Zamknij Select2
    Execute JavaScript    document.querySelector('#${select_id}').nextElementSibling.querySelector('.select2-selection').click()

 # Wyraźnie zamknij listę Select2 po wyborze
    Execute JavaScript    $("#${select_id}").select2('close')
    Sleep    0.2s  # Zwłoka, aby zapewnić zamknięcie listy przed przejściem do kolejnego elementu

Verify Option In Select Element
    [Arguments]    ${select_id}    ${expected_option}
    ${options}=    Get WebElements    xpath=//select[@id='${select_id}']/option
    ${found}=    Set Variable    ${False}
    FOR    ${option}    IN    @{options}
        ${text}=    Get Text    ${option}
        ${text}=    Strip String    ${text}   # Usuwa dodatkowe białe znaki z początku i końca
        ${expected_option}=    Strip String    ${expected_option}   # Usuwa dodatkowe białe znaki z początku i końca
        ${is_match}=    Run Keyword And Return Status    Should Be Equal    ${text}    ${expected_option}
        ${found}=    Set Variable If    ${is_match}    ${True}    ${found}
    END
    Run Keyword If    '${found}' == 'False'    Fail    Expected option '${expected_option}' not found in select element with id '${select_id}'





