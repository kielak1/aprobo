from django.core.management import BaseCommand 
from general.raporty_zakupowe import  najblizsze_zakupy_det

class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        najblizsze_zakupy_det()


     
