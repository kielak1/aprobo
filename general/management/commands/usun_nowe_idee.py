from django.core.management.base import BaseCommand
from ideas.models import Ideas, StatusIdei  # Upewnij się, że zamieniłeś 'myapp' na właściwą nazwę swojej aplikacji

class Command(BaseCommand):
    help = 'Usuwa wszystkie obiekty Ideas, których status_idei wskazuje na obiekt StatusIdei o polu status = "nowa"'

    def handle(self, *args, **kwargs):
        # Znajdź wszystkie obiekty StatusIdei o statusie "nowa"
        status_nowa = StatusIdei.objects.filter(status='nowa').first()

        if status_nowa:
            # Znajdź wszystkie idee ze statusem "nowa"
            ideas_to_delete = Ideas.objects.filter(status_idei=status_nowa)
            count = ideas_to_delete.count()
            
            # Usuń znalezione idee
            ideas_to_delete.delete()

            self.stdout.write(self.style.SUCCESS(f'Successfully deleted {count} ideas with status "nowa".'))
        else:
            self.stdout.write(self.style.WARNING('No status "nowa" found in StatusIdei.'))
