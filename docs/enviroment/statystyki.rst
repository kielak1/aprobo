Konfiguracja GoAccess
=====================

Instalacja GoAccess
-------------------

1. Zaktualizuj system i zainstaluj GoAccess:

   .. code-block:: bash

       sudo apt update
       sudo apt install goaccess

2. Utwórz plik skryptu w katalogu `/usr/local/sbin`:

   .. code-block:: bash

       sudo nano /usr/local/sbin/nginig-log-skrypt-all.sh

   Zawartość pliku:


   .. include:: ../../configs/prod/goaccess/nginig-log-skrypt-all.sh
      :code:

3. Nadaj uprawnienia do uruchamiania pliku:

   .. code-block:: bash

       sudo chmod +x /usr/local/sbin/nginig-log-skrypt-all.sh

Konfiguracja Cron
-----------------

1. Edytuj crontab, aby uruchamiać skrypt co 30 minut:

   .. code-block:: bash

       crontab -e

   Dodaj linię:

   .. code-block:: bash

       */30 * * * * /usr/local/sbin/nginig-log-skrypt-all.sh

Konfiguracja Nginx
------------------

1. Skonfiguruj nowy serwer w pliku `/etc/nginx/sites-available/stat.avanticdev.gas.pgnig.pl`:

   .. code-block:: nginx

       server {
           listen 80;
           server_name stat.avanticdev.gas.pgnig.pl;

           location / {
               root /var/www/html/nginix_raport;
               index combined_report.html;
           }
       }

2. Aktywuj konfigurację serwera:

   .. code-block:: bash

       sudo ln -s /etc/nginx/sites-available/stat.avanticdev.gas.pgnig.pl /etc/nginx/sites-enabled/

3. Zrestartuj serwer Nginx:

   .. code-block:: bash

       sudo systemctl restart nginx
