#!/bin/bash

# Główna zmienna URL
BASE_URL="https://avanticdev.gas.pgnig.pl"

# Plik do którego będziemy zapisywać skrypt testujący
OUTPUT_FILE="test_script.robot"

# Funkcja do wyciągania ścieżek URL z pliku urls.py
extract_urls() {
    grep -oP "path\(\s*['\"]([^'\"]+)['\"]" "$1" | grep -oP "(?<=\()['\"][^'\"]+['\"]" | sed "s/[\'\"]//g"
}

# Rozpocznij pisanie skryptu testującego
echo "*** Settings ***
Library    SeleniumLibrary

*** Variables ***
\${BROWSER}        chrome
\${URL}            $BASE_URL
" > "$OUTPUT_FILE"

echo "*** Test Cases ***
Security
    Open Browser    \${URL}    \${BROWSER}
    Maximize Browser Window
    Sleep    1s
" >> "$OUTPUT_FILE"

# Przejdź przez wszystkie podkatalogi
for dir in $(find . -type d); do
    if [[ "$dir" == *"account"* ]]; then
                continue
    fi
    if [ -f "$dir/urls.py" ]; then
        echo "Processing $dir/urls.py"
        urls=$(extract_urls "$dir/urls.py")
    
        # Dodaj ścieżki do pliku skryptu
        for url in $urls; do
            if [[ "$url" == *"myadmin"* ]]; then
                continue
            fi            
            if [[ "$url" == *"admin"* ]]; then
                continue
            fi
            if [[ "$url" == *"logout"* ]]; then
                continue
            fi                       
            if [[ "$url" == *"login"* ]]; then
                continue
            fi            
            if [[ "$url" == *"login"* ]]; then
                continue
            fi
            if [[ "$url" == *"account"* ]]; then
                continue
            fi
             
            echo "/turl $url"
            if [ "$dir" == "." ]; then
                full_url="${BASE_URL}/$url"
            else
                subdir=$(basename "$dir")
                if [ "$subdir" == "test1" ]; then
                    full_url="${BASE_URL}/$url"
                else
                    full_url="${BASE_URL}/$subdir/$url"
                fi
            fi

            # Dodaj odpowiednie parametry ID w zależności od URL
            if [[ "$full_url" == *"edit_crip"* ]]; then
                full_url="${full_url}?crip_id=12"
            elif [[ "$full_url" == *"edit_purchase"* ]]; then
                full_url="${full_url}?purchase_id=1509"
            elif [[ "$full_url" == *"edit_idea"* ]]; then
                full_url="${full_url}?idea_id=2727"
            elif [[ "$full_url" == *"edit_need"* ]]; then
                full_url="${full_url}?need_id=2500"
            elif [[ "$full_url" == *"edit_contract"* ]]; then
                full_url="${full_url}?contract_id=14701"
            fi

            echo "    Open Browser    $full_url    \${BROWSER}" >> "$OUTPUT_FILE"
            echo "    Maximize Browser Window" >> "$OUTPUT_FILE"
            echo "    Wait Until Page Contains    Logowanie" >> "$OUTPUT_FILE"
            echo "    Close Browser" >> "$OUTPUT_FILE"
        done
    fi
done

echo "Skrypt testujący został wygenerowany w pliku $OUTPUT_FILE"
