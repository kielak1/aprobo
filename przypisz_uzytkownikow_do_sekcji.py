import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'test1.settings')
django.setup()


from django.contrib.auth.models import User


from general.models import Sections
from django.db.models import Count

def assign_sections_to_users():
    # Wyszukiwanie użytkowników bez przypisanych sekcji, którzy mają wypełnione pole second_name
    users_without_sections = User.objects.annotate(num_sections=Count('custom_models')).filter(num_sections=0, last_name__isnull=False)

    for user in users_without_sections:
        print(f"Użytkownik: {user.first_name} {user.last_name}, ID: {user.id}")
        short_name = input("Podaj short_name sekcji do przypisania: ")

        try:
            section = Sections.objects.get(short_name=short_name)
            section.users.add(user)
            print(f"Użytkownik {user.first_name} {user.last_name} został przypisany do sekcji {section.name}.")
        except Sections.DoesNotExist:
            print("Nie znaleziono sekcji o podanym short_name.")

if __name__ == "__main__":
    assign_sections_to_users()


