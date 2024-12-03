#!/bin/bash

# Katalog, w którym chcesz zmienić uprawnienia
DIR="staticfiles"

# Ustaw uprawnienia rw dla wszystkich plików
find "$DIR" -type f -exec chmod 664 {} \;

# Ustaw uprawnienia rwx dla wszystkich podkatalogów
find "$DIR" -type d -exec chmod 775 {} \;

echo "Uprawnienia zostały zaktualizowane."
