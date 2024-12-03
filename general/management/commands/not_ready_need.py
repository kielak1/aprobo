from django.core.management.base import BaseCommand, CommandError
from needs.models import Needs
from general.models import Status_akceptacji

class Command(BaseCommand):
    help = 'Sets the status fields to "niegotowe" for a given Needs record'

    def add_arguments(self, parser):
        parser.add_argument('need_id', type=int, help='ID of the Needs record')

    def handle(self, *args, **options):
        need_id = options['need_id']
        try:
            need_record = Needs.objects.get(id=need_id)
            not_ready_status = Status_akceptacji.objects.get(akceptacja="niegotowe")
            
            need_record.status_akceptacji_infrastruktury = not_ready_status
            need_record.status_akceptacji_sieci = not_ready_status
            need_record.status_akceptacji_finansow = not_ready_status
            need_record.status_akceptacji_uslug = not_ready_status
            
            need_record.save()
            
            self.stdout.write(self.style.SUCCESS(f'Statuses updated successfully for Need ID {need_id}'))
        except Needs.DoesNotExist:
            raise CommandError(f'Need with ID {need_id} does not exist.')
        except Status_akceptacji.DoesNotExist:
            raise CommandError('Status "niegotowe" does not exist in Status_akceptacji.')
        except Exception as e:
            raise CommandError(f'An error occurred: {e}')
