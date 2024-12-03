import json
from django.contrib.auth.models import User, Group, Permission
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = 'Export users and their permissions'

    def handle(self, *args, **kwargs):
        users_data = []
        usernames = ['acceptor', 'architect', 'director', 'guest', 'manager', 'superuser', 'user', 'viewer']

        for username in usernames:
            try:
                user = User.objects.get(username=username)
                groups = list(user.groups.values_list('name', flat=True))
                permissions = list(user.user_permissions.values_list('codename', flat=True))
                user_data = {
                    'username': user.username,
                    'is_superuser': user.is_superuser,
                    'is_staff': user.is_staff,
                    'groups': groups,
                    'permissions': permissions
                }
                users_data.append(user_data)
            except User.DoesNotExist:
                self.stdout.write(self.style.WARNING(f'User {username} does not exist.'))

        with open('users_data.json', 'w') as f:
            json.dump(users_data, f, indent=4)

        self.stdout.write(self.style.SUCCESS('Users data exported successfully.'))
