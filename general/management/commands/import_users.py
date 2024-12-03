import json
from django.contrib.auth.models import User, Group, Permission
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = 'Import users and their permissions'

    def handle(self, *args, **kwargs):
        with open('users_data.json', 'r') as f:
            users_data = json.load(f)

        for user_data in users_data:
            user, created = User.objects.get_or_create(username=user_data['username'])
            user.is_superuser = user_data['is_superuser']
            user.is_staff = user_data['is_staff']
            user.save()

            user.groups.clear()
            for group_name in user_data['groups']:
                group, _ = Group.objects.get_or_create(name=group_name)
                user.groups.add(group)

            user.user_permissions.clear()
            for perm_codename in user_data['permissions']:
                try:
                    permission = Permission.objects.get(codename=perm_codename)
                    user.user_permissions.add(permission)
                except Permission.DoesNotExist:
                    self.stdout.write(self.style.WARNING(f'Permission {perm_codename} does not exist.'))

            self.stdout.write(self.style.SUCCESS(f'User {user.username} imported successfully.'))

        self.stdout.write(self.style.SUCCESS('All users imported successfully.'))