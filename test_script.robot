*** Settings ***
Library    SeleniumLibrary

*** Variables ***
${BROWSER}        chrome
${URL}            https://avanticdev.gas.pgnig.pl

*** Test Cases ***
Security
    Open Browser    ${URL}    ${BROWSER}
    Maximize Browser Window
    Sleep    1s

    Open Browser    https://avanticdev.gas.pgnig.pl/contracts/edit_purchase_short/?purchase_id=1509    ${BROWSER}
    Maximize Browser Window
    Wait Until Page Contains    Logowanie
    Close Browser
    Open Browser    https://avanticdev.gas.pgnig.pl/contracts/edit_contract_short/?contract_id=14701    ${BROWSER}
    Maximize Browser Window
    Wait Until Page Contains    Logowanie
    Close Browser
    Open Browser    https://avanticdev.gas.pgnig.pl/contracts/edit_need_short/?need_id=2500    ${BROWSER}
    Maximize Browser Window
    Wait Until Page Contains    Logowanie
    Close Browser
    Open Browser    https://avanticdev.gas.pgnig.pl/contracts/edit_idea_short/?idea_id=2727    ${BROWSER}
    Maximize Browser Window
    Wait Until Page Contains    Logowanie
    Close Browser
    Open Browser    https://avanticdev.gas.pgnig.pl/contracts/cbu_import/    ${BROWSER}
    Maximize Browser Window
    Wait Until Page Contains    Logowanie
    Close Browser
    Open Browser    https://avanticdev.gas.pgnig.pl/contracts/ezzc_import/    ${BROWSER}
    Maximize Browser Window
    Wait Until Page Contains    Logowanie
    Close Browser
    Open Browser    https://avanticdev.gas.pgnig.pl/contracts/wszystkieumowyaktywne/edit_contract_short/?contract_id=14701    ${BROWSER}
    Maximize Browser Window
    Wait Until Page Contains    Logowanie
    Close Browser
    Open Browser    https://avanticdev.gas.pgnig.pl/contracts/wszystkieumowyaktywne/    ${BROWSER}
    Maximize Browser Window
    Wait Until Page Contains    Logowanie
    Close Browser
    Open Browser    https://avanticdev.gas.pgnig.pl/contracts/wszystkieumowy/edit_contract_short/?contract_id=14701    ${BROWSER}
    Maximize Browser Window
    Wait Until Page Contains    Logowanie
    Close Browser
    Open Browser    https://avanticdev.gas.pgnig.pl/contracts/wszystkieumowy/    ${BROWSER}
    Maximize Browser Window
    Wait Until Page Contains    Logowanie
    Close Browser
    Open Browser    https://avanticdev.gas.pgnig.pl/contracts/nieprzypisane/edit_contract_short/?contract_id=14701    ${BROWSER}
    Maximize Browser Window
    Wait Until Page Contains    Logowanie
    Close Browser
    Open Browser    https://avanticdev.gas.pgnig.pl/contracts/nieprzypisane/    ${BROWSER}
    Maximize Browser Window
    Wait Until Page Contains    Logowanie
    Close Browser
    Open Browser    https://avanticdev.gas.pgnig.pl/contracts/czyobslugiwane/edit_contract_short/?contract_id=14701    ${BROWSER}
    Maximize Browser Window
    Wait Until Page Contains    Logowanie
    Close Browser
    Open Browser    https://avanticdev.gas.pgnig.pl/contracts/czyobslugiwane/    ${BROWSER}
    Maximize Browser Window
    Wait Until Page Contains    Logowanie
    Close Browser
    Open Browser    https://avanticdev.gas.pgnig.pl/contracts/czykontynuowac/edit_contract_short/?contract_id=14701    ${BROWSER}
    Maximize Browser Window
    Wait Until Page Contains    Logowanie
    Close Browser
    Open Browser    https://avanticdev.gas.pgnig.pl/contracts/czykontynuowac/    ${BROWSER}
    Maximize Browser Window
    Wait Until Page Contains    Logowanie
    Close Browser
    Open Browser    https://avanticdev.gas.pgnig.pl/contracts/kiedykontynuowac/edit_contract_short/?contract_id=14701    ${BROWSER}
    Maximize Browser Window
    Wait Until Page Contains    Logowanie
    Close Browser
    Open Browser    https://avanticdev.gas.pgnig.pl/contracts/kiedykontynuowac/    ${BROWSER}
    Maximize Browser Window
    Wait Until Page Contains    Logowanie
    Close Browser
    Open Browser    https://avanticdev.gas.pgnig.pl/contracts/jakkontynuowac/edit_contract_short/?contract_id=14701    ${BROWSER}
    Maximize Browser Window
    Wait Until Page Contains    Logowanie
    Close Browser
    Open Browser    https://avanticdev.gas.pgnig.pl/contracts/jakkontynuowac/    ${BROWSER}
    Maximize Browser Window
    Wait Until Page Contains    Logowanie
    Close Browser
    Open Browser    https://avanticdev.gas.pgnig.pl/contracts/cbu_list/    ${BROWSER}
    Maximize Browser Window
    Wait Until Page Contains    Logowanie
    Close Browser
    Open Browser    https://avanticdev.gas.pgnig.pl/contracts/ezzc_list/    ${BROWSER}
    Maximize Browser Window
    Wait Until Page Contains    Logowanie
    Close Browser
    Open Browser    https://avanticdev.gas.pgnig.pl/contracts/ezzc_add/    ${BROWSER}
    Maximize Browser Window
    Wait Until Page Contains    Logowanie
    Close Browser
    Open Browser    https://avanticdev.gas.pgnig.pl/contracts/auto_contract/    ${BROWSER}
    Maximize Browser Window
    Wait Until Page Contains    Logowanie
    Close Browser
    Open Browser    https://avanticdev.gas.pgnig.pl/contracts/ostatniozmieniane/edit_contract_short/?contract_id=14701    ${BROWSER}
    Maximize Browser Window
    Wait Until Page Contains    Logowanie
    Close Browser
    Open Browser    https://avanticdev.gas.pgnig.pl/contracts/ostatniozmieniane/    ${BROWSER}
    Maximize Browser Window
    Wait Until Page Contains    Logowanie
    Close Browser
    Open Browser    https://avanticdev.gas.pgnig.pl/general/crip-list/    ${BROWSER}
    Maximize Browser Window
    Wait Until Page Contains    Logowanie
    Close Browser
    Open Browser    https://avanticdev.gas.pgnig.pl/general/crip-linked/    ${BROWSER}
    Maximize Browser Window
    Wait Until Page Contains    Logowanie
    Close Browser
    Open Browser    https://avanticdev.gas.pgnig.pl/general/crip-alone/    ${BROWSER}
    Maximize Browser Window
    Wait Until Page Contains    Logowanie
    Close Browser
    Open Browser    https://avanticdev.gas.pgnig.pl/general/edit_crip_short/?crip_id=12    ${BROWSER}
    Maximize Browser Window
    Wait Until Page Contains    Logowanie
    Close Browser
    Open Browser    https://avanticdev.gas.pgnig.pl/general/crip-list/edit_crip_short/?crip_id=12    ${BROWSER}
    Maximize Browser Window
    Wait Until Page Contains    Logowanie
    Close Browser
    Open Browser    https://avanticdev.gas.pgnig.pl/general/crip-linked/edit_crip_short/?crip_id=12    ${BROWSER}
    Maximize Browser Window
    Wait Until Page Contains    Logowanie
    Close Browser
    Open Browser    https://avanticdev.gas.pgnig.pl/general/crip-alone/edit_crip_short/?crip_id=12    ${BROWSER}
    Maximize Browser Window
    Wait Until Page Contains    Logowanie
    Close Browser
    Open Browser    https://avanticdev.gas.pgnig.pl/general/edit_crip_short_new/?crip_id=12    ${BROWSER}
    Maximize Browser Window
    Wait Until Page Contains    Logowanie
    Close Browser
    Open Browser    https://avanticdev.gas.pgnig.pl/general/full_search/    ${BROWSER}
    Maximize Browser Window
    Wait Until Page Contains    Logowanie
    Close Browser
    Open Browser    https://avanticdev.gas.pgnig.pl/general/edit_purchase_short/?purchase_id=1509    ${BROWSER}
    Maximize Browser Window
    Wait Until Page Contains    Logowanie
    Close Browser
    Open Browser    https://avanticdev.gas.pgnig.pl/general/edit_contract_short/?contract_id=14701    ${BROWSER}
    Maximize Browser Window
    Wait Until Page Contains    Logowanie
    Close Browser
    Open Browser    https://avanticdev.gas.pgnig.pl/general/edit_need_short/?need_id=2500    ${BROWSER}
    Maximize Browser Window
    Wait Until Page Contains    Logowanie
    Close Browser
    Open Browser    https://avanticdev.gas.pgnig.pl/general/edit_idea_short/?idea_id=2727    ${BROWSER}
    Maximize Browser Window
    Wait Until Page Contains    Logowanie
    Close Browser
    Open Browser    https://avanticdev.gas.pgnig.pl/general/auto_ezz/    ${BROWSER}
    Maximize Browser Window
    Wait Until Page Contains    Logowanie
    Close Browser
    Open Browser    https://avanticdev.gas.pgnig.pl/general/contracts/    ${BROWSER}
    Maximize Browser Window
    Wait Until Page Contains    Logowanie
    Close Browser
    Open Browser    https://avanticdev.gas.pgnig.pl/ideas/edit_purchase_short/?purchase_id=1509    ${BROWSER}
    Maximize Browser Window
    Wait Until Page Contains    Logowanie
    Close Browser
    Open Browser    https://avanticdev.gas.pgnig.pl/ideas/edit_contract_short/?contract_id=14701    ${BROWSER}
    Maximize Browser Window
    Wait Until Page Contains    Logowanie
    Close Browser
    Open Browser    https://avanticdev.gas.pgnig.pl/ideas/edit_need_short/?need_id=2500    ${BROWSER}
    Maximize Browser Window
    Wait Until Page Contains    Logowanie
    Close Browser
    Open Browser    https://avanticdev.gas.pgnig.pl/ideas/edit_idea_short/?idea_id=2727    ${BROWSER}
    Maximize Browser Window
    Wait Until Page Contains    Logowanie
    Close Browser
    Open Browser    https://avanticdev.gas.pgnig.pl/ideas/pomyslydoakceptacji/edit_idea_short/?idea_id=2727    ${BROWSER}
    Maximize Browser Window
    Wait Until Page Contains    Logowanie
    Close Browser
    Open Browser    https://avanticdev.gas.pgnig.pl/ideas/wszystkiepomysly/edit_idea_short/?idea_id=2727    ${BROWSER}
    Maximize Browser Window
    Wait Until Page Contains    Logowanie
    Close Browser
    Open Browser    https://avanticdev.gas.pgnig.pl/ideas/wszystkiepomysly/    ${BROWSER}
    Maximize Browser Window
    Wait Until Page Contains    Logowanie
    Close Browser
    Open Browser    https://avanticdev.gas.pgnig.pl/ideas/pomyslydoakceptacji/    ${BROWSER}
    Maximize Browser Window
    Wait Until Page Contains    Logowanie
    Close Browser
    Open Browser    https://avanticdev.gas.pgnig.pl/needs/potrzebydoakceptacjiinfra/edit_need_short/?need_id=2500    ${BROWSER}
    Maximize Browser Window
    Wait Until Page Contains    Logowanie
    Close Browser
    Open Browser    https://avanticdev.gas.pgnig.pl/needs/potrzebydoakceptacjiinfra/    ${BROWSER}
    Maximize Browser Window
    Wait Until Page Contains    Logowanie
    Close Browser
    Open Browser    https://avanticdev.gas.pgnig.pl/needs/potrzebydoakceptacjiuslugi/edit_need_short/?need_id=2500    ${BROWSER}
    Maximize Browser Window
    Wait Until Page Contains    Logowanie
    Close Browser
    Open Browser    https://avanticdev.gas.pgnig.pl/needs/potrzebydoakceptacjiuslugi/    ${BROWSER}
    Maximize Browser Window
    Wait Until Page Contains    Logowanie
    Close Browser
    Open Browser    https://avanticdev.gas.pgnig.pl/needs/potrzebydoakceptacjisiec/edit_need_short/?need_id=2500    ${BROWSER}
    Maximize Browser Window
    Wait Until Page Contains    Logowanie
    Close Browser
    Open Browser    https://avanticdev.gas.pgnig.pl/needs/potrzebydoakceptacjisiec/    ${BROWSER}
    Maximize Browser Window
    Wait Until Page Contains    Logowanie
    Close Browser
    Open Browser    https://avanticdev.gas.pgnig.pl/needs/potrzebydoakceptacjifinanse/edit_need_short/?need_id=2500    ${BROWSER}
    Maximize Browser Window
    Wait Until Page Contains    Logowanie
    Close Browser
    Open Browser    https://avanticdev.gas.pgnig.pl/needs/potrzebydoakceptacjifinanse/    ${BROWSER}
    Maximize Browser Window
    Wait Until Page Contains    Logowanie
    Close Browser
    Open Browser    https://avanticdev.gas.pgnig.pl/needs/potrzebydoakceptacji/edit_need_short/?need_id=2500    ${BROWSER}
    Maximize Browser Window
    Wait Until Page Contains    Logowanie
    Close Browser
    Open Browser    https://avanticdev.gas.pgnig.pl/needs/potrzebydoakceptacji/    ${BROWSER}
    Maximize Browser Window
    Wait Until Page Contains    Logowanie
    Close Browser
    Open Browser    https://avanticdev.gas.pgnig.pl/needs/edit_purchase_short/?purchase_id=1509    ${BROWSER}
    Maximize Browser Window
    Wait Until Page Contains    Logowanie
    Close Browser
    Open Browser    https://avanticdev.gas.pgnig.pl/needs/edit_contract_short/?contract_id=14701    ${BROWSER}
    Maximize Browser Window
    Wait Until Page Contains    Logowanie
    Close Browser
    Open Browser    https://avanticdev.gas.pgnig.pl/needs/edit_need_short/?need_id=2500    ${BROWSER}
    Maximize Browser Window
    Wait Until Page Contains    Logowanie
    Close Browser
    Open Browser    https://avanticdev.gas.pgnig.pl/needs/edit_idea_short/?idea_id=2727    ${BROWSER}
    Maximize Browser Window
    Wait Until Page Contains    Logowanie
    Close Browser
    Open Browser    https://avanticdev.gas.pgnig.pl/needs/wszystkiepotrzeby/edit_need_short/?need_id=2500    ${BROWSER}
    Maximize Browser Window
    Wait Until Page Contains    Logowanie
    Close Browser
    Open Browser    https://avanticdev.gas.pgnig.pl/needs/potrzebybezzakupow/edit_need_short/?need_id=2500    ${BROWSER}
    Maximize Browser Window
    Wait Until Page Contains    Logowanie
    Close Browser
    Open Browser    https://avanticdev.gas.pgnig.pl/needs/wszystkiepotrzeby/    ${BROWSER}
    Maximize Browser Window
    Wait Until Page Contains    Logowanie
    Close Browser
    Open Browser    https://avanticdev.gas.pgnig.pl/needs/potrzebybezzakupow/    ${BROWSER}
    Maximize Browser Window
    Wait Until Page Contains    Logowanie
    Close Browser
    Open Browser    https://avanticdev.gas.pgnig.pl/needs/potrzebydozamkniecia/    ${BROWSER}
    Maximize Browser Window
    Wait Until Page Contains    Logowanie
    Close Browser
    Open Browser    https://avanticdev.gas.pgnig.pl/needs/potrzebydozamkniecia/edit_need_short/?need_id=2500    ${BROWSER}
    Maximize Browser Window
    Wait Until Page Contains    Logowanie
    Close Browser
    Open Browser    https://avanticdev.gas.pgnig.pl/purchases/edit_purchase_short/?purchase_id=1509    ${BROWSER}
    Maximize Browser Window
    Wait Until Page Contains    Logowanie
    Close Browser
    Open Browser    https://avanticdev.gas.pgnig.pl/purchases/edit_contract_short/?contract_id=14701    ${BROWSER}
    Maximize Browser Window
    Wait Until Page Contains    Logowanie
    Close Browser
    Open Browser    https://avanticdev.gas.pgnig.pl/purchases/edit_need_short/?need_id=2500    ${BROWSER}
    Maximize Browser Window
    Wait Until Page Contains    Logowanie
    Close Browser
    Open Browser    https://avanticdev.gas.pgnig.pl/purchases/edit_idea_short/?idea_id=2727    ${BROWSER}
    Maximize Browser Window
    Wait Until Page Contains    Logowanie
    Close Browser
    Open Browser    https://avanticdev.gas.pgnig.pl/purchases/zakupydoakceptacji/edit_purchase_short/?purchase_id=1509    ${BROWSER}
    Maximize Browser Window
    Wait Until Page Contains    Logowanie
    Close Browser
    Open Browser    https://avanticdev.gas.pgnig.pl/purchases/wszystkiezakupy/edit_purchase_short/?purchase_id=1509    ${BROWSER}
    Maximize Browser Window
    Wait Until Page Contains    Logowanie
    Close Browser
    Open Browser    https://avanticdev.gas.pgnig.pl/purchases/zakupy_roboczy/edit_purchase_short/?purchase_id=1509    ${BROWSER}
    Maximize Browser Window
    Wait Until Page Contains    Logowanie
    Close Browser
    Open Browser    https://avanticdev.gas.pgnig.pl/purchases/zakupy_ezz/edit_purchase_short/?purchase_id=1509    ${BROWSER}
    Maximize Browser Window
    Wait Until Page Contains    Logowanie
    Close Browser
    Open Browser    https://avanticdev.gas.pgnig.pl/purchases/zakupy_zakupy/edit_purchase_short/?purchase_id=1509    ${BROWSER}
    Maximize Browser Window
    Wait Until Page Contains    Logowanie
    Close Browser
    Open Browser    https://avanticdev.gas.pgnig.pl/purchases/zakupy_bgnig/edit_purchase_short/?purchase_id=1509    ${BROWSER}
    Maximize Browser Window
    Wait Until Page Contains    Logowanie
    Close Browser
    Open Browser    https://avanticdev.gas.pgnig.pl/purchases/zakupy_realizacja/edit_purchase_short/?purchase_id=1509    ${BROWSER}
    Maximize Browser Window
    Wait Until Page Contains    Logowanie
    Close Browser
    Open Browser    https://avanticdev.gas.pgnig.pl/purchases/wszystkiezakupy/    ${BROWSER}
    Maximize Browser Window
    Wait Until Page Contains    Logowanie
    Close Browser
    Open Browser    https://avanticdev.gas.pgnig.pl/purchases/zakupydoakceptacji/    ${BROWSER}
    Maximize Browser Window
    Wait Until Page Contains    Logowanie
    Close Browser
    Open Browser    https://avanticdev.gas.pgnig.pl/purchases/ezz/import    ${BROWSER}
    Maximize Browser Window
    Wait Until Page Contains    Logowanie
    Close Browser
    Open Browser    https://avanticdev.gas.pgnig.pl/purchases/ezz/import_postepowan    ${BROWSER}
    Maximize Browser Window
    Wait Until Page Contains    Logowanie
    Close Browser
    Open Browser    https://avanticdev.gas.pgnig.pl/purchases/ezz/    ${BROWSER}
    Maximize Browser Window
    Wait Until Page Contains    Logowanie
    Close Browser
    Open Browser    https://avanticdev.gas.pgnig.pl/purchases/ezz-illegal/    ${BROWSER}
    Maximize Browser Window
    Wait Until Page Contains    Logowanie
    Close Browser
    Open Browser    https://avanticdev.gas.pgnig.pl/purchases/postepowania_list/    ${BROWSER}
    Maximize Browser Window
    Wait Until Page Contains    Logowanie
    Close Browser
    Open Browser    https://avanticdev.gas.pgnig.pl/purchases/crip_import/    ${BROWSER}
    Maximize Browser Window
    Wait Until Page Contains    Logowanie
    Close Browser
    Open Browser    https://avanticdev.gas.pgnig.pl/purchases/zakupy_roboczy/    ${BROWSER}
    Maximize Browser Window
    Wait Until Page Contains    Logowanie
    Close Browser
    Open Browser    https://avanticdev.gas.pgnig.pl/purchases/zakupy_ezz/    ${BROWSER}
    Maximize Browser Window
    Wait Until Page Contains    Logowanie
    Close Browser
    Open Browser    https://avanticdev.gas.pgnig.pl/purchases/zakupy_zakupy/    ${BROWSER}
    Maximize Browser Window
    Wait Until Page Contains    Logowanie
    Close Browser
    Open Browser    https://avanticdev.gas.pgnig.pl/purchases/zakupy_bgnig/    ${BROWSER}
    Maximize Browser Window
    Wait Until Page Contains    Logowanie
    Close Browser
    Open Browser    https://avanticdev.gas.pgnig.pl/purchases/zakupy_realizacja/    ${BROWSER}
    Maximize Browser Window
    Wait Until Page Contains    Logowanie
    Close Browser
    Open Browser    https://avanticdev.gas.pgnig.pl/purchases/unlinked_ezz/    ${BROWSER}
    Maximize Browser Window
    Wait Until Page Contains    Logowanie
    Close Browser
    Open Browser    https://avanticdev.gas.pgnig.pl/general/    ${BROWSER}
    Maximize Browser Window
    Wait Until Page Contains    Logowanie
    Close Browser
    Open Browser    https://avanticdev.gas.pgnig.pl/purchases/    ${BROWSER}
    Maximize Browser Window
    Wait Until Page Contains    Logowanie
    Close Browser
    Open Browser    https://avanticdev.gas.pgnig.pl/contracts/    ${BROWSER}
    Maximize Browser Window
    Wait Until Page Contains    Logowanie
    Close Browser
    Open Browser    https://avanticdev.gas.pgnig.pl/needs/    ${BROWSER}
    Maximize Browser Window
    Wait Until Page Contains    Logowanie
    Close Browser
    Open Browser    https://avanticdev.gas.pgnig.pl/ideas/    ${BROWSER}
    Maximize Browser Window
    Wait Until Page Contains    Logowanie
    Close Browser
    Open Browser    https://avanticdev.gas.pgnig.pl/edit_purchase_short/?purchase_id=1509    ${BROWSER}
    Maximize Browser Window
    Wait Until Page Contains    Logowanie
    Close Browser
    Open Browser    https://avanticdev.gas.pgnig.pl/edit_contract_short/?contract_id=14701    ${BROWSER}
    Maximize Browser Window
    Wait Until Page Contains    Logowanie
    Close Browser
    Open Browser    https://avanticdev.gas.pgnig.pl/edit_need_short/?need_id=2500    ${BROWSER}
    Maximize Browser Window
    Wait Until Page Contains    Logowanie
    Close Browser
    Open Browser    https://avanticdev.gas.pgnig.pl/edit_idea_short/?idea_id=2727    ${BROWSER}
    Maximize Browser Window
    Wait Until Page Contains    Logowanie
    Close Browser
