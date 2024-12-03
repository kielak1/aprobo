from django.core.management import BaseCommand 
from general.raporty_jakosci import  nielegalne_ezz_det

class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        nielegalne_ezz_det()


     
