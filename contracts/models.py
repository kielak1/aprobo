from django.db import models
from datetime import date
from general.models import Sections, Clients
from ideas.models import Ideas
from django.contrib.auth.models import User
from django.utils import timezone
from django.contrib.contenttypes.fields import GenericRelation
from general.models import Note


class CBU(models.Model):
    sygnatura = models.CharField(max_length=40, verbose_name="Sygnatura")
    data_zawarcia = models.DateField(
        default=date(1990, 1, 1), verbose_name="Data zawarcia"
    )
    data_zakonczenia = models.DateField(
        default=date(1990, 1, 1), verbose_name="Data zakończenia"
    )
    status = models.CharField(max_length=20, verbose_name="Status")
    nazwa_kontrahenta = models.CharField(
        max_length=400, verbose_name="Nazwa kontrahenta"
    )
    osoba_prowadzaca = models.CharField(max_length=50, verbose_name="Osoba prowadząca")
    wartosc_wydatkowa = models.FloatField(verbose_name="Wartość wydatkowa")
    wartosc_wplywowa = models.FloatField(verbose_name="Wartość wpływowa")
    wartosc_odbiorow_wydatkowych = models.FloatField(
        verbose_name="Wartość odbiorów wydatkowych"
    )
    wartosc_odbiorow_wplywowych = models.FloatField(
        verbose_name="Wartość odbiorów wpływowych"
    )
    temat = models.CharField(max_length=700, verbose_name="Temat")
    idemand = models.CharField(max_length=20, verbose_name="IDemand")
    mandant = models.CharField(max_length=20, default=None, verbose_name="Mandant")

    class Meta:
        verbose_name = "CBU"
        verbose_name_plural = "CBU"


class EZZC(models.Model):
    sygnatura = models.CharField(max_length=40, verbose_name="Sygnatura")  #  1
    sygnatura_nadrzedna = models.CharField(
        max_length=41, null=True, verbose_name="Sygnatura nadrzędna"
    )  #  2
    przedmiot = models.CharField(max_length=377, verbose_name="Przedmiot")  #  3
    numer_SRM = models.CharField(
        max_length=21, null=True, verbose_name="Numer SRM"
    )  #  5
    numer_ZZZT = models.CharField(
        max_length=22, null=True, verbose_name="Numer ZZZT"
    )  #  6
    wartosc = models.FloatField(verbose_name="Wartość")  # 15
    typ_umowy = models.CharField(max_length=38, verbose_name="Typ umowy")  # 24
    komorka = models.CharField(max_length=7, verbose_name="Komórka")  # 25
    podstawa_prawna = models.CharField(
        max_length=24, verbose_name="Podstawa prawna"
    )  # 28
    waluta = models.CharField(max_length=6, null=True, verbose_name="Waluta")  # 32
    wlasciciel_merytoryczny = models.CharField(
        max_length=25, verbose_name="Właściciel merytoryczny"
    )  # 33
    opiekun_BZ = models.CharField(
        max_length=26, null=True, verbose_name="Opiekun BZ"
    )  # 34
    dostawca = models.CharField(max_length=98, verbose_name="Dostawca")  # 35
    koordynatorzy = models.CharField(max_length=52, verbose_name="Koordynatorzy")  # 39
    typ_zakresu = models.CharField(max_length=41, verbose_name="Typ zakresu")  # 41
    status = models.CharField(max_length=15, verbose_name="Status")  # 42
    od_kiedy = models.DateField(default=date(1990, 1, 1), verbose_name="Od kiedy")  # 43
    do_kiedy = models.DateField(default=date(1990, 1, 1), verbose_name="Do kiedy")  # 44

    class Meta:
        verbose_name = "EZZC"
        verbose_name_plural = "EZZC"


class LogContract(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.PROTECT, null=True, verbose_name="Użytkownik"
    )
    akcja = models.CharField(
        max_length=303, null=True, default=None, verbose_name="Akcja"
    )
    data = models.DateTimeField(default=timezone.now, verbose_name="Data")

    def __str__(self):
        return f"{self.data} {self.user.username} {self.akcja}"

    class Meta:
        verbose_name = "Log umowy"
        verbose_name_plural = "Logi umów"


