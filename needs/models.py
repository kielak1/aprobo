from django.db import models
from django.utils import timezone

from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericRelation

from general.models import (
    Crip,
    Rodzaje_uslug,
    Klasyfikacja_zmiany,
    Priorytet_inicjatywy,
    Sposob_zakupu,
    Poziomy_dostepnosci,
    Dostepnosci_rozwiazania,
    Rodzaj_inicjatywy,
    Sposob_wyceny,
    Pilnosc,
    Sections,
    Clients,
    Status_akceptacji,
    Note,
    zlecenia_kontrolingowe,
    uslugi,
)


class StatusNeed(models.Model):
    status = models.CharField(max_length=20, verbose_name="Status potrzeby")

    def __str__(self):
        return self.status

    class Meta:
        verbose_name = "Status potrzeby"
        verbose_name_plural = "Statusy potrzeby"


class LogNeed(models.Model):
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
        verbose_name = "Log potrzeby"
        verbose_name_plural = "Logi potrzeby"


class Needs(models.Model):
    status_potrzeby = models.ForeignKey(
        StatusNeed, on_delete=models.PROTECT, null=True, verbose_name="Status potrzeby"
    )
    status_akceptacji = models.ForeignKey(
        Status_akceptacji,
        on_delete=models.PROTECT,
        null=True,
        verbose_name="Status akceptacji",
    )
    status_akceptacji_infrastruktury = models.ForeignKey(
        Status_akceptacji,
        on_delete=models.PROTECT,
        null=True,
        related_name="infrastruktura",
        verbose_name="Status akceptacji infrastruktury",
    )
    status_akceptacji_sieci = models.ForeignKey(
        Status_akceptacji,
        on_delete=models.PROTECT,
        null=True,
        related_name="siec",
        verbose_name="Status akceptacji sieci",
    )
    status_akceptacji_finansow = models.ForeignKey(
        Status_akceptacji,
        on_delete=models.PROTECT,
        null=True,
        related_name="finanse",
        verbose_name="Status akceptacji finansów",
    )
    status_akceptacji_uslug = models.ForeignKey(
        Status_akceptacji,
        on_delete=models.PROTECT,
        null=True,
        related_name="uslugi",
        verbose_name="Status akceptacji usług",
    )

    link_do_clarity = models.CharField(
        max_length=400,
        default="",
        null=True,
        blank=True,
        verbose_name="Link do Clarity",
    )
    link_do_dokumentacji = models.CharField(
        max_length=400,
        default="",
        null=True,
        blank=True,
        verbose_name="Link do dokumentacji",
    )
    czy_dotyczy_architektury = models.BooleanField(
        default=None, null=True, blank=True, verbose_name="Czy dotyczy architektury?"
    )

    # Pola przekopiowywane z Idei
    subject = models.CharField(max_length=2000, blank=True, verbose_name="Temat")
    data_utworzenia = models.DateField(
        default=timezone.now, verbose_name="Data utworzenia"
    )
    komentarz = models.CharField(
        max_length=2303, null=True, default=None, blank=True, verbose_name="Komentarz"
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
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        verbose_name="Osoba prowadząca",
    )
    osoba_kontakowa_u_klienta = models.CharField(
        max_length=53,
        null=True,
        default=None,
        blank=True,
        verbose_name="Osoba kontaktowa u klienta",
    )

    rodzaj_inicjatywy = models.ForeignKey(
        Rodzaj_inicjatywy,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        verbose_name="Rodzaj inicjatywy",
    )
    opis = models.CharField(
        max_length=2612, null=True, default=None, blank=True, verbose_name="Opis"
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
        max_length=2029, null=True, default=None, blank=True, verbose_name="Produkty"
    )
    log = models.ManyToManyField(LogNeed, blank=True, default=None, verbose_name="Logi")
    komentarz_akceptujacego = models.CharField(
        max_length=400, default="", blank=True, verbose_name="Komentarz akceptującego"
    )
    odpowiedz_do_akceptujacego = models.CharField(
        max_length=400,
        default="",
        blank=True,
        verbose_name="Odpowiedź do akceptującego",
    )

    # Pola dodane po analizie karty zakupu
    pilnosc = models.ForeignKey(
        Pilnosc, on_delete=models.PROTECT, null=True, blank=True, verbose_name="Pilność"
    )
    odtworzeniowy = models.BooleanField(
        default=False, blank=True, verbose_name="Odtworzeniowy"
    )
    rozwojowy = models.BooleanField(default=False, blank=True, verbose_name="Rozwojowy")
    waluta = models.CharField(
        max_length=7, default="PLN", blank=True, verbose_name="Waluta"
    )

    # Infrastruktura
    czy_wymagana_jest_infrastruktura = models.BooleanField(
        default=False, blank=True, verbose_name="Czy wymagana jest infrastruktura?"
    )
    wymagane_komponenty_infrastruktury = models.CharField(
        max_length=200,
        default="",
        blank=True,
        verbose_name="Wymagane komponenty infrastruktury",
    )
    wymagane_parametry_infrastruktury = models.CharField(
        max_length=200,
        default="",
        blank=True,
        verbose_name="Wymagane parametry infrastruktury",
    )
    czy_wymagany_backup = models.BooleanField(
        default=False, blank=True, verbose_name="Czy wymagany jest backup?"
    )
    oczekiwania_wobec_backupu_infrastruktury = models.CharField(
        max_length=100,
        default="",
        blank=True,
        verbose_name="Oczekiwania wobec backupu infrastruktury",
    )
    wymagana_dostepnosc_rozwiazania = models.ForeignKey(
        Dostepnosci_rozwiazania,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        verbose_name="Wymagana dostępność rozwiązania",
    )
    sposob_realizacji_okien_serwisowych = models.CharField(
        max_length=200,
        default="",
        blank=True,
        verbose_name="Sposób realizacji okien serwisowych",
    )
    czy_wymagany_zakup_infrastruktury = models.BooleanField(
        default=False,
        blank=True,
        verbose_name="Czy wymagany jest zakup infrastruktury?",
    )
    zakres_infrastruktury_do_zakupu = models.CharField(
        max_length=200,
        default="",
        blank=True,
        verbose_name="Zakres infrastruktury do zakupu",
    )
    czy_wymagany_zakup_uslug_utrzymania_infrastruktury = models.BooleanField(
        default=False,
        blank=True,
        verbose_name="Czy wymagany jest zakup usług utrzymania infrastruktury?",
    )
    zakres_uslug_do_zakupu = models.CharField(
        max_length=200, default="", blank=True, verbose_name="Zakres usług do zakupu"
    )
    wymagania_dotyczace_monitorowania_infrastruktury = models.CharField(
        max_length=200,
        default="",
        blank=True,
        verbose_name="Wymagania dotyczące monitorowania infrastruktury",
    )
    czy_adminstratorzy_maja_kompetencje = models.BooleanField(
        default=False, blank=True, verbose_name="Czy administratorzy mają kompetencje?"
    )
    komentarz_infrastrukturalny = models.CharField(
        max_length=400,
        default="",
        blank=True,
        verbose_name="Komentarz infrastrukturalny",
    )
    odpowiedz_na_infrastrukturalny = models.CharField(
        max_length=400,
        default="",
        blank=True,
        verbose_name="Odpowiedź na komentarz infrastrukturalny",
    )

    # Sieć
    czy_beda_wymagane_uslugi_zewnetrzne = models.BooleanField(
        default=False, blank=True, verbose_name="Czy będą wymagane usługi zewnętrzne?"
    )
    zakres_uslug_zewnetrznych = models.CharField(
        max_length=200, default="", blank=True, verbose_name="Zakres usług zewnętrznych"
    )
    czy_bedzie_wymagany_load_balancer = models.BooleanField(
        default=False, blank=True, verbose_name="Czy będzie wymagany load balancer?"
    )
    komentarz_sieciowy = models.CharField(
        max_length=400, default="", blank=True, verbose_name="Komentarz sieciowy"
    )
    odpowiedz_na_sieciowy = models.CharField(
        max_length=400,
        default="",
        blank=True,
        verbose_name="Odpowiedź na komentarz sieciowy",
    )

    # Usługi
    czy_inicjatywa_dotyczy_uslug_w_ramach_umow_SLA = models.BooleanField(
        default=False,
        blank=True,
        verbose_name="Czy inicjatywa dotyczy usług w ramach umów SLA?",
    )
    czy_inicjatywa_wymaga_akceptacji_klienow = models.BooleanField(
        default=False,
        blank=True,
        verbose_name="Czy inicjatywa wymaga akceptacji klientów?",
    )
    czy_wymagana_bedzie_zmiana_w_kartach_uslug = models.BooleanField(
        default=False,
        blank=True,
        verbose_name="Czy będzie wymagana zmiana w kartach usług?",
    )
    komentarz_uslugowy = models.CharField(
        max_length=1086, default="", blank=True, verbose_name="Komentarz usługowy"
    )
    odpowiedz_na_uslugowy = models.CharField(
        max_length=1001,
        default="",
        blank=True,
        verbose_name="Odpowiedź na komentarz usługowy",
    )

    # Finanse
    czy_przedmiotem_jest_zakup_licencji_subskrypcji = models.BooleanField(
        default=False,
        blank=True,
        verbose_name="Czy przedmiotem jest zakup licencji subskrypcji?",
    )
    czy_licencje_sa_wieczyste = models.BooleanField(
        default=False, blank=True, verbose_name="Czy licencje są wieczyste?"
    )
    start_licencji = models.DateField(
        default=timezone.now, null=True, blank=True, verbose_name="Start licencji"
    )
    koniec_licencji = models.DateField(
        default=timezone.now, null=True, blank=True, verbose_name="Koniec licencji"
    )
    czas_licencji = models.IntegerField(
        default=0, null=True, blank=True, verbose_name="Czas licencji"
    )
    czy_licencje_sa_objete_uslugami_wsparcia_producenta = models.BooleanField(
        default=False,
        blank=True,
        verbose_name="Czy licencje są objęte usługami wsparcia producenta?",
    )
    start_wsparcia_licencji = models.DateField(
        default=timezone.now,
        null=True,
        blank=True,
        verbose_name="Start wsparcia licencji",
    )
    koniec_wsparcia_licencji = models.DateField(
        default=timezone.now,
        null=True,
        blank=True,
        verbose_name="Koniec wsparcia licencji",
    )
    okres_wsparcia_licencji = models.IntegerField(
        default=0, null=True, blank=True, verbose_name="Okres wsparcia licencji"
    )
    czy_koszt_wsparcia_jest_wliczony_w_wartosc_zakupionych_licencji = models.BooleanField(
        default=False,
        blank=True,
        verbose_name="Czy koszt wsparcia jest wliczony w wartość zakupionych licencji?",
    )
    czy_koszt_wsparcia_licencji_jest_wyodrebniany = models.BooleanField(
        default=False,
        blank=True,
        verbose_name="Czy koszt wsparcia licencji jest wyodrębniany?",
    )
    czy_zakup_wsparcia_licencji_dotyczy_licencji_juz_zakupionych = models.BooleanField(
        default=False,
        blank=True,
        verbose_name="Czy zakup wsparcia licencji dotyczy licencji już zakupionych?",
    )
    nazwy_i_ilosci_posiadanych_licencji = models.CharField(
        max_length=200,
        default="",
        blank=True,
        verbose_name="Nazwy i ilości posiadanych licencji",
    )
    czy_zakup_licencji_jest_powiazany_z_zakupem_uslug = models.BooleanField(
        default=False,
        blank=True,
        verbose_name="Czy zakup licencji jest powiązany z zakupem usług?",
    )

    czy_przedmiotem_sa_uslugi_wsparcia_producenta = models.BooleanField(
        default=False,
        null=True,
        blank=True,
        verbose_name="Czy przedmiotem są usługi wsparcia producenta?",
    )
    data_poczatku_uslug_wsparcia = models.DateField(
        default=timezone.now,
        null=True,
        blank=True,
        verbose_name="Data początku usług wsparcia",
    )
    data_konca_uslug_wsparcia = models.DateField(
        default=timezone.now,
        null=True,
        blank=True,
        verbose_name="Data końca usług wsparcia",
    )
    czas_trwania_wsparcia = models.IntegerField(
        default=0, null=True, blank=True, verbose_name="Czas trwania wsparcia"
    )
    czy_przedmiotem_zakupu_jest_sprzet = models.BooleanField(
        default=False,
        null=True,
        blank=True,
        verbose_name="Czy przedmiotem zakupu jest sprzęt?",
    )
    czy_w_ramach_zakupu_sprzetu_kupowane_sa_licencje = models.BooleanField(
        default=False,
        null=True,
        blank=True,
        verbose_name="Czy w ramach zakupu sprzętu kupowane są licencje?",
    )
    czy_licencje_sa_przypisane_do_sprzetu = models.BooleanField(
        default=False,
        null=True,
        blank=True,
        verbose_name="Czy licencje są przypisane do sprzętu?",
    )
    czy_koszt_licencji_bedzie_na_fakturze = models.BooleanField(
        default=False,
        null=True,
        blank=True,
        verbose_name="Czy koszt licencji będzie na fakturze?",
    )
    czy_w_ramach_sprzetu_sa_uslugi_wsparcia = models.BooleanField(
        default=False,
        blank=True,
        verbose_name="Czy w ramach sprzętu są usługi wsparcia?",
    )
    czy_uslugi_wsparcia_sa_przypisane_do_sprzetu = models.BooleanField(
        default=False,
        blank=True,
        verbose_name="Czy usługi wsparcia są przypisane do sprzętu?",
    )
    czy_koszt_uslug_wsparcia_bedzie_wyodrebniony_na_fakturze = models.BooleanField(
        default=False,
        blank=True,
        verbose_name="Czy koszt usług wsparcia będzie wyodrębniony na fakturze?",
    )
    czy_w_wyniku_zakupu_bedzie_wycofywany_stary_sprzet = models.BooleanField(
        default=False,
        blank=True,
        verbose_name="Czy w wyniku zakupu będzie wycofywany stary sprzęt?",
    )
    numery_seryjne_nazwy_wycofywnego_sprzetu = models.CharField(
        max_length=200,
        default="",
        blank=True,
        verbose_name="Numery seryjne/nazwy wycofywanego sprzętu",
    )
    czy_wymiana_sprzetu_na_nowy = models.BooleanField(
        default=False, blank=True, verbose_name="Czy wymiana sprzętu na nowy?"
    )
    czy_przedmiotem_zakupu_sa_uslugi_inne_niz_wsparcia = models.BooleanField(
        default=False,
        blank=True,
        verbose_name="Czy przedmiotem zakupu są usługi inne niż wsparcia?",
    )
    rodzaj_kupowanych_uslug = models.ManyToManyField(
        Rodzaje_uslug, blank=True, default=None, verbose_name="Rodzaj kupowanych usług"
    )

    czy_zakup_uslug_jest_powiazany_z_zakupem_sprzetu = models.BooleanField(
        default=False,
        blank=True,
        verbose_name="Czy zakup usług jest powiązany z zakupem sprzętu?",
    )
    czy_koszt_sprzetu_bedzie_wyodrebniony_na_fakturze = models.BooleanField(
        default=False,
        blank=True,
        verbose_name="Czy koszt sprzętu będzie wyodrębniony na fakturze?",
    )
    czy_zakup_usług_jest_powiazany_ze_wsparci_producenta = models.BooleanField(
        default=False,
        blank=True,
        verbose_name="Czy zakup usług jest powiązany ze wsparciem producenta?",
    )
    czy_koszt_uslug_wsparcia_producenta_bedzie_na_fakturze = models.BooleanField(
        default=False,
        blank=True,
        verbose_name="Czy koszt usług wsparcia producenta będzie na fakturze?",
    )
    czy_zakup_uslug_jest_zwiazany_z_zakupem_licencji = models.BooleanField(
        default=False,
        blank=True,
        verbose_name="Czy zakup usług jest związany z zakupem licencji?",
    )
    czy_koszt_licencji_bedzie_wyodrebniony_na_fakturze = models.BooleanField(
        default=False,
        blank=True,
        verbose_name="Czy koszt licencji będzie wyodrębniony na fakturze?",
    )
    czy_zadanie_zgodne_z_PDG = models.BooleanField(
        default=False, blank=True, verbose_name="Czy zadanie zgodne z PDG?"
    )
    czy_zadanie_zostalo_zaplanowane = models.BooleanField(
        default=False, blank=True, verbose_name="Czy zadanie zostało zaplanowane?"
    )
    pozycje_z_planu_CRIP = models.ManyToManyField(
        Crip, blank=True, default=None, verbose_name="Pozycje z planu CRIP"
    )
    pozycja_PDG = models.CharField(
        max_length=100, default="", blank=True, verbose_name="Pozycja PDG"
    )
    przyczyny_nie_zaplanowania_zadania = models.CharField(
        max_length=228,
        default="",
        blank=True,
        verbose_name="Przyczyny nie zaplanowania zadania",
    )

    capex = models.FloatField(
        max_length=19, default=0, null=True, blank=True, verbose_name="CAPEX"
    )
    opex = models.FloatField(
        max_length=19, default=0, null=True, blank=True, verbose_name="OPEX"
    )

    sposob_okreslenia_budzetu = models.ForeignKey(
        Sposob_wyceny,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        verbose_name="Sposób określenia budżetu",
    )
    harmonogram_platnosci_OPEX = models.CharField(
        max_length=200,
        default="",
        blank=True,
        verbose_name="Harmonogram płatności OPEX",
    )
    harmonogram_platnosci_CAPEX = models.CharField(
        max_length=246,
        default="",
        blank=True,
        verbose_name="Harmonogram płatności CAPEX",
    )
    numer_zadania_inwestycyjnego = models.CharField(
        max_length=20,
        default="",
        blank=True,
        verbose_name="Numer zadania inwestycyjnego",
    )
    komentarz_finansowy = models.CharField(
        max_length=400, default="", blank=True, verbose_name="Komentarz finansowy"
    )
    odpowiedz_na_finansowy = models.CharField(
        max_length=449,
        default="",
        blank=True,
        verbose_name="Odpowiedź na komentarz finansowy",
    )

    # Ogólne
    czy_inicjatywa_dotyczy_aplikacji = models.BooleanField(
        default=False, blank=True, verbose_name="Czy inicjatywa dotyczy aplikacji?"
    )
    oczekiwany_poziom_dostepnosci = models.ForeignKey(
        Poziomy_dostepnosci,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        verbose_name="Oczekiwany poziom dostępności",
    )

    godziny_dostepnosci_rozwiazania = models.CharField(
        max_length=50,
        default="",
        blank=True,
        verbose_name="Godziny dostępności rozwiązania",
    )
    oczekiwany_czas_reakcji = models.IntegerField(
        default=0, blank=True, verbose_name="Oczekiwany czas reakcji"
    )
    oczekiwany_czas_przywrocenia = models.IntegerField(
        default=0, blank=True, verbose_name="Oczekiwany czas przywrócenia"
    )
    klasyfikacja_w_sensie_procedury_jakosci = models.ForeignKey(
        Klasyfikacja_zmiany,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        verbose_name="Klasyfikacja w sensie procedury jakości",
    )

    notes = GenericRelation(Note, verbose_name="Notatki")

    zlecenia_kontrolingowe = models.ManyToManyField(
        zlecenia_kontrolingowe, blank=True, verbose_name="Zlecenia kontrolingowe"
    )
    uslugi = models.ManyToManyField(uslugi, blank=True, verbose_name="Usługi")

    komentarz_architekta = models.CharField(
        max_length=2987,
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

    def __str__(self):
        return f"{self.id} {self.subject}"

    def get_link_short(self):
        return f"edit_need_short/?need_id={self.id}"

    def get_powiazane(self):
        return "-------------"

    class Meta:
        verbose_name = "Potrzeba"
        verbose_name_plural = "Potrzeby"
