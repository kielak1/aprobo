from django.db import models


class zlecenia_kontrolingowe(models.Model):
    numer = models.CharField(max_length=100, null=True)
    nazwa = models.CharField(max_length=1000)

    def __str__(self):
        return f"{self.numer} - {self.nazwa}"

    def get_link_short(self):
        return f"edit_zlecenia_short/?numer={self.id}"

    def suma_budzetu(self):
        return "+++"


class uslugi(models.Model):
    numer = models.CharField(max_length=100, null=True)
    nazwa = models.CharField(max_length=1000, null=True)

    def __str__(self):
        return f"{self.numer} - {self.nazwa}"

    def get_link_short(self):
        return f"edit_uslugi_short/?numer={self.id}"

    def suma_budzetu(self):
        return "+++"
