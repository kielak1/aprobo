from django.db import models
from django.utils import timezone
from django.db import transaction

from django.contrib.auth.models import User
from needs.models import Needs
from general.models import (
    Sections,
    Clients,
    Status_akceptacji,
    Sposob_wyceny,
    Rodzaj_inicjatywy,
    Priorytet_inicjatywy,
    Sposob_zakupu,
)
from django.contrib.contenttypes.fields import GenericRelation
from general.models import Note


class StatusIdei(models.Model):
    status = models.CharField(max_length=20, verbose_name="Status")

    def __str__(self):
        return self.status

    class Meta:
        verbose_name = "Status idei"
        verbose_name_plural = "Statusy idei"


class LogIdea(models.Model):
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
        verbose_name = "Log idei"
        verbose_name_plural = "Logi idei"


class Ideas(models.Model):
    status_idei = models.ForeignKey(
        StatusIdei, on_delete=models.PROTECT, null=True, verbose_name="Status Idei"
    )
    status_akceptacji = models.ForeignKey(
        Status_akceptacji,
        on_delete=models.PROTECT,
        null=True,
        verbose_name="Status Akceptacji",
    )
    subject = models.CharField(max_length=2000, verbose_name="Temat")
    czy_dotyczy_architektury = models.BooleanField(
        default=True, null=True, blank=True, verbose_name="Czy dotyczy architektury?"
    )
    data_utworzenia = models.DateField(
        default=timezone.now, verbose_name="Data utworzenia"
    )
    komentarz = models.CharField(
        max_length=425, null=True, default=None, blank=True, verbose_name="Komentarz"
    )
    wymagana_data_realizacji = models.DateField(
        default=None, null=True, blank=True, verbose_name="Wymagana data realizacji"
    )
    orientacynjy_budzet = models.FloatField(
        max_length=19,
        default=0,
        null=True,
        blank=True,
        verbose_name="Orientacyjny budżet",
    )
    section = models.ForeignKey(
        Sections, on_delete=models.PROTECT, null=True, blank=True, verbose_name="Dział"
    )
    client = models.ForeignKey(
        Clients, on_delete=models.PROTECT, null=True, blank=True, verbose_name="Klient"
    )
    osoba_prowadzaca = models.ForeignKey(
        User,
        related_name="idea_koordynator",
        on_delete=models.PROTECT,
        null=True,
        verbose_name="Osoba prowadząca",
    )
    inicjator = models.ForeignKey(
        User,
        related_name="idea_inicjator",
        on_delete=models.PROTECT,
        null=True,
        verbose_name="Inicjator",
    )
    osoba_kontakowa_u_klienta = models.CharField(
        max_length=53,
        null=True,
        default=None,
        blank=True,
        verbose_name="Osoba kontaktowa u klienta",
    )
    needs = models.ManyToManyField(
        Needs, blank=True, default=None, verbose_name="Potrzeby"
    )
    do_kiedy_zawieszona = models.DateField(
        default=timezone.now, null=True, blank=True, verbose_name="Do kiedy zawieszona?"
    )
    rodzaj_inicjatywy = models.ForeignKey(
        Rodzaj_inicjatywy,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        verbose_name="Rodzaj Inicjatywy",
    )
    opis = models.CharField(
        max_length=2301, null=True, default=None, blank=True, verbose_name="Opis"
    )
    uzasadnienie = models.CharField(
        max_length=2503,
        null=True,
        default=None,
        blank=True,
        verbose_name="Uzasadnienie",
    )
    priorytet = models.ForeignKey(
        Priorytet_inicjatywy,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        verbose_name="Priorytet",
    )
    wlasciciel_biznesowy = models.CharField(
        max_length=85,
        null=True,
        default=None,
        blank=True,
        verbose_name="Właściciel biznesowy",
    )
    proponowany_sposob_realizacji = models.ForeignKey(
        Sposob_zakupu,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        verbose_name="Proponowany sposób realizacji",
    )
    produkty = models.CharField(
        max_length=1986,
        null=True,
        default=None,
        help_text="Opis produktów, które zostaną wytworzone w wyniku realizacji pomysłu",
        blank=True,
        verbose_name="Produkty",
    )
    log = models.ManyToManyField(LogIdea, blank=True, default=None, verbose_name="Logi")
    powiazane_idee = models.ManyToManyField(
        "self", symmetrical=True, blank=True, verbose_name="Powiązane idee"
    )
    komentarz_akceptujacego = models.CharField(
        max_length=300, default="", blank=True, verbose_name="Komentarz akceptującego"
    )
    notes = GenericRelation(Note, verbose_name="Notatki")
    komentarz_architekta = models.CharField(
        max_length=300,
        default="",
        blank=True,
        null=True,
        verbose_name="Komentarz architekta",
    )
    odpowiedz_koordynatora_do_architekta = models.CharField(
        max_length=2997,
        default="",
        blank=True,
        null=True,
        verbose_name="Odpowiedź koordynatora do architekta",
    )
    atrapa = models.CharField(
        max_length=2, default="", null=True, blank=True, verbose_name="Atrapa"
    )

    def __str__(self):
        return f"{self.id} {self.subject}"

    def get_link_short(self):
        return f"edit_idea_short/?idea_id={self.id}"

    def get_powiazane(self):
        return "-------------"

    def clone_idea(self):
        with transaction.atomic():
            cloned_idea = Ideas.objects.create(
                status_idei=StatusIdei.objects.get(status="nowa"),
                status_akceptacji=Status_akceptacji.objects.get(akceptacja="niegotowe"),
                subject=self.subject + f" - klon pomysłu {self.id}",
                czy_dotyczy_architektury=self.czy_dotyczy_architektury,
                data_utworzenia=self.data_utworzenia,
                komentarz=self.komentarz,
                orientacynjy_budzet=self.orientacynjy_budzet,
                section=self.section,
                client=self.client,
                osoba_prowadzaca=self.osoba_prowadzaca,
                inicjator=self.inicjator,
                osoba_kontakowa_u_klienta=self.osoba_kontakowa_u_klienta,
                do_kiedy_zawieszona=self.do_kiedy_zawieszona,
                rodzaj_inicjatywy=self.rodzaj_inicjatywy,
                opis=self.opis,
                uzasadnienie=self.uzasadnienie,
                priorytet=self.priorytet,
                wlasciciel_biznesowy=self.wlasciciel_biznesowy,
                proponowany_sposob_realizacji=self.proponowany_sposob_realizacji,
                produkty=self.produkty,
                atrapa=self.atrapa,
                komentarz_architekta="",
                odpowiedz_koordynatora_do_architekta="",
                komentarz_akceptujacego="",
            )

            cloned_idea.powiazane_idee.add(self)
            self.powiazane_idee.add(cloned_idea)
            cloned_idea.save()

        return cloned_idea

    class Meta:
        verbose_name = "Pomysł"
        verbose_name_plural = "Pomysły"
