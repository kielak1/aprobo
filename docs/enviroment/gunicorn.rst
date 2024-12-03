Konfiguracja Gunicorn
=====================




* python manage.py collectstatic

plik konfiguracyjny gunicorn:
-----------------------------
* /home/tkielak/testy-django/bgnig1/test1/gunicorn_config.py


.. include:: ../../configs/prod/gunicorn/gunicorn_config.py
      :code:







static files:
-------------
* /home/tkielak/testy-django/bgnig1/test1/staticfiles/

uruchomienie gunicorna:
-----------------------
* gunicorn -c gunicorn_config.py test1.wsgi:application


Konfiguracja i uruchomienie serwisu
-----------------------------------

plik: /etc/systemd/system/gunicorn.service
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^



.. include:: ../../configs/prod/gunicorn/gunicorn.service
      :code:







polecenia:
^^^^^^^^^^

* sudo systemctl daemon-reload
* sudo systemctl restart gunicorn
* sudo systemctl enable gunicorn

* sudo systemctl status gunicorn

restartowanie serwisu:
^^^^^^^^^^^^^^^^^^^^^^

* sudo systemctl restart gunicorn
* sudo systemctl status gunicorn


