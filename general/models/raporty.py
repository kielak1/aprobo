from django.db import models

from purchases.models import Purchases
from needs.models import Needs
from ideas.models import Ideas
from general.models import  Sections
from django.contrib.auth.models import User
from general.models import  Sposob_wyceny, Sposob_zakupu, Rodzaj_inicjatywy

class Planowane_zakupy(models.Model):
    subject = models.CharField(max_length=5000, null=True, default=None)
    zakup = models.ForeignKey(Purchases, on_delete=models.PROTECT, null=True, default=None)
    potrzeba = models.ForeignKey(Needs, on_delete=models.PROTECT, null=True, default=None)
    pomysl = models.ForeignKey(Ideas, on_delete=models.PROTECT, null=True, default=None)
    budzet = models.FloatField(max_length=19, default=0, null=True)
    section = models.ForeignKey( Sections, on_delete=models.PROTECT,null=True , default=None)
    osoba_prowadzaca = models.ForeignKey(User, on_delete=models.PROTECT, null=True, default=None)
    wymagana_data_realizacji = models.DateField(default=None, null=True)  

    wymagana_data_zawarcia_umowy = models.DateField(default=None, null=True)  

    EZZ_number = models.CharField(max_length=20, null=True, default=None)
    waluta = models.CharField(max_length=7, default='PLN', null=True)
    budzet_capex_netto = models.FloatField(default=0, null=True)
    budzet_opex_netto = models.FloatField(default=0, null=True)   
    sposob_wyceny = models.ForeignKey( Sposob_wyceny, on_delete=models.PROTECT,null=True )
    dostawca = models.CharField(max_length=191, default='', null=True)
    sposob_zakupu =  models.ForeignKey( Sposob_zakupu, on_delete=models.PROTECT,null=True )
 
    odtworzeniowy = models.BooleanField(default=False, null=True)
    rozwojowy = models.BooleanField(default=False, null=True)
    rodzaj_inicjatywy = models.ForeignKey(Rodzaj_inicjatywy, on_delete=models.PROTECT, null=True)

    def __str__(self):
        return self.subject     