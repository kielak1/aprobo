from django.core.management.base import BaseCommand
from django.utils import timezone
from contracts.models import Contracts
from ideas.models import Ideas
from needs.models import Needs
from purchases.models import Purchases
from purchases.models import Postepowania

class Command(BaseCommand):
    help = "Generate a report of text fields with third longest entries for specified models"

    def handle(self, *args, **options):
        models = [Contracts, Ideas, Needs, Purchases, Postepowania]
        report = []

        for model in models:
            model_name = model.__name__
            self.stdout.write(f"Processing model: {model_name}")
            
            # Pobranie najnowszych 100 rekordów dla modelu
            queryset = model.objects.all().order_by("-id")[:100]
            for field in model._meta.fields:
                if field.get_internal_type() == 'CharField' and field.max_length > 1:
                    field_name = field.name
                    max_length = field.max_length
                    
                    # Sortowanie rekordów na podstawie długości pola tekstowego
                    sorted_entries = sorted(
                        [getattr(obj, field_name) for obj in queryset if getattr(obj, field_name)],
                        key=len,
                        reverse=True
                    )
                    
                    # Sprawdzenie, czy istnieje co najmniej 3 wartości
                    if len(sorted_entries) >= 3:
                        third_longest = sorted_entries[2]
                        length_third_longest = len(third_longest)
                        length_percentage = (length_third_longest / max_length) * 100
                        
                        # Dodanie informacji do raportu
                        report_entry = {
                            "Model": model_name,
                            "Pole": field.verbose_name,
                            "Maksymalna długość": max_length,
                            "Procent do maks": length_percentage,
                        }
                        
                        # Obliczanie zasugerowanej wartości, jeśli procent przekracza 70%
                        if length_percentage > 70:
                            suggested_length = int(length_third_longest / 0.7) + 1
                            report_entry["Sugerowana długość"] = suggested_length
                        
                        report.append(report_entry)
                        self.stdout.write(f"Added entry for field '{field_name}'")
                    else:
                        self.stdout.write(f"Not enough entries for field '{field_name}'")
        
        # Wyświetlenie pełnego raportu
        self.display_report(report)
        
        # Sortowanie raportu po wskaźniku procentowym i wybieranie 10 najwyższych wartości
        top_10 = sorted(report, key=lambda x: x["Procent do maks"], reverse=True)[:10]
        self.display_top_10(top_10)

    def display_report(self, report):
        self.stdout.write("Generated Report:")
        for entry in report:
            self.stdout.write(f"Model: {entry['Model']}")
            self.stdout.write(f"Pole: {entry['Pole']}")
            self.stdout.write(f"Maksymalna długość: {entry['Maksymalna długość']}")
            self.stdout.write(f"Procent do maks: {entry['Procent do maks']:.2f}%")
            if "Sugerowana długość" in entry:
                self.stdout.write(f"Sugerowana długość: {entry['Sugerowana długość']}")
            self.stdout.write("------------------------------------------------------")

    def display_top_10(self, top_10):
        self.stdout.write("\nTop 10 Fields with the Highest Percentage of Max Length:")
        for entry in top_10:
            self.stdout.write(f"Model: {entry['Model']}")
            self.stdout.write(f"Pole: {entry['Pole']}")
            self.stdout.write(f"Maksymalna długość: {entry['Maksymalna długość']}")
            self.stdout.write(f"Procent do maks: {entry['Procent do maks']:.2f}%")
            if "Sugerowana długość" in entry:
                self.stdout.write(f"Sugerowana długość: {entry['Sugerowana długość']}")
            self.stdout.write("------------------------------------------------------")
