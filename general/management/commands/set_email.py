from django.core.management.base import BaseCommand
from django.contrib.auth.models import User

class Command(BaseCommand):
    help = 'Updates the email address for all users who have an email address set'

    def add_arguments(self, parser):
        parser.add_argument('new_email', type=str, help='The new email address to set for all users')

    def handle(self, *args, **kwargs):
        new_email = kwargs['new_email']
        users = User.objects.exclude(email='').exclude(email__isnull=True)

        if not users.exists():
            self.stdout.write(self.style.WARNING('No users found with an email address set.'))
            return

        for user in users:
            user.email = new_email
            user.save()

        self.stdout.write(self.style.SUCCESS(f'Successfully updated email address for {users.count()} users.'))
