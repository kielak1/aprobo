from django.db import models
from datetime import date
from general.models import (
    Sections,
    Clients,
    Status_procesu,
    Status_akceptacji,
    Pilnosc,
    Crip,
    Acceptor,
    Sposob_wyceny,
    Zgodnosc_mapy,
    Sposob_zakupu,
)
from needs.models import Needs
from django.contrib.auth.models import User
from django.utils import timezone
from django.contrib.contenttypes.fields import GenericRelation
from general.models import Note
from django.utils.translation import gettext_lazy as _


class EZZ(models.Model):
    EZZ_number = models.CharField(max_length=20, unique=True, verbose_name="Numer EZZ")
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
        max_length=201,
        default="",
        null=True,
        verbose_name="Bieżący akceptor",
        blank=True,
    )
    date_of_last_acceptance = models.DateField(
        default=date(1990, 1, 1), null=True, verbose_name="Data ostatniej akceptacji"
    )
    nieistotny = models.BooleanField(
        default=False, blank=True, verbose_name="Nieistotny"
    )

    class Meta:
        verbose_name = _("Wniosek EZZ")
        verbose_name_plural = _("Wnioski EZZ")

    def __str__(self):
        return f"{self.EZZ_number} - {self.subject}"


class LogPurchase(models.Model):
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
        verbose_name = _("Log zakupu")
        verbose_name_plural = _("Logi zakupów")


def domyslny_status_roboczy():
    status = Status_procesu.objects.get(status="roboczy")
    return status.pk


def domyslny_status_procesu():
    status = Status_procesu.objects.get(status="roboczy")
    return status.pk


def domyslny_status_akceptacji():
    status = Status_akceptacji.objects.get(akceptacja="niegotowe")
    return status.pk


