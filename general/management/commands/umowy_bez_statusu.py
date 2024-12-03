from django.core.management import BaseCommand 
from general.raporty_jakosci import  umowy_bez_statusu_det

class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        umowy_bez_statusu_det()


     
