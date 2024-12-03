from django.core.management import BaseCommand
from general.poprawianie_danych import sections_users_det

class Command(BaseCommand):
    help = 'Uruchamia funkcję sections_users_det'

    def handle(self, *args, **kwargs):
        sections_users_det()
