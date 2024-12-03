from django.db import models
from datetime import date

from django.contrib.auth.models import User

from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


class Parametry(models.Model):
    """
    Model reprezentujący parametry.

    :param nazwa: Nazwa parametru
    :type nazwa: str
    :param opis: Opis parametru
    :type opis: str
    :param num: Wartość numeryczna parametru
    :type num: int
    :param str: Warto ść tekstowa parametru
    :type str: str
    """

    nazwa = models.CharField(max_length=40, default="", null=True)
    opis = models.CharField(max_length=400, default="", null=True)
    num = models.IntegerField(default=0, null=True)
    str = models.CharField(max_length=400, default="", null=True)

    class Meta:
        verbose_name = _("Parametr")
        verbose_name_plural = _("Parametry")

    def __str__(self):
        """
        Zwraca sklejoną reprezentację nazwy, numerycznej wartości i opisu, przyciętą do 40 znaków.

        :return: Sformatowany ciąg znaków
        :rtype: str
        """
        result = f"{self.nazwa} ({self.num}) [{self.str}] {self.opis}"
        return result[:40]


class Note(models.Model):
    content = models.CharField(max_length=400, default="", null=True)
    timestamp = models.DateTimeField(default=timezone.now)
    user = models.ForeignKey(User, on_delete=models.PROTECT, null=True)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey("content_type", "object_id")

    class Meta:
        verbose_name = _("Notatka")
        verbose_name_plural = _("Notatki")

    def __str__(self):
        return f"Note by {self.user.username if self.user else 'Unknown'} on {self.timestamp}"


class Sections(models.Model):
    name = models.CharField(max_length=70)
    short_name = models.CharField(max_length=10)
    manager = models.CharField(max_length=30, default="")
    users = models.ManyToManyField(User, related_name="custom_models")
    kierownik = models.ForeignKey(
        User,
        related_name="sections_kierownik",
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        default=None,
    )

    class Meta:
        verbose_name = _("Dział")
        verbose_name_plural = _("Działy")

    def __str__(self):
        return self.short_name


class Clients(models.Model):
    name = models.CharField(max_length=70, default="")
    short_name = models.CharField(max_length=10, default="")
    users = models.ManyToManyField(User, related_name="clients_custom_models")
    opiekun = models.ForeignKey(
        User,
        related_name="clients_opiekun",
        on_delete=models.PROTECT,
        null=True,
        blank=False,
        default=None,
        limit_choices_to={"groups__name": "idea_allocator", "is_active": True},
    )

    class Meta:
        verbose_name = _("Klient")
        verbose_name_plural = _("Klienci")

    def __str__(self):
        return self.name


class Status_procesu(models.Model):
    status = models.CharField(max_length=20, default="")

    class Meta:
        verbose_name = _("Status procesu")
        verbose_name_plural = _("Statusy procesu")

    def __str__(self):
        return self.status


class Status_akceptacji(models.Model):
    akceptacja = models.CharField(max_length=20, default="")

    class Meta:
        verbose_name = _("Status akceptacji")
        verbose_name_plural = _("Statusy akceptacji")

    def __str__(self):
        return self.akceptacja


class Pilnosc(models.Model):
    pilnosc = models.CharField(max_length=20, default="")

    class Meta:
        verbose_name = _("Pilność")
        verbose_name_plural = _("Pilności")

    def __str__(self):
        return self.pilnosc


class Crip(models.Model):
    crip_id = models.CharField(max_length=40)
    nazwa_projektu = models.CharField(max_length=700, default="")
    jednostka = models.CharField(max_length=16, default="", null=True)
    sekcja = models.CharField(max_length=16, default="", null=True)

    class Meta:
        verbose_name = _("Crip")
        verbose_name_plural = _("Cripy")

    def __str__(self):
        # Przycięcie nazwa_projektu do 50 znaków
        trimmed_project_name = self.nazwa_projektu[:50]

        # Zwróć string składający się z crip_id, znaku '-' oraz przyciętej nazwy projektu
        return f"{self.crip_id} - {trimmed_project_name}"

    def get_link_short(self):
        return f"edit_crip_short/?crip_id={self.id}"

    def suma_budzetu(self):
        return "+++"


