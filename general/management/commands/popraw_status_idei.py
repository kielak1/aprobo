from django.core.management import BaseCommand 
from general.poprawianie_danych import popraw_status_idei_det

class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        popraw_status_idei_det()
     
