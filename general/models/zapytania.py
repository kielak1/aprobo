from django.db import models
from django.contrib.auth.models import User

class Zapytanie(models.Model):
    nazwa = models.CharField(max_length=400, default='', null=True)
    tresc = models.CharField(max_length=2400, default='', null=True)
    user = models.ForeignKey(User, on_delete=models.PROTECT, null=True)
    