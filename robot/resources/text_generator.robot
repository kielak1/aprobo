*** Settings ***
Library    BuiltIn
Library    String

*** Keywords ***
Generate Text
    [Arguments]    ${length}
    ${base_text}=    Set Variable    My, Naród Polski – wszyscy obywatele Rzeczypospolitej, zarówno wierzący w Boga będącego źródłem prawdy, sprawiedliwości, dobra i piękna, jak i nie podzielający tej wiary, a te uniwersalne wartości wywodzący z innych źródeł, równi w prawach i w powinnościach wobec dobra wspólnego – Polski, wdzięczni naszym przodkom za ich pracę, za walkę o niepodległość okupioną ogromnymi ofiarami, za kulturę zakorzenioną w chrześcijańskim dziedzictwie Narodu i ogólnoludzkich wartościach, ...
    ${multiplier}=    Evaluate    ${length} // len("${base_text}")
    ${text}=    Evaluate    "${base_text}" * ${multiplier}
    
    # Oblicz brakującą długość, którą należy dodać
    ${remaining_length}=    Evaluate    ${length} - len("${text}")
    ${remaining_text}=    Get Substring    ${base_text}    0    ${remaining_length}
    
    # Połącz pełny tekst
    ${text}=    Set Variable    ${text}${remaining_text}
    RETURN    ${text}
