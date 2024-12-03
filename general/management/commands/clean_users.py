import json
from datetime import timedelta
from django.utils.timezone import now
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.db.models.deletion import ProtectedError


class Command(BaseCommand):
    help = "Usuwa użytkowników, którzy nie są na liście ignorowanych, nie logowali się w ciągu określonej liczby dni, i generuje raport usuniętych użytkowników."

    def add_arguments(self, parser):
        parser.add_argument(
            "--ignore-file",
            type=str,
            required=True,
            help="Ścieżka do pliku JSON z listą użytkowników do pominięcia.",
        )
        parser.add_argument(
            "--output-file",
            type=str,
            required=True,
            help="Ścieżka do pliku JSON, w którym zostanie zapisany raport usuniętych użytkowników.",
        )
        parser.add_argument(
            "--days",
            type=int,
            default=140,
            help="Liczba dni od ostatniego logowania użytkownika, po której może zostać usunięty (domyślnie 140 dni).",
        )

    def handle(self, *args, **options):
        ignore_file = options["ignore_file"]
        output_file = options["output_file"]
        days = options["days"]

        self.stdout.write(f"Używana liczba dni: {days}")

        # Wczytaj listę użytkowników do pominięcia
        ignored_users = self.load_ignored_users(ignore_file)
        self.stdout.write(f"Wczytano {len(ignored_users)} użytkowników do pominięcia.")

        # Znajdź użytkowników do usunięcia
        safe_period = now() - timedelta(days=days)
        users_to_delete = User.objects.exclude(
            id__in=[user["user_id"] for user in ignored_users if user["user_id"]]
        ).exclude(
            username__in=[user["username"] for user in ignored_users if user["username"]]
        ).filter(
            last_login__lt=safe_period  # Użytkownicy, którzy nie logowali się w ciągu podanej liczby dni
        )

        self.stdout.write(f"Znaleziono {users_to_delete.count()} użytkowników do usunięcia.")

        # Usuń użytkowników i buduj raport
        deleted_users = []
        for user in users_to_delete:
            try:
                user.delete()
                self.stdout.write(self.style.SUCCESS(f"Usunięto użytkownika: {user.username}"))
                deleted_users.append({
                    "user_id": user.id,
                    "username": user.username,
                    "reason": "Successfully deleted"
                })
            except ProtectedError as e:
                self.stdout.write(self.style.WARNING(
                    f"Nie można usunąć użytkownika {user.username}: {e}"
                ))

        # Zapisz raport do pliku
        self.save_deleted_users_report(deleted_users, output_file)
        self.stdout.write(self.style.SUCCESS(f"Raport usuniętych użytkowników zapisano do {output_file}."))

    def load_ignored_users(self, file_path):
        """
        Wczytuje listę użytkowników do pominięcia z pliku JSON.
        """
        try:
            with open(file_path, mode="r", encoding="utf-8") as file:
                return json.load(file)
        except FileNotFoundError:
            self.stdout.write(self.style.ERROR(f"Plik {file_path} nie istnieje."))
            return []
        except json.JSONDecodeError as e:
            self.stdout.write(self.style.ERROR(f"Błąd dekodowania JSON: {e}"))
            return []

    def save_deleted_users_report(self, deleted_users, file_path):
        """
        Zapisuje raport usuniętych użytkowników do pliku JSON.
        """
        try:
            with open(file_path, mode="w", encoding="utf-8") as file:
                json.dump(deleted_users, file, indent=4)
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Błąd zapisu pliku {file_path}: {e}"))
