# your_app/management/commands/update_contracts.py
import unicodedata
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from contracts.models import Contracts
from general.models import Sections

class Command(BaseCommand):
    help = 'Update Contracts objects with missing coordinators based on osoba_prowadzaca or section'

    def normalize(self, text):
        # Normalize the text by removing diacritical marks and converting to lowercase
        text = unicodedata.normalize('NFD', text)
        text = text.encode('ascii', 'ignore').decode('utf-8')
        return text.lower()

    def handle(self, *args, **kwargs):
        contracts = Contracts.objects.filter(koordynator__isnull=True)

        for contract in contracts:
            user_assigned = False

            if contract.osoba_prowadzaca:
                last_name = contract.osoba_prowadzaca.split(' ')[-1]
                normalized_last_name = self.normalize(last_name)
                users = User.objects.all()
                matching_users = [user for user in users if self.normalize(user.last_name) == normalized_last_name]

                if matching_users:
                    user = matching_users[0]
                    contract.koordynator = user
                    contract.save()
                    self.stdout.write(self.style.SUCCESS(f'Successfully assigned koordynator for contract ID {contract.id} based on osoba_prowadzaca {contract.koordynator.username}'))
                    user_assigned = True
                else:
                    self.stdout.write(self.style.WARNING(f'No User found with last name {last_name} (normalized: {normalized_last_name}) for contract ID {contract.id}'))

            if not user_assigned:
                if contract.section:
                    if contract.section.kierownik:
                        contract.koordynator = contract.section.kierownik
                        contract.save()
                        self.stdout.write(self.style.SUCCESS(f'Successfully assigned koordynator for contract ID {contract.id} based on section kierownik {contract.koordynator.username}   ->  {contract.obslugiwana}       '))
                    else:
                        self.stdout.write(self.style.WARNING(f'Section ID {contract.section.id} has no kierownik for contract ID {contract.id}'))
                else:
                    if contract.obslugiwana is False:
                        try:
                            system_user = User.objects.get(username='system')
                            contract.koordynator = system_user
                            contract.save()
                            self.stdout.write(self.style.SUCCESS(f'Successfully assigned system user as koordynator for contract ID {contract.id}'))
                        except User.DoesNotExist:
                            self.stdout.write(self.style.ERROR(f'No User with username "system" found for contract ID {contract.id}'))
                    else:
                        self.stdout.write(self.style.ERROR(f'Contract ID {contract.id} has no section and obslugiwana is {contract.obslugiwana}'))
