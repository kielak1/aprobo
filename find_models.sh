#!/bin/bash

# Funkcja wyświetlająca aplikacje i modele
function find_models {
    local models_file="$1"
    local app_path=$(dirname "$models_file")
    local app_name=$(basename $(dirname "$app_path")) # Pobieramy nazwę aplikacji

    echo "Aplikacja: $app_name (Plik: $models_file)"
    
    # Szukamy definicji modeli w pliku .py
    grep -E 'class [A-Za-z0-9_]+\(.+Model.*\)' "$models_file" | while read -r line ; do
        # Wyciągamy nazwę modelu
        model_name=$(echo "$line" | sed -n 's/class \([A-Za-z0-9_]\+\).*/\1/p')
        if [[ -n "$model_name" ]]; then
            echo "  Model: $model_name"
        fi
    done
    
    echo ""
}

# Szukamy wszystkich plików .py w katalogach models oraz models.py w aplikacjach
echo "Struktura projektu Django i zdefiniowane modele:"
find . -type f \( -name "models.py" -o -path "*/models/*.py" \) | while read -r models_file ; do
    echo "Przeszukuję plik: $models_file"
    find_models "$models_file"
done
