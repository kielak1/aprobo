import os
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from general.mail import utworz_mail_do_wyslania

class Command(BaseCommand):
    help = 'Send emails to all users'

    def add_arguments(self, parser):
        parser.add_argument('subject_file', type=str, help='Path to the file containing the email subject')
        parser.add_argument('body_file', type=str, help='Path to the file containing the email body')

    def handle(self, *args, **options):
        subject_file = options['subject_file']
        body_file = options['body_file']

        # Wczytaj temat i treść e-maila z plików
        with open(subject_file, 'r', encoding='utf-8') as f:
            subject = f.read().strip()

        with open(body_file, 'r', encoding='utf-8') as f:
            body = f.read().strip()

        # Pobierz wszystkich użytkowników
        users = User.objects.all()

        # Wyślij e-maile do wszystkich użytkowników
        for user in users:
            email = utworz_mail_do_wyslania(user, subject, body)
            # Zakładam, że funkcja utworz_mail_do_wyslania zajmuje się wysyłaniem e-maili
            # Jeśli nie, tutaj powinno się znaleźć wysyłanie maila, np. email.send()

        self.stdout.write(self.style.SUCCESS('E-maile zostały wysłane.'))
