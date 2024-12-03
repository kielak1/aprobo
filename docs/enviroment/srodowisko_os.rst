Konfiguracja środowiska systemu operacyjnego
============================================

1. Zapewnienie dostępności lokalizacji UTF-8
--------------------------------------------

Aby upewnić się, że system obsługuje polską lokalizację UTF-8, wykonaj poniższe kroki:

.. code-block:: bash

   sudo yum install glibc-locale-source glibc-langpack-pl
   sudo localedef -i pl_PL -f UTF-8 pl_PL.UTF-8

2. Utworzenie i aktywacja środowiska wirtualnego
------------------------------------------------

Załóż środowisko wirtualne w lokalizacji ``/opt/avantic/env``, a następnie je aktywuj:

.. code-block:: bash

   cd /opt/avantic
   python3 -m venv env
   source env/bin/activate

3. Wynik polecenia `pip freeze`
-------------------------------

Dla uzyskania listy zainstalowanych bibliotek w środowisku, wynik polecenia `pip freeze` znajduje się w pliku konfiguracyjnym:

.. include:: ../../configs/prod/conf-env/freeze.txt
   :code:

Uwagi końcowe
-------------

Pamiętaj, aby regularnie aktualizować lokalizację oraz środowisko wirtualne w celu zapewnienia kompatybilności z aktualizacjami systemu i aplikacji. 
W przypadku problemów z konfiguracją UTF-8, upewnij się, że system operacyjny obsługuje odpowiednie pakiety językowe.
