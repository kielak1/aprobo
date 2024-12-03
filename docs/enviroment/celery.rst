Konfiguracja Celery
===================

* pip install celery redis

* Utwórz plik celery.py w katalogu głównym projektu (obok settings.py):

::

	# celery.py
	from __future__ import absolute_import, unicode_literals
	import os
	from celery import Celery
	from django.apps import apps
	from celery.schedules import crontab

	os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'test1.settings')

	app = Celery('test1')
	app.config_from_object('django.conf:settings', namespace='CELERY')

	# Ręczne określenie modułów do odkrywania zadań, w tym pliku mail.py
	app.autodiscover_tasks(lambda: [app_config.name for app_config in apps.get_app_configs()])



* W pliku __init__.py projektu dodaj:

::

	# __init__.py
	from __future__ import absolute_import, unicode_literals
	from .celery import app as celery_app

	__all__ = ('celery_app',)



* Dodaj konfigurację Celery do settings.py:

::

	# settings.py
	CELERY_BROKER_URL = 'redis://localhost:6379/0'
	CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'
	CELERY_ACCEPT_CONTENT = ['json']
	CELERY_TASK_SERIALIZER = 'json'
	CELERY_RESULT_SERIALIZER = 'json'
	CELERY_TIMEZONE = 'Europe/Warsaw'

	CELERY_BROKER_CONNECTION_RETRY_ON_STARTUP = True


* Utwórz lub edytuj plik mail.py w aplikacji, w której znajduje się funkcja wyslij_wszystkie_maile:

::

	# mail.py
	from celery import shared_task
	from .models import MaileDoWyslania
	from .mail_functions import wyslij_mail  # importuj funkcję wyslij_mail z odpowiedniego miejsca

	@shared_task
	def wyslij_wszystkie_maile():
	    wszystkie_maile = MaileDoWyslania.objects.all()
	    for mail in wszystkie_maile:
		if wyslij_mail(mail):
		    mail.delete()
		    print(f"E-mail to {mail.recipient} has been sent and deleted.")
		else:
		    print(f"Failed to send e-mail to {mail.recipient}.")


* W pliku celery.py dodaj konfigurację okresowych zadań:

::

	# celery.py (dodatkowa konfiguracja na końcu pliku)
	from celery.schedules import crontab

	app.conf.beat_schedule = {
	    'send-emails-every-5-minutes': {
		'task': 'general.mail.wyslij_wszystkie_maile',
		'schedule': crontab(minute='*/5'),
	    },
	}






Running Celery Worker and Beat
------------------------------

To run the Celery worker:

.. code-block:: sh

   celery -A test1 worker --loglevel=info

To run the Celery beat:

.. code-block:: sh

   celery -A test1 beat --loglevel=info




* instalacje redis

::

	sudo apt-get update
	sudo apt-get install redis-server



