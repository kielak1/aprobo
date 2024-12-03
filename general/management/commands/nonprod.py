
import os
import django
from django.core.management import BaseCommand, call_command
from general.models import Parametry

class Command(BaseCommand):
    help = 'Run import_users_pass and update send_not parameters'

    def handle(self, *args, **kwargs):
        os.environ.setdefault("DJANGO_SETTINGS_MODULE", "test1.settings")
        django.setup()

        # Uruchomienie skryptu import_users_pass
        call_command('import_users_pass', 'qwer')

        self.stdout.write("Users ok!")

        # Ustawienie parametrów w modelu Parametry
        try:
            send_not_record = Parametry.objects.get(nazwa='send_not')
            send_not_record.num = 0    
            send_not_record.str = '0'    
            send_not_record.save()    
            self.stdout.write(self.style.SUCCESS("Pomyślnie zaktualizowano rekord send_not."))
        except Parametry.DoesNotExist:
            self.stdout.write(self.style.ERROR("Rekord send_not nie istnieje."))
