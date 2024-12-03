from django.core.management.base import BaseCommand
from django.contrib.auth.models import User

class Command(BaseCommand):
    help = 'Delete all users who are not staff or superusers'

    def handle(self, *args, **kwargs):
        non_staff_users = User.objects.filter(is_staff=False, is_superuser=False)
        user_count = non_staff_users.count()
        
        if user_count > 0:
            non_staff_users.delete()
            self.stdout.write(self.style.SUCCESS(f'Successfully deleted {user_count} non-staff and non-superuser accounts.'))
        else:
            self.stdout.write('No non-staff and non-superuser accounts to delete.')
