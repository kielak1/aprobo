from django.core.management.base import BaseCommand
from django.utils import timezone
from purchases.models import Purchases

class Command(BaseCommand):
    help = 'Update wymagana_data_zawarcia_umowy with need.wymagana_data_realizacji if need is not None'

    def handle(self, *args, **kwargs):
 
        purchases_with_required_date = Purchases.objects.filter(wymagana_data_zawarcia_umowy__isnull=True)

        updated_count = 0

        for purchase in purchases_with_required_date:
 
            # Sprawdzenie, czy 'need' jest różne od None
            if purchase.need is not None:
                # Ustawienie wartości pola 'wymagana_data_zawarcia_umowy' na 'need.wymagana_data_realizacji'
                if purchase.need.wymagana_data_realizacji:
                    print( purchase.id,  purchase.przedmiot_zakupu)
                    purchase.wymagana_data_zawarcia_umowy = purchase.need.wymagana_data_realizacji
                    purchase.save()
                    updated_count += 1

        self.stdout.write(self.style.SUCCESS(f'Updated {updated_count} purchases with the required date.'))