class Contracts(models.Model):
    subject = models.CharField(max_length=700, verbose_name="Temat")
    kontrahent = models.CharField(
        max_length=400, null=True, default="", verbose_name="Kontrahent"
    )
    numer_umowy = models.CharField(max_length=41, null=True, verbose_name="Numer umowy")
    data_zawarcia = models.DateField(
        default=date(1990, 1, 1), verbose_name="Data zawarcia"
    )
    obslugiwana = models.BooleanField(
        null=True, default=None, verbose_name="Obsługiwana"
    )
    section = models.ForeignKey(
        Sections, on_delete=models.PROTECT, null=True, verbose_name="Sekcja"
    )
    zakres = models.CharField(max_length=700, null=True, verbose_name="Zakres")
    czy_wymagana_kontynuacja = models.BooleanField(
        null=True, verbose_name="Czy wymagana kontynuacja"
    )
    wymagana_data_zawarcia_kolejnej_umowy = models.DateField(
        default=None, null=True, verbose_name="Wymagana data zawarcia kolejnej umowy"
    )
    przedmiot_kolejnej_umowy = models.CharField(
        max_length=700, null=True, verbose_name="Przedmiot kolejnej umowy"
    )
    wartosc = models.FloatField(
        max_length=19, default=0, null=True, verbose_name="Wartość"
    )  # 15
    waluta = models.CharField(
        max_length=5, null=True, default="PLN", verbose_name="Waluta"
    )
    osoba_prowadzaca = models.CharField(
        max_length=42, null=True, default=None, verbose_name="Osoba prowadząca"
    )
    komentarz = models.CharField(
        max_length=303,
        null=True,
        blank=True,  # Pozwala na puste pole w formularzu
        default=None,
        verbose_name="Komentarz",
    )
    nr_ezz = models.CharField(
        max_length=30, null=True, default=None, verbose_name="Numer EZZ"
    )
    liczba_aneksow = models.IntegerField(default=0, verbose_name="Liczba aneksów")
    ideas = models.ManyToManyField(
        Ideas, blank=True, default=None, verbose_name="Pomysły"
    )
    ezzc = models.OneToOneField(
        EZZC,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="ezzc",
        verbose_name="EZZC",
    )
    cbu = models.OneToOneField(
        CBU,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="cbu",
        verbose_name="CBU",
    )
    log = models.ManyToManyField(
        LogContract, blank=True, default=None, verbose_name="Logi"
    )
    notes = GenericRelation(Note, verbose_name="Notatki")
    koordynator = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        default=None,
        verbose_name="Koordynator",
    )

    def __str__(self):
        return self.subject

    def get_link(self):
        return f"edit_contract/?contract_id={self.id}"

    def get_link_short(self):
        return f"edit_contract_short/?contract_id={self.id}"

    class Meta:
        verbose_name = "Umowa"
        verbose_name_plural = "Umowy"


class ImportedEZZ(models.Model):
    EZZ_number = models.CharField(max_length=20, verbose_name="Numer EZZ")
    ordering_person = models.CharField(max_length=40, verbose_name="Osoba zamawiająca")
    creation_date = models.DateField(
        default=date(1990, 1, 1), verbose_name="Data utworzenia"
    )
    subject = models.CharField(max_length=5000, verbose_name="Temat")
    status = models.CharField(max_length=40, verbose_name="Status")
    suplier = models.CharField(max_length=300, null=True, verbose_name="Dostawca")
    source_of_financing = models.CharField(
        max_length=20, verbose_name="Źródło finansowania"
    )
    final_receiver = models.CharField(max_length=30, verbose_name="Odbiorca końcowy")
    current_acceptor = models.CharField(
        max_length=199, default="", null=True, verbose_name="Aktualny akceptor"
    )
    date_of_last_acceptance = models.DateField(
        default=date(1990, 1, 1), null=True, verbose_name="Data ostatniej akceptacji"
    )

    class Meta:
        verbose_name = "Zaimportowane EZZ"
        verbose_name_plural = "Zaimportowane EZZ"