class Purchases(models.Model):
    data_utworzenia = models.DateField(
        default=timezone.now, blank=True, verbose_name="Data utworzenia"
    )
    osoba_prowadzaca = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        verbose_name="Osoba prowadząca",
    )
    przedmiot_zakupu = models.CharField(
        max_length=2000, default="", blank=True, verbose_name="Przedmiot zakupu"
    )
    uzasadnienie_zakupu = models.CharField(
        max_length=5022, default="", blank=True, verbose_name="Uzasadnienie zakupu"
    )
    zakres_zakupu = models.CharField(
        max_length=3001, default="", blank=True, verbose_name="Zakres zakupu"
    )
    cel_i_produkty = models.CharField(
        max_length=2000, default="", blank=True, verbose_name="Cel i produkty"
    )
    komentarz = models.CharField(
        max_length=400, default="", blank=True, verbose_name="Komentarz"
    )
    ezz = models.ForeignKey(
        EZZ, on_delete=models.PROTECT, null=True, blank=True, verbose_name="Wniosek EZZ"
    )
    section = models.ForeignKey(
        Sections, on_delete=models.PROTECT, null=True, blank=True, verbose_name="Dział"
    )
    client = models.ForeignKey(
        Clients, on_delete=models.PROTECT, null=True, blank=True, verbose_name="Klient"
    )
    link_do_ezz = models.CharField(
        max_length=200, default="", null=True, blank=True, verbose_name="Link do EZZ"
    )

    status_procesu = models.ForeignKey(
        Status_procesu,
        on_delete=models.PROTECT,
        default=domyslny_status_roboczy,
        null=True,
        verbose_name="Status procesu",
    )
    status_akceptacji = models.ForeignKey(
        Status_akceptacji,
        on_delete=models.PROTECT,
        null=True,
        default=domyslny_status_akceptacji,
        verbose_name="Status akceptacji",
    )
    pilnosc = models.ForeignKey(
        Pilnosc, on_delete=models.PROTECT, null=True, blank=True, verbose_name="Pilność"
    )

    odtworzeniowy = models.BooleanField(
        default=False, blank=True, verbose_name="Odtworzeniowy"
    )
    rozwojowy = models.BooleanField(default=False, blank=True, verbose_name="Rozwojowy")
    planowany_termin_platnosci = models.CharField(
        max_length=81, default="", blank=True, verbose_name="Planowany termin płatności"
    )
    waluta = models.CharField(
        max_length=7, default="PLN", blank=True, verbose_name="Waluta"
    )
    budzet_capex_netto = models.FloatField(
        default=0, blank=True, null=True, verbose_name="Budżet CAPEX netto"
    )
    budzet_opex_netto = models.FloatField(
        default=0, blank=True, null=True, verbose_name="Budżet OPEX netto"
    )

    crip_id = models.ManyToManyField(
        Crip, blank=True, default=None, verbose_name="Pozycje CRIP"
    )

    sposob_wyceny = models.ForeignKey(
        Sposob_wyceny,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        verbose_name="Sposób wyceny",
    )
    id_sap = models.CharField(
        max_length=60, default="", blank=True, verbose_name="ID SAP"
    )
    zgodnosc_mapy = models.ForeignKey(
        Zgodnosc_mapy,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        verbose_name="Zgodność mapy",
    )
    dostawca = models.CharField(
        max_length=191, default="", blank=True, verbose_name="Dostawca"
    )
    sposob_zakupu = models.ForeignKey(
        Sposob_zakupu,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        verbose_name="Sposób zakupu",
    )

    acceptors = models.ManyToManyField(
        Acceptor, blank=True, default=None, verbose_name="Akceptorzy"
    )
    komentarz_akceptujacego = models.CharField(
        max_length=300, default="", blank=True, verbose_name="Komentarz akceptującego"
    )

    need = models.ForeignKey(
        Needs,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="purchases",
        verbose_name="Potrzeba",
    )

    log = models.ManyToManyField(
        LogPurchase, blank=True, default=None, verbose_name="Logi"
    )

    notes = GenericRelation(Note, verbose_name="Notatki")
    wymagana_data_zawarcia_umowy = models.DateField(
        default=None, null=True, blank=True, verbose_name="Wymagana data zawarcia umowy"
    )
    atrapa = models.CharField(
        max_length=3, default="", null=True, blank=True, verbose_name="Atrapa"
    )

    def get_link(self):
        return f"edit_purchase/?purchase_id={self.id}"

    def __str__(self):
        return f"{self.id} {self.przedmiot_zakupu}"

    def get_link_short(self):
        return f"edit_purchase_short/?purchase_id={self.id}"

    def get_powiazane(self):
        return "-------------"

    class Meta:
        verbose_name = _("Zakup")
        verbose_name_plural = _("Zakupy")


class Postepowania(models.Model):
    numer_SRM_SAP = models.CharField(max_length=21, verbose_name="Numer SRM/SAP")  # 0
    numer_ZZ = models.CharField(max_length=22, verbose_name="Numer ZZ")  # 1
    opis_zapotrzebowania = models.CharField(
        max_length=1121, verbose_name="Opis zapotrzebowania"
    )  # 2
    priorytet = models.CharField(
        max_length=13, null=True, verbose_name="Priorytet"
    )  # 3
    status_SRM = models.CharField(
        max_length=19, null=True, verbose_name="Status SRM"
    )  # 4
    zlecajacy = models.CharField(
        max_length=28, null=True, verbose_name="Zlecający"
    )  # 5
    kupiec = models.CharField(max_length=36, null=True, verbose_name="Kupiec")  # 6
    status_biura = models.CharField(
        max_length=62, null=True, verbose_name="Status biura"
    )  # 7
    data_wprowadzenia = models.DateField(
        default=None, null=True, verbose_name="Data wprowadzenia"
    )  # 8
    connect = models.CharField(
        max_length=40, null=True, default="", verbose_name="Status na Conect"
    )  # 10

    class Meta:
        verbose_name = _("Postępowanie")
        verbose_name_plural = _("Postępowania")
