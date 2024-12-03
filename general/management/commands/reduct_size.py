from django.core.management.base import BaseCommand
from contracts.models import Contracts
from ideas.models import Ideas
from needs.models import Needs
from purchases.models import Purchases
from purchases.models import Postepowania

class Command(BaseCommand):
    help = "Generate a report of text fields with the lowest percentage of max length for specified models"

    def handle(self, *args, **options):
        models = [Contracts, Ideas, Needs, Purchases, Postepowania]
        report = []

        for model in models:
            model_name = model.__name__
            self.stdout.write(f"Processing model: {model_name}")
            
            # Pobranie wszystkich rekordów dla modelu
            queryset = model.objects.all()
            for field in model._meta.fields:
                if field.get_internal_type() == 'CharField' and field.max_length > 100:
                    field_name = field.name
                    max_length = field.max_length
                    
                    # Sortowanie rekordów na podstawie długości pola tekstowego
                    sorted_entries = sorted(
                        [(getattr(obj, field_name), obj.id) for obj in queryset if getattr(obj, field_name)],
                        key=lambda x: len(x[0]),
                        reverse=True
                    )
                    
                    # Sprawdzenie, czy istnieje co najmniej 3 wartości
                    if len(sorted_entries) >= 3:
                        third_longest = sorted_entries[2][0]
                        length_third_longest = len(third_longest)
                        length_percentage = (length_third_longest / max_length) * 100
                        
                        # Dodanie informacji do raportu
                        report_entry = {
                            "Model": model_name,
                            "Pole": field.verbose_name,
                            "Maksymalna długość": max_length,
                            "Procent do maks": length_percentage,
                            "ID najdłuższych": [sorted_entries[0][1], sorted_entries[1][1], sorted_entries[2][1]],
                            "Długość najdłuższego rekordu": len(sorted_entries[0][0]),
                            "Długość drugiego najdłuższego rekordu": len(sorted_entries[1][0]),
                            "Długość trzeciego najdłuższego rekordu": length_third_longest
                        }
                        
                        report.append(report_entry)
                        self.stdout.write(f"Added entry for field '{field_name}'")
                    else:
                        self.stdout.write(f"Not enough entries for field '{field_name}'")
        
        # Sortowanie raportu po wskaźniku procentowym i wybieranie 5 najniższych wartości
        bottom_5 = sorted(report, key=lambda x: x["Procent do maks"])[:10]
        self.display_bottom_5(bottom_5)

    def display_bottom_5(self, bottom_5):
        self.stdout.write("\nTop 5 Fields with the Lowest Percentage of Max Length:")
        for entry in bottom_5:
            self.stdout.write(f"Model: {entry['Model']}")
            self.stdout.write(f"Pole: {entry['Pole']}")
            self.stdout.write(f"Maksymalna długość: {entry['Maksymalna długość']}")
            self.stdout.write(f"Procent do maks: {entry['Procent do maks']:.2f}%")
            self.stdout.write(f"ID najdłuższych rekordów: {entry['ID najdłuższych']}")
            self.stdout.write(f"Długość najdłuższego rekordu: {entry['Długość najdłuższego rekordu']}")
            self.stdout.write(f"Długość drugiego najdłuższego rekordu: {entry['Długość drugiego najdłuższego rekordu']}")
            self.stdout.write(f"Długość trzeciego najdłuższego rekordu: {entry['Długość trzeciego najdłuższego rekordu']}")
            self.stdout.write("------------------------------------------------------")