class Sposob_zakupu(models.Model):
    sposob_zakupu = models.CharField(max_length=500, default="")

    class Meta:
        verbose_name = _("Sposób zakupu")
        verbose_name_plural = _("Sposoby zakupu")

    def __str__(self):
        return self.sposob_zakupu


class Acceptor(models.Model):
    opiniujacy = models.CharField(max_length=80, default="")

    class Meta:
        verbose_name = _("Opiniujący")
        verbose_name_plural = _("Opiniujący")

    def __str__(self):
        return self.opiniujacy


class Sposob_wyceny(models.Model):
    sposob_wyceny = models.CharField(max_length=40, default="")

    class Meta:
        verbose_name = _("Sposób wyceny")
        verbose_name_plural = _("Sposoby wyceny")

    def __str__(self):
        return self.sposob_wyceny


class Zgodnosc_mapy(models.Model):
    zgodnosc_mapy = models.CharField(max_length=40, default="")

    class Meta:
        verbose_name = _("Zgodność mapy")
        verbose_name_plural = _("Zgodności map")

    def __str__(self):
        return self.zgodnosc_mapy


class Rodzaj_inicjatywy(models.Model):
    rodzaj_inicjatywy = models.CharField(max_length=60, default="")

    class Meta:
        verbose_name = _("Rodzaj inicjatywy")
        verbose_name_plural = _("Rodzaje inicjatyw")

    def __str__(self):
        return self.rodzaj_inicjatywy


class Priorytet_inicjatywy(models.Model):
    priorytet_inicjatywy = models.CharField(max_length=20, default="")

    class Meta:
        verbose_name = _("Priorytet inicjatywy")
        verbose_name_plural = _("Priorytety inicjatyw")

    def __str__(self):
        return self.priorytet_inicjatywy


class Rodzaje_uslug(models.Model):
    usluga = models.CharField(max_length=80)

    class Meta:
        verbose_name = _("Rodzaj usługi")
        verbose_name_plural = _("Rodzaje usług")

    def __str__(self):
        return self.usluga


class Klasyfikacja_zmiany(models.Model):
    zmiana = models.CharField(max_length=40)

    class Meta:
        verbose_name = _("Klasyfikacja zmiany")
        verbose_name_plural = _("Klasyfikacje zmiany")

    def __str__(self):
        return self.zmiana


class Poziomy_dostepnosci(models.Model):
    poziom = models.CharField(max_length=40)

    class Meta:
        verbose_name = _("Poziom dostępności")
        verbose_name_plural = _("Poziomy dostępności")

    def __str__(self):
        return self.poziom


class Dostepnosci_rozwiazania(models.Model):
    poziom = models.CharField(max_length=40)

    class Meta:
        verbose_name = _("SLA")
        verbose_name_plural = _("SLA")

    def __str__(self):
        return self.poziom


class MaileDoWyslania(models.Model):
    """
    MaileDoWyslania służy do przechowywania mail-i (powiadomień) o istotnych zdarzeniach w systemie
    Rekordy w tej tabeli tworzone są na bieżąco a wyysyłanie odbywa się okresowo i wtedy rekordy są usuwane.
    """

    subject = models.CharField(
        max_length=200, help_text="Temat maila, który zostanie wysłany"
    )
    body = models.CharField(
        max_length=40000, help_text="Treść maila, który zostanie wysłany"
    )
    recipient = models.CharField(
        max_length=100, help_text="Adresat maila, który zostanie wysłany"
    )
    sender = models.CharField(
        max_length=100,
        default="avantic@pgnig.pl",
        help_text="Nadawca maila, który zostanie wysłany",
    )

    class Meta:
        verbose_name = _("Mail do wysłania")
        verbose_name_plural = _("Maile do wysłania")

    def __str__(self):
        """
        Zwraca sklejoną reprezentację adresata i tematu, przyciętą do 40 znaków.

        :return: Sformatowany ciąg znaków
        :rtype: str
        """
        combined_str = f"{self.recipient} - {self.subject}"
        return combined_str[:60]
