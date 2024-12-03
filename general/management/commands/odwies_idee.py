from django.core.management import BaseCommand 
from general.poprawianie_danych import odwies_zawieszone

class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        odwies_zawieszone()
     
