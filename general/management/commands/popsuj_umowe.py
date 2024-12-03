from django.core.management.base import BaseCommand
from contracts.models import Contracts
import logging

# Set up logging
logger = logging.getLogger('avantic')

class Command(BaseCommand):
    help = 'Update the "czy_obslugiwana" field for the first contract record to None'

    def handle(self, *args, **kwargs):
        try:
            # Fetch the first contract
            contract = Contracts.objects.first()
            if contract:
                contract_id = contract.id
                contract.obslugiwana = None
                contract.save()

                # Log success
                logger.info(f'Contract with id {contract_id} has been updated successfully.')
                self.stdout.write(self.style.SUCCESS(f'Contract with id {contract_id} has been updated successfully.'))
            else:
                # Log no contracts found
                logger.warning('No Contracts records found.')
                self.stdout.write(self.style.WARNING('No Contracts records found.'))
        except Exception as e:
            # Log the error
            logger.error(f'An error occurred: {e}', exc_info=True)
            self.stdout.write(self.style.ERROR(f'An error occurred: {e}'))
