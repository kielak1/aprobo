from django.core.management import BaseCommand 
from general.raporty_jakosci import  potrzeby_do_podjecia_det

class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        potrzeby_do_podjecia_det()


     
