from django.core.management import BaseCommand 
from general.raporty_jakosci import  umowy_jak_kontynuowac_det

class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        umowy_jak_kontynuowac_det()


     
