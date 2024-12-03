from django.core.management import BaseCommand 
from general.linki import generate_need_url, generate_idea_url, generate_purchase_url

class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        link =  generate_idea_url( 2700 )
        print( link )       
