from general.advanced_search import search_advanced
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = 'advanced search'

    def add_arguments(self, parser):
        parser.add_argument('query', type=str, help='query')


    def handle(self, *args, **options):
        query = options['query']
        print(search_advanced( query ))


        
