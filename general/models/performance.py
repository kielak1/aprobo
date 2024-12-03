from django.db import models
from django.utils import timezone

class Stamp(models.Model):
    nazwa = models.CharField(max_length=400, default='', null=True, help_text='Nazwa zdarzenia')
    opis = models.TextField(blank=True, help_text='Opis kontekstu zdarzenia')
    czas_utworzenia = models.DateTimeField(default=timezone.now, help_text='Dokładny czas utworzenia')
    sekwencja = models.CharField(max_length=100, blank=True, help_text='Opcjonalna sekwencja, do której należy dany rekord')
    czas_trwania = models.DurationField(null=True, blank=True, help_text='Czas trwania operacji')
    typ_zdarzenia = models.CharField(max_length=100, blank=True, help_text='Rodzaj lub kategoria zdarzenia, np. "database", "IO", "CPU"')

    class Meta:
        ordering = ['czas_utworzenia']
        indexes = [
            models.Index(fields=['sekwencja']),
            models.Index(fields=['czas_utworzenia']),
        ]

    def __str__(self):
        return f"{self.nazwa} - {self.czas_trwania}- {self.czas_utworzenia}"

    def zapisz_czas_trwania(self, typ=""):
        """Funkcja do zapisania czasu trwania operacji. Domyślnie używa bieżącego czasu."""
        czas_koncowy = timezone.now()
        self.typ_zdarzenia = typ
        self.czas_trwania = czas_koncowy - self.czas_utworzenia
        self.save()



        