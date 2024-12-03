from django.core.management.base import BaseCommand
from purchases.models import Purchases
from general.models import Planowane_zakupy

class Command(BaseCommand):
    help = 'Delete any one purchase record'

    def handle(self, *args, **kwargs):
        try:
            purchase = Purchases.objects.first()
            if purchase:
                # Usuwanie ManyToMany relationships
                purchase.crip_id.clear()
                purchase.acceptors.clear()
                purchase.log.clear()

                # Usuwanie powiązanych obiektów (jeśli to możliwe)
                related_zakupy = Planowane_zakupy.objects.filter(zakup=purchase)
                related_zakupy.delete()

                # Usuń purchase
                purchase_id = purchase.id
                purchase.delete()
                self.stdout.write(self.style.SUCCESS(f'Purchase with id {purchase_id} has been deleted successfully.'))
            else:
                self.stdout.write(self.style.WARNING('No Purchase records found.'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'An error occurred: {e}'))
