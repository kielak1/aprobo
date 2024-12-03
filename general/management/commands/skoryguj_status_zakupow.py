from django.core.management import BaseCommand 
from general.poprawianie_danych import skoryguj_status_zakupow_det

class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        skoryguj_status_zakupow_det()


     
