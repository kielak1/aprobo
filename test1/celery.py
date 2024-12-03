from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from django.apps import apps
from celery.schedules import crontab
import django

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "test1.settings")
django.setup()

app = Celery("test1")

# Using a string here means the worker will not have to pickle the object when using Windows.
app.config_from_object("django.conf:settings", namespace="CELERY")

# Load task modules from all registered Django app configs.
app.autodiscover_tasks(
    lambda: [app_config.name for app_config in apps.get_app_configs()]
)

# Specific task modules to discover
app.autodiscover_tasks(["general.raporty_jakosci"])

# Define the Celery beat schedule
app.conf.beat_schedule = {
    "send-emails-every-5-minutes": {
        "task": "general.mail.wyslij_wszystkie_maile",
        "schedule": crontab(minute="*/5"),
    },
    "unfreeze-suspended-ideas-every-30-minutes": {
        "task": "general.poprawianie_danych.odwies_zawieszone_pomysly",
        "schedule": crontab(minute="*/30"),
    },
    "update-ideas-status-every-10-minutes": {
        "task": "general.poprawianie_danych.popraw_status_idei",
        "schedule": crontab(minute="*/10"),
    },
    "update-needs-status-every-15-minutes": {
        "task": "general.poprawianie_danych.popraw_status_needs",
        "schedule": crontab(minute="*/15"),
    },
    "update-zakupy-do-podjecia-once-daily": {
        "task": "general.raporty_jakosci.zakupy_do_podjecia",
        "schedule": crontab(hour=7, minute=0),
    },
    "update-potrzeby-do-podjecia-once-daily": {
        "task": "general.raporty_jakosci.potrzeby_do_podjecia",
        "schedule": crontab(hour=7, minute=1),
    },
    "update-pomysly-do-podjecia-once-daily": {
        "task": "general.raporty_jakosci.pomysly_do_podjecia",
        "schedule": crontab(hour=7, minute=2),
    },
    "update-umowy-bez-statusu-once-daily": {
        "task": "general.raporty_jakosci.umowy_bez_statusu",
        "schedule": crontab(hour=7, minute=3),
    },
    "update-umowy-czy-kontynuowac-once-dailyhour=7,": {
        "task": "general.raporty_jakosci.umowy_czy_kontynuowac",
        "schedule": crontab(hour=7, minute=4),
    },
    "update-umowy-brak-wlasciciela-once-daily": {
        "task": "general.raporty_jakosci.umowy_brak_wlasciciela",
        "schedule": crontab(hour=7, minute=5),
    },
    "update-umowy-jak-kontynuowac-once-daily": {
        "task": "general.raporty_jakosci.umowy_jak_kontynuowac",
        "schedule": crontab(hour=7, minute=6),
    },
    "update-umowy-kiedy-kontynuowac-once-daily": {
        "task": "general.raporty_jakosci.umowy_kiedy_kontynuowac",
        "schedule": crontab(hour=7, minute=7),
    },
    "update-nielegalne-ezz-once-daily": {
        "task": "general.raporty_jakosci.nielegalne_ezz",
        "schedule": crontab(hour=7, minute=8),
    },
    "update-sections-users-once-daily": {
        "task": "general.poprawianie_danych.sections_users",
        "schedule": crontab(hour=7, minute=9),
    },
    "update-skoryguj-status-zakupow-once-daily": {
        "task": "general.poprawianie_danych.skoryguj_status_zakupow",
        "schedule": crontab(hour=7, minute=10),
    },
    "update-raport-ciaglosci-serwisow-once-daily": {
        "task": "general.raporty_jakosci.raport_ciaglosci_serwisow",
        "schedule": crontab(hour=7, minute=11),
    },
    "potencjalnie-zabezpieczone-umowy-once-daily": {
        "task": "general.raporty_jakosci.umowy_zabezpieczone",
        "schedule": crontab(hour=7, minute=12),
    },
}
