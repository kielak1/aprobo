from django.core.management import BaseCommand 
from general.raporty_jakosci import  umowy_zabezpieczone_det

class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        umowy_zabezpieczone_det()


     
