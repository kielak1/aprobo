from django.db import models

class Variable(models.Model):
    nazwa = models.CharField(max_length=200, default='', blank=True, help_text='Nazwa zmiennej')
    wartosc = models.IntegerField(default=0, null=True, blank=True)

    def __str__(self):
        return f"{self.nazwa}={self.wartosc}"

    @classmethod
    def get(cls, nazwa, wartosc_domyslna=0):
        obj, created = cls.objects.get_or_create(nazwa=nazwa, defaults={'wartosc': wartosc_domyslna})
        return obj.wartosc

    @classmethod
    def set(cls, nazwa, wartosc):
        obj, created = cls.objects.get_or_create(nazwa=nazwa)
        obj.wartosc = wartosc
        obj.save()