from django.core.management import BaseCommand 
from general.raporty_jakosci import raport_ciaglosci_serwisow_det

class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        raport_ciaglosci_serwisow_det()


     
