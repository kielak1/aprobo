Przenoszenie bazy danych ze środowiska produkcyjnego do nieprodukcyjnego
========================================================================

Wymagania wstępne
-----------------
- Upewnij się, że zarówno na systemie produkcyjnym, jak i nieprodukcyjnym:

  - Używasz tej samej gałęzi w repozytorium Git.
  - Stan gałęzi jest zsynchronizowany zdalnie (``git pull``).
- Posiadasz odpowiednie dane uwierzytelniające:

  - Hasło użytkownika ``bgnig1`` dla bazy PostgreSQL.

Proces na środowisku produkcyjnym
---------------------------------

Eksport bazy danych
~~~~~~~~~~~~~~~~~~~
1. Otwórz terminal i przejdź do katalogu:

   .. code-block:: bash

      cd /home/tkielak/Avantic

2. Uruchom skrypt eksportujący bazę danych:

   .. code-block:: bash

      ./zrzuc_baze

3. Podaj nazwę pliku do zapisu:
   - Przykład: ``dump_bazy.dump``
4. Wprowadź hasło użytkownika ``bgnig1``.

**Wynik**: Eksport bazy danych zakończy się sukcesem, a plik zrzutu zostanie zapisany w podanej lokalizacji.

Dodanie pliku do repozytorium
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
1. Sprawdź status Git:

   .. code-block:: bash

      git status

2. Dodaj plik i zatwierdź zmiany:

   .. code-block:: bash

      git add dump_bazy.dump
      git commit -am "Dump bazy danych"

3. Wypchnij zmiany do zdalnego repozytorium:

   .. code-block:: bash

      git push

Proces na środowisku nieprodukcyjnym
------------------------------------

Pobranie pliku z repozytorium
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
1. Otwórz terminal i przejdź do katalogu:

   .. code-block:: bash

      cd /home/tkielak/Avantic

2. Pobierz zmiany z repozytorium:

   .. code-block:: bash

      git pull

Import bazy danych
~~~~~~~~~~~~~~~~~~
1. Uruchom skrypt odtwarzający bazę:

   .. code-block:: bash

      ./odtworz_baze

2. Potwierdź usunięcie i odtworzenie bazy danych:

   - Odpowiedz ``t`` na pytanie.
3. Podaj nazwę pliku kopii bazy danych:

   - Przykład: ``dump_bazy.dump``
4. Wprowadź hasło użytkownika ``bgnig1``.

**Wynik**: Baza danych zostanie odtworzona z pliku ``dump_bazy.dump``. Dodatkowo:

- Użytkownicy testowi zostaną zaimportowani.
- Adresy e-mail zostaną ustawione na ``fake@fake.pl``.

Uwagi
-----
1. **Bezpieczeństwo**:

   - Inicjalne hasło użytkownika bgnig1 w bazie postgres to bgnig.

Skrypty
-------

Skrypt: `zrzuc_baze`
~~~~~~~~~~~~~~~~~~~~
.. code-block:: bash

   #!/bin/bash

   # Funkcja do sprawdzenia, czy ostatnie polecenie zakończyło się powodzeniem
   check_status() {
     if [ $? -ne 0 ]; then
       echo "Błąd podczas wykonywania operacji: $1"
       exit 1
     fi
   }

   # Zapytaj użytkownika o nazwę pliku
   read -p "Podaj nazwę pliku do zapisu zrzutu bazy danych (np. /home/tkielak/dump_bazy.dump): " plik_zrzutu

   # Sprawdź, czy nazwa pliku jest poprawna
   if [ -z "$plik_zrzutu" ]; then
     echo "Nazwa pliku nie może być pusta. Przerywam."
     exit 1
   fi

   # Wykonaj zrzut bazy danych
   echo "Tworzenie zrzutu bazy danych do pliku $plik_zrzutu..."
   pg_dump -U bgnig1 -h localhost -Fc -f "$plik_zrzutu" -d bgnig1
   check_status "pg_dump"

   echo "Zrzut bazy danych zakończony sukcesem."

Skrypt: `odtworz_baze`
~~~~~~~~~~~~~~~~~~~~~~
.. code-block:: bash

   #!/bin/bash

   # Funkcja do sprawdzenia, czy ostatnie polecenie zakończyło się powodzeniem
   check_status() {
     if [ $? -ne 0 ]; then
       echo "Błąd podczas wykonywania operacji: $1"
       exit 1
     fi
   }

   # Potwierdzenie usunięcia i odtworzenia bazy danych
   echo "Czy chcesz usunąć i utworzyć bazę danych od nowa? (t/n)"
   read response
   if [[ "$response" == "t" ]]; then
     echo "Usuwanie i tworzenie bazy danych..."
     
     # Zakończenie aktywnych połączeń z bazą
     sudo -u postgres psql -c "SELECT pg_terminate_backend(pid) FROM pg_stat_activity WHERE datname = 'bgnig1';"
     
     sudo -u postgres psql -c "DROP DATABASE IF EXISTS bgnig1;"
     check_status "DROP DATABASE"
     sudo -u postgres psql -c "CREATE DATABASE bgnig1;"
     check_status "CREATE DATABASE"
   fi

   # Dodanie uprawnień dla użytkownika
   echo "Dodawanie uprawnień dla użytkownika bgnig1..."
   sudo -u postgres psql -d bgnig1 -c "GRANT CONNECT ON DATABASE bgnig1 TO bgnig1;"
   check_status "GRANT CONNECT"
   sudo -u postgres psql -d bgnig1 -c "GRANT ALL PRIVILEGES ON SCHEMA public TO bgnig1;"
   check_status "GRANT ALL PRIVILEGES"

   # Odtworzenie bazy danych
   echo "Podaj nazwę pliku z kopią zapasową bazy danych (.dump):"
   read dump_file

   if [ -z "$dump_file" ]; then
     echo "Nazwa pliku nie może być pusta. Przerywam."
     exit 1
   fi

   if [ ! -f "$dump_file" ]; then
     echo "Plik kopii zapasowej nie istnieje: $dump_file"
     exit 1
   fi

   echo "Odtwarzanie bazy danych z pliku $dump_file..."
   pg_restore -U bgnig1 -h localhost -d bgnig1 "$dump_file"
   check_status "pg_restore"

   # Import użytkowników testowych
   echo "Importowanie użytkowników testowych..."
   python manage.py import_users_pass qwer
   check_status "import_users (import użytkowników)"

   # Ustawienie haseł dla użytkowników
   echo "Ustawianie maili dla wszystkich na fake@fake.pl"
   python manage.py set_email fake@fake.pl
   check_status "set_email (ustawienie maili)"

   echo "Import bazy danych zakończony sukcesem."
