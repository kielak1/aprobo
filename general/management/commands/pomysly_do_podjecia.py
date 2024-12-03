from django.core.management import BaseCommand 
from general.raporty_jakosci import  pomysly_do_podjecia_det

class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        pomysly_do_podjecia_det()


     
