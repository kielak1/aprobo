Konfiguracja Nginx
==================

Główna konfiguracja Nginx znajduje się w pliku `/etc/nginx/nginx.conf`
----------------------------------------------------------------------

Funkcjonują trzy serwisy, których konfiguracje znajdują się w katalogu `/etc/nginx/sites.d`.

Struktura plików Nginx
----------------------

Poniżej przedstawiona jest struktura katalogów oraz zawartość plików, zaczynając od ścieżki `/etc/nginx/`:

.. code-block:: text

   /etc/nginx/
   ├── nginx.conf
   ├── sites.d/
   │   ├── avantic.gas.pgnig.pl  
   │   ├── doc.avantic.gas.pgnig.pl           
   │   └── stat.avantic.gas.pgnig.pl          
   └── ssl/
       ├── cert.pem
       └── key.pem

.. include:: nginx_config.rst

W przypadku serwisu `doc.avantic.gas.pgnig.pl` dostęp do dokumentacji w niektórych sekcjach jest zabezpieczony hasłami. Poniżej znajdują się loginy i hasła inicjalne:

.. list-table:: Hasła dostępowe
   :header-rows: 1

   * - Login
     - Hasło
   * - developer
     - dev!?
   * - admin
     - adm??#
   * - environment
     - env##!!

Tworzenie plików haseł
----------------------

Jeżei jeszcze nie tego nie zrobłes to zainstaluj httpd-tools:

.. code-block:: bash

   sudo yum install httpd-tools


Aby utworzyć pliki z hasłami, możesz użyć poniższych poleceń:

.. code-block:: bash

   sudo htpasswd -c /etc/nginx/.devpasswd developer
   sudo htpasswd -c /etc/nginx/.envpasswd environment
   sudo htpasswd -c /etc/nginx/.admpasswd admin

Po utworzeniu plików z hasłami należy nadać im odpowiednie uprawnienia, aby były czytelne dla serwera Nginx:

.. code-block:: bash

   sudo chmod a+r /etc/nginx/.devpasswd
   sudo chmod a+r /etc/nginx/.envpasswd
   sudo chmod a+r /etc/nginx/.admpasswd


**Przeładowanie konfiguracji Nginx**
------------------------------------

Po utworzeniu lub edycji plików z hasłami konieczne jest przeładowanie konfiguracji Nginx, aby zmiany zostały zastosowane. W tym celu użyj następującego polecenia:

.. code-block:: bash

   sudo systemctl reload nginx

Jeśli chcesz sprawdzić poprawność konfiguracji Nginx przed przeładowaniem, możesz użyć polecenia:

.. code-block:: bash

   sudo nginx -t

Jeżeli wszystko jest poprawne, zobaczysz komunikat:
   
   nginx: the configuration file /etc/nginx/nginx.conf syntax is ok
   nginx: configuration file /etc/nginx/nginx.conf test is successful





logi nginix:
------------
* /var/log/nginx/