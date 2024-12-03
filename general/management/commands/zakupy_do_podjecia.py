from django.core.management import BaseCommand 
from general.raporty_jakosci import  zakupy_do_podjecia_det

class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        zakupy_do_podjecia_det()


     
