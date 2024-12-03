from datetime import datetime
import logging
from urllib.parse import urlparse

from dal import autocomplete
from django import forms
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.shortcuts import render, redirect
from django.urls import resolve, Resolver404
from django.views.decorators.csrf import csrf_protect

from contracts.models import Contracts
from general.common_context import common_context
from general.common_view import get_current_url
from general.konwertuj_wartosci_do_porownania import konwertuj_wartosci_do_porownania
from general.mail import utworz_mail_do_wyslania, wyslij_mail_do_grupy
from general.models import (
    Sections,
    Status_akceptacji,
    Clients,
    Rodzaje_uslug,
    Crip,
    Sposob_wyceny,
    Rodzaj_inicjatywy,
    Priorytet_inicjatywy,
    Sposob_zakupu,
    Klasyfikacja_zmiany,
    Poziomy_dostepnosci,
    Dostepnosci_rozwiazania,
    Pilnosc,
    Note,
    Resolution,
    Stamp,
)
from general.parametry import get_param_int
from ideas.models import Ideas
from needs.models import Needs, StatusNeed, LogNeed
from purchases.models import Purchases, EZZ
from general.widgets import (
    CharCountTextArea,
    create_char_count_field,
    create_float_field,
)

logger = logging.getLogger("avantic")


def create_comm_field(field_name, rows=3, cols=116, required=False):
    return create_char_count_field(
        field_name=field_name,
        rows=rows,
        cols=cols,
        model=Needs,
        required=required,
        attrs={
            "style": "background-color: #ffff99;",
        },
    )


def create_resp_field(field_name, rows=3, cols=116, required=False):
    return create_char_count_field(
        field_name=field_name,
        rows=rows,
        cols=cols,
        model=Needs,
        required=required,
        attrs={
            "style": "background-color: #0fff99;",
        },
    )

def create_stand_field(field_name, rows=3, cols=116, required=False):
    return create_char_count_field(
        field_name=field_name,
        rows=rows,
        cols=cols,
        model=Needs,
        required=required,
    )

class DynamicneedsFormShort(forms.ModelForm):
    link_do_clarity = forms.CharField(
        widget=forms.Textarea(attrs={"rows": 1, "cols": 100}), required=False
    )
    link_do_dokumentacji = forms.CharField(
        widget=forms.Textarea(attrs={"rows": 1, "cols": 100}), required=False
    )
    status_potrzeby = forms.ModelChoiceField(
        label="Status potrzeby", queryset=StatusNeed.objects.all(), required=False
    )
    status_akceptacji = forms.ModelChoiceField(
        label="Status akceptacji",
        queryset=Status_akceptacji.objects.all(),
        required=False,
    )

    subject = create_stand_field("subject", required=True)

    data_utworzenia = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={"type": "date", "style": "width: 13ch;"}),
    )

    komentarz = create_stand_field("komentarz")

    wymagana_data_realizacji = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={"type": "date", "style": "width: 13ch;"}),
    )

    orientacynjy_budzet = create_float_field(label="Orientacyjny budżet")

    section = forms.ModelChoiceField(
        label="Dział", queryset=Sections.objects.all(), required=False
    )
    client = forms.ModelChoiceField(
        label="Klient", queryset=Clients.objects.all(), required=False
    )
    osoba_prowadzaca = forms.ModelChoiceField(
        label="Właściciel potrzeby", queryset=User.objects.all(), required=False
    )
    osoba_kontakowa_u_klienta = forms.CharField(
        label="Osoba kontaktowa w biznesie",
        widget=forms.Textarea(attrs={"rows": 1, "cols": 22}),
        required=False,
    )

    rodzaj_inicjatywy = forms.ModelChoiceField(
        label="Rodzaj inicjatywy",
        queryset=Rodzaj_inicjatywy.objects.all(),
        required=False,
    )

    opis = create_stand_field("opis")
    uzasadnienie = create_stand_field("uzasadnienie")
    priorytet = forms.ModelChoiceField(
        label="Priorytet", queryset=Priorytet_inicjatywy.objects.all(), required=False
    )
    wlasciciel_biznesowy = forms.CharField(
        label="Opis",
        widget=forms.Textarea(attrs={"rows": 1, "cols": 30}),
        required=False,
    )

    produkty = create_stand_field("produkty")

    proponowany_sposob_realizacji = forms.ModelChoiceField(
        queryset=Sposob_zakupu.objects.all(),
        widget=forms.Select(attrs={"style": "width: 800px;", "size": 1}),
        required=False,
    )
    czy_wymagana_jest_infrastruktura = forms.BooleanField(
        label="Rodzaj inicjatywy",
        required=False,  # Ustawiamy na False, aby domyślnie było False (czyli niezaznaczone)
        widget=forms.CheckboxInput(
            attrs={"class": "custom-checkbox"}
        ),  # Dodatkowe atrybuty dla wyglądu
    )

    wymagane_komponenty_infrastruktury = create_stand_field(
        "wymagane_komponenty_infrastruktury", cols=94
    )
    wymagane_parametry_infrastruktury = create_stand_field(
        "wymagane_parametry_infrastruktury", cols=94
    )
    czy_wymagany_backup = forms.BooleanField(
        label="Rodzaj inicjatywy",
        required=False,
        widget=forms.CheckboxInput(attrs={"class": "custom-checkbox"}),
    )

    oczekiwania_wobec_backupu_infrastruktury = create_stand_field(
        "oczekiwania_wobec_backupu_infrastruktury", cols=94
    )
    wymagana_dostepnosc_rozwiazania = forms.ModelChoiceField(
        queryset=Dostepnosci_rozwiazania.objects.all(), required=False
    )

    sposob_realizacji_okien_serwisowych = create_stand_field(
        "sposob_realizacji_okien_serwisowych", cols=94
    )
    czy_wymagany_zakup_infrastruktury = forms.BooleanField(
        label="Rodzaj inicjatywy",
        required=False,
        widget=forms.CheckboxInput(attrs={"class": "custom-checkbox"}),
    )

    zakres_infrastruktury_do_zakupu = create_stand_field(
        "zakres_infrastruktury_do_zakupu", cols=94
    )
    czy_wymagany_zakup_uslug_utrzymania_infrastruktury = forms.BooleanField(
        label="Rodzaj inicjatywy",
        required=False,
        widget=forms.CheckboxInput(attrs={"class": "custom-checkbox"}),
    )

    zakres_uslug_do_zakupu = create_stand_field("zakres_uslug_do_zakupu", cols=94)
    wymagania_dotyczace_monitorowania_infrastruktury = create_stand_field(
        "wymagania_dotyczace_monitorowania_infrastruktury", cols=94
    )
    czy_adminstratorzy_maja_kompetencje = forms.BooleanField(
        label="Rodzaj inicjatywy",
        required=False,
        widget=forms.CheckboxInput(attrs={"class": "custom-checkbox"}),
    )

    czy_beda_wymagane_uslugi_zewnetrzne = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={"class": "custom-checkbox"}),
    )

    zakres_uslug_zewnetrznych = create_stand_field("zakres_uslug_zewnetrznych", cols=94)
    czy_bedzie_wymagany_load_balancer = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={"class": "custom-checkbox"}),
    )
    czy_inicjatywa_wymaga_akceptacji_klienow = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={"class": "custom-checkbox"}),
    )
    czy_wymagana_bedzie_zmiana_w_kartach_uslug = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={"class": "custom-checkbox"}),
    )
    czy_przedmiotem_jest_zakup_licencji_subskrypcji = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={"class": "custom-checkbox"}),
    )
    czy_licencje_sa_wieczyste = forms.BooleanField(
        required=False, widget=forms.CheckboxInput(attrs={"class": "custom-checkbox"})
    )
    start_licencji = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={"type": "date", "style": "width: 15ch;"}),
    )
    koniec_licencji = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={"type": "date", "style": "width: 15ch;"}),
    )
    czas_licencji = forms.IntegerField(
        required=False, widget=forms.TextInput(attrs={"style": "width: 40px;"})
    )

    czy_licencje_sa_objete_uslugami_wsparcia_producenta = forms.BooleanField(
        required=False, widget=forms.CheckboxInput(attrs={"class": "custom-checkbox"})
    )

    start_wsparcia_licencji = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={"type": "date", "style": "width: 15ch;"}),
    )
    koniec_wsparcia_licencji = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={"type": "date", "style": "width: 15ch;"}),
    )
    okres_wsparcia_licencji = forms.IntegerField(
        required=False, widget=forms.TextInput(attrs={"style": "width: 40px;"})
    )

    czy_koszt_wsparcia_jest_wliczony_w_wartosc_zakupionych_licencji = (
        forms.BooleanField(
            required=False,
            widget=forms.CheckboxInput(attrs={"class": "custom-checkbox"}),
        )
    )
    czy_koszt_wsparcia_licencji_jest_wyodrebniany = forms.BooleanField(
        required=False, widget=forms.CheckboxInput(attrs={"class": "custom-checkbox"})
    )
    czy_zakup_wsparcia_licencji_dotyczy_licencji_juz_zakupionych = forms.BooleanField(
        required=False, widget=forms.CheckboxInput(attrs={"class": "custom-checkbox"})
    )

    nazwy_i_ilosci_posiadanych_licencji = create_stand_field(
        "nazwy_i_ilosci_posiadanych_licencji", cols=93, rows=3
    )

    czy_zakup_licencji_jest_powiazany_z_zakupem_usług = forms.BooleanField(
        required=False, widget=forms.CheckboxInput(attrs={"class": "custom-checkbox"})
    )

    czy_przedmiotem_sa_uslugi_wsparcia_producenta = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={"class": "custom-checkbox"}),
    )
    data_poczatku_uslug_wsparcia = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={"type": "date", "style": "width: 15ch;"}),
    )
    data_konca_uslug_wsparcia = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={"type": "date", "style": "width: 15ch;"}),
    )
    czas_trwania_wsparcia = forms.IntegerField(
        required=False, widget=forms.TextInput(attrs={"style": "width: 40px;"})
    )
    czy_przedmiotem_zakupu_jest_sprzet = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={"class": "custom-checkbox"}),
    )
    czy_w_ramach_zakupu_sprzetu_kupowane_sa_licencje = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={"class": "custom-checkbox"}),
    )
    czy_licencje_sa_przypisane_do_sprzetu = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={"class": "custom-checkbox"}),
    )
    czy_koszt_licencji_bedzie_na_fakturze = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={"class": "custom-checkbox"}),
    )
    czy_w_ramach_sprzetu_sa_uslugi_wsparcia = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={"class": "custom-checkbox"}),
    )
    czy_uslugi_wsparcia_sa_przypisane_do_sprzetu = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={"class": "custom-checkbox"}),
    )
    czy_koszt_uslug_wsparcia_bedzie_wyodrebniony_na_fakturze = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={"class": "custom-checkbox"}),
    )
    czy_w_wyniku_zakupu_bedzie_wycofywany_stary_sprzet = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={"class": "custom-checkbox"}),
    )

    numery_seryjne_nazwy_wycofywnego_sprzetu = create_stand_field(
        "numery_seryjne_nazwy_wycofywnego_sprzetu", cols=94
    )
    czy_wymiana_sprzetu_na_nowy = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={"class": "custom-checkbox"}),
    )
    czy_przedmiotem_zakupu_sa_uslugi_inne_niz_wsparcia = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={"class": "custom-checkbox"}),
    )
    czy_zakup_uslug_jest_powiazany_z_zakupem_sprzetu = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={"class": "custom-checkbox"}),
    )
    czy_koszt_sprzetu_bedzie_wyodrebniony_na_fakturze = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={"class": "custom-checkbox"}),
    )
    czy_zakup_usług_jest_powiazany_ze_wsparci_producenta = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={"class": "custom-checkbox"}),
    )
    czy_koszt_uslug_wsparcia_producenta_bedzie_na_fakturze = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={"class": "custom-checkbox"}),
    )
    czy_zakup_uslug_jest_zwiazany_z_zakupem_licencji = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={"class": "custom-checkbox"}),
    )
    czy_koszt_licencji_bedzie_wyodrebniony_na_fakturze = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={"class": "custom-checkbox"}),
    )
    czy_zadanie_zgodne_z_PDG = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={"class": "custom-checkbox"}),
    )
    czy_zadanie_zostalo_zaplanowane = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={"class": "custom-checkbox"}),
    )
    pozycja_PDG = forms.CharField(
        widget=forms.Textarea(attrs={"rows": 1, "cols": 60}), required=False
    )

    capex = create_float_field(label="capex")
    opex = create_float_field(label="opex")
    
    sposob_okreslenia_budzetu = forms.ModelChoiceField(
        label="Sposob_wyceny", queryset=Sposob_wyceny.objects.all(), required=False
    )

    harmonogram_platnosci_OPEX = create_stand_field(
        "harmonogram_platnosci_OPEX", cols=97
    )
    harmonogram_platnosci_CAPEX = create_stand_field(
        "harmonogram_platnosci_CAPEX", cols=97
    )
    numer_zadania_inwestycyjnego = forms.CharField(
        label="nr zadania",
        widget=forms.Textarea(attrs={"rows": 1, "cols": 20}),
        required=False,
    )
    przyczyny_nie_zaplanowania_zadania = create_stand_field(
        "przyczyny_nie_zaplanowania_zadania", cols=94
    )
    oczekiwany_poziom_dostepnosci = forms.ModelChoiceField(
        queryset=Poziomy_dostepnosci.objects.all(), required=False
    )

    czy_inicjatywa_dotyczy_aplikacji = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={"class": "custom-checkbox"}),
    )

    godziny_dostepnosci_rozwiazania = forms.CharField(
        widget=forms.Textarea(attrs={"rows": 1, "cols": 30}), required=False
    )
    oczekiwany_czas_reakcji = forms.IntegerField(
        required=False, widget=forms.TextInput(attrs={"style": "width: 40px;"})
    )
    oczekiwany_czas_przywrocenia = forms.IntegerField(
        required=False, widget=forms.TextInput(attrs={"style": "width: 40px;"})
    )
    klasyfikacja_w_sensie_procedury_jakosci = forms.ModelChoiceField(
        queryset=Klasyfikacja_zmiany.objects.all(), required=False
    )

    # definicje pól dodanych po analizie kart zakupów
    pilnosc = forms.ModelChoiceField(
        label="Pilność", queryset=Pilnosc.objects.all(), required=False
    )
    odtworzeniowy = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={"class": "custom-checkbox"}),
    )
    rozwojowy = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={"class": "custom-checkbox"}),
    )
    waluta = forms.CharField(
        widget=forms.Textarea(
            attrs={
                "rows": 1,
                "cols": 5,
                "title": "Wpisz trzyliterowy skrót walutu wielkimi literami",
            }
        ),
        required=False,
    )
    komentarz_finansowy = create_comm_field("komentarz_finansowy")
    komentarz_infrastrukturalny = create_comm_field("komentarz_infrastrukturalny")
    komentarz_sieciowy = create_comm_field("komentarz_sieciowy")
    komentarz_uslugowy = create_comm_field("komentarz_uslugowy")
    komentarz_akceptujacego = create_comm_field("komentarz_akceptujacego")
    odpowiedz_do_akceptujacego = create_resp_field("odpowiedz_do_akceptujacego")
    odpowiedz_na_infrastrukturalny = create_resp_field("odpowiedz_na_infrastrukturalny")
    odpowiedz_na_sieciowy = create_resp_field("odpowiedz_na_sieciowy")
    odpowiedz_na_uslugowy = create_resp_field("odpowiedz_na_uslugowy")
    odpowiedz_na_finansowy = create_resp_field("odpowiedz_na_finansowy")
    komentarz_architekta = create_comm_field("komentarz_architekta")
    odpowiedz_koordynatora_do_architekta = create_resp_field(
        "odpowiedz_koordynatora_do_architekta"
    )
    odlinkowany_purchase = forms.ModelChoiceField(
        queryset=Purchases.objects.none(),  # Zostanie ustawiony w __init__
        required=False,
        label="Odłącz zakup",
        help_text="Wybierz zakup do odłączenia",
        widget=forms.Select(attrs={"style": "width: 830px;"}),
    )

    podlinkowany_purchase = forms.ModelChoiceField(
        queryset=Purchases.objects.filter(need__isnull=True),
        required=False,
        label="Podlinkuj zakup",
        help_text="Wybierz zakup do podlinkowania",
        widget=forms.Select(attrs={"style": "width: 830px;"}),
    )

    ezz_do_powiazania = forms.ModelChoiceField(
        queryset=EZZ.objects.filter(purchases__isnull=True),
        required=False,
        label="EZZ do powiązania",
        help_text="Wybierz EZZ, które ma zostać powiązane z nowym zakupem.",
        widget=forms.Select(attrs={"style": "width: 830px;"}),
    )

    def __init__(
        self,
        *args,
        display_fields=None,
        is_need_allocator=False,
        is_need_viewer=False,
        is_need_editor=False,
        **kwargs,
    ):
        super(DynamicneedsFormShort, self).__init__(*args, **kwargs)

        instance = kwargs.get("instance", None)
        if instance and instance.pk:
            self.fields["odlinkowany_purchase"].queryset = instance.purchases.all()
        self.fields["ezz_do_powiazania"].queryset = EZZ.objects.filter(
            purchases__isnull=True
        )

        if display_fields:
            for field_name in self.fields.copy().keys():
                if field_name not in display_fields:
                    self.fields.pop(field_name)
        if not is_need_editor:
            for field_name, field in self.fields.items():
                field.widget.attrs["readonly"] = True

    class Meta:
        model = Needs
        fields = "__all__"

        widgets = {
            "uslugi": autocomplete.ModelSelect2Multiple(
                url="uslugi-autocomplete",
                attrs={
                    "class": "selector",
                    "data-placeholder": "Wybierz usługi (numer)",
                },
            ),
            "zlecenia_kontrolingowe": autocomplete.ModelSelect2Multiple(
                url="zlecenia-autocomplete",
                attrs={
                    "class": "selector",
                    "data-placeholder": "Wybierz zlecenia (numer)",
                },
            ),
            "pozycje_z_planu_CRIP": autocomplete.ModelSelect2Multiple(
                url="crips-autocomplete",
                attrs={
                    "class": "selector",
                    "data-placeholder": "Wybierz numer crip",
                },
            ),
            "rodzaj_kupowanych_uslug": autocomplete.ModelSelect2Multiple(
                url="rodzaje-uslug-autocomplete",
                attrs={
                    "class": "selector",
                    "data-placeholder": "Wybierz usługę",
                },
            ),
        }


def sklonuj_need_to_purchase(need, purchase):
    purchase.przedmiot_zakupu = need.subject
    purchase.id_sap = need.numer_zadania_inwestycyjnego
    purchase.budzet_capex_netto = need.capex
    purchase.budzet_opex_netto = need.opex
    purchase.sposob_wyceny = need.sposob_okreslenia_budzetu
    purchase.uzasadnienie_zakupu = need.uzasadnienie
    purchase.cel_i_produkty = need.produkty
    purchase.zakres_zakupu = need.opis
    purchase.sposob_zakupu = need.proponowany_sposob_realizacji
    wspolne_pola = [
        "section",
        "client",
        "osoba_prowadzaca",
        "pilnosc",
        "odtworzeniowy",
        "rozwojowy",
        "waluta",
    ]
    for pole in wspolne_pola:
        setattr(purchase, pole, getattr(need, pole))
    purchase.save()
    pozycje_z_planu_CRIP = need.pozycje_z_planu_CRIP.all()
    for pozycja in pozycje_z_planu_CRIP:
        purchase.crip_id.add(pozycja)


def validate_and_return_url(request, default_url="/ideas/wszystkiepomysly/"):
    full_url = request.session.get("need_edit", default_url)
    path = urlparse(
        full_url
    ).path  # Usuwa parametry zapytania, zostawiając tylko ścieżkę

    try:
        resolve(path)  # Sprawdza, czy ścieżka jest poprawna
        return full_url  # Zwraca pełny URL, włącznie z parametrami zapytania
    except Resolver404:
        return default_url  # Zwraca URL domyślny, jeśli podany URL jest nieprawidłowy


@csrf_protect
def return_need_path(request):
    return_page = validate_and_return_url(request)
    if "need_edit" in request.session:
        del request.session["need_edit"]
    return return_page


def get_contracts_ideas_and_purchases(need_instance):

    ideas = Ideas.objects.filter(needs=need_instance).exclude(needs=None)
    contract_list = Contracts.objects.filter(ideas__in=ideas).distinct()
    purchase_list = need_instance.purchases.all()

    return contract_list, ideas, purchase_list


def get_need_context(form, need_instance, request):
    is_need_allocator = False
    is_need_editor = False
    is_need_acceptor = False
    is_need_recommender = False

    if request.user.is_authenticated:
        if request.user.groups.filter(name="need_editor").exists():
            is_need_editor = True
        if request.user.groups.filter(name="need_allocator").exists():
            is_need_allocator = True
            is_need_editor = True
        if request.user.groups.filter(name="need_acceptor").exists():
            is_need_acceptor = True
            is_need_editor = True
        if request.user.groups.filter(name="need_recommender").exists():
            is_need_recommender = True
            is_need_editor = True
    status_akceptacji = "niegotowe"
    status_need = "nowe"
    if need_instance.status_potrzeby:
        status_need = need_instance.status_potrzeby.status
    if need_instance.status_akceptacji:
        status_akceptacji = need_instance.status_akceptacji.akceptacja
    if need_instance.section:
        sekcja = need_instance.section
    data_utworzenia = need_instance.data_utworzenia
    osoba_prowadzaca = need_instance.osoba_prowadzaca
    priorytet = need_instance.priorytet

    status_akceptacji_infrastruktury = "niegotowe"
    status_akceptacji_sieci = "niegotowe"
    status_akceptacji_finansow = "niegotowe"
    status_akceptacji_uslug = "niegotowe"
    if need_instance.status_akceptacji_infrastruktury:
        status_akceptacji_infrastruktury = (
            need_instance.status_akceptacji_infrastruktury.akceptacja
        )
    if need_instance.status_akceptacji_sieci:
        status_akceptacji_sieci = need_instance.status_akceptacji_sieci.akceptacja
    if need_instance.status_akceptacji_finansow:
        status_akceptacji_finansow = need_instance.status_akceptacji_finansow.akceptacja
    if need_instance.status_akceptacji_uslug:
        status_akceptacji_uslug = need_instance.status_akceptacji_uslug.akceptacja

    if (
        status_akceptacji_infrastruktury == "zaakceptowane"
        and status_akceptacji_sieci == "zaakceptowane"
        and status_akceptacji_uslug == "zaakceptowane"
        and status_akceptacji_finansow == "zaakceptowane"
        and (
            status_need == "wstrzymane"
            or status_need == "realizowana"
            or status_need == "analiza"
        )
    ):
        is_acceptable = True
    else:
        is_acceptable = False

    lista_uslug = []
    for x in need_instance.rodzaj_kupowanych_uslug.all():
        lista_uslug.append(x)
    cripy = []
    for x in need_instance.pozycje_z_planu_CRIP.all():
        cripy.append(x)

    uslugi = []
    for x in need_instance.uslugi.all():
        uslugi.append(x)

    zlecenia_kontrolingowe = []
    for x in need_instance.zlecenia_kontrolingowe.all():
        zlecenia_kontrolingowe.append(x)

    freeze_all = False
    freeze_infra = False
    freeze_siec = False
    freeze_uslugi = False
    freeze_finanse = False
    if (
        status_need == "rada architektury"
        or status_akceptacji == "zaakceptowane"
        or status_akceptacji == "do akceptacji"
        or (
            not is_need_acceptor
            and not is_need_allocator
            and not is_need_editor
            and not is_need_recommender
        )
    ):
        freeze_all = True
        freeze_infra = True
        freeze_siec = True
        freeze_uslugi = True
        freeze_finanse = True

    if (
        status_akceptacji_infrastruktury == "zaakceptowane"
        or status_akceptacji_infrastruktury == "do akceptacji"
    ):
        freeze_infra = True
    if (
        status_akceptacji_sieci == "zaakceptowane"
        or status_akceptacji_sieci == "do akceptacji"
    ):
        freeze_siec = True
    if (
        status_akceptacji_finansow == "zaakceptowane"
        or status_akceptacji_finansow == "do akceptacji"
    ):
        freeze_finanse = True
    if (
        status_akceptacji_uslug == "zaakceptowane"
        or status_akceptacji_uslug == "do akceptacji"
    ):
        freeze_uslugi = True

    notes = Note.objects.filter(
        content_type=ContentType.objects.get_for_model(Needs),
        object_id=need_instance.id,
    ).order_by("-timestamp")

    liczba_logow = get_param_int("log_entry", 20)
    recent_logs = need_instance.log.all().order_by("-data")[:liczba_logow]

    contract_list, ideas, purchase_list = get_contracts_ideas_and_purchases(
        need_instance
    )
    dal_media = autocomplete.Select2().media

    freeze_arch_resp = True

    if status_akceptacji == "do poprawy":
        freeze_arch_resp = False

    # Oblicz różnicę w widoku
    # Sprawdzenie, czy składniki są typu liczbowego, w przeciwnym wypadku przypisanie im wartości 0
    orientacynjy_budzet = (
        need_instance.orientacynjy_budzet
        if isinstance(need_instance.orientacynjy_budzet, (int, float))
        else 0
    )
    opex = need_instance.opex if isinstance(need_instance.opex, (int, float)) else 0
    capex = need_instance.capex if isinstance(need_instance.capex, (int, float)) else 0
    # Obliczenie różnicy
    diff = orientacynjy_budzet - opex - capex
    # Obliczenie wartości absolutnej różnicy
    diff_abs = abs(diff)

    context = {
        "form": form,
        "diff": diff,
        "diff_abs": diff_abs,
        "freeze_arch_resp": freeze_arch_resp,
        "contract_list": contract_list,
        "status_need": status_need,
        "status_akceptacji": status_akceptacji,
        "sekcja": sekcja,
        "data_utworzenia": data_utworzenia,
        "osoba_prowadzaca": osoba_prowadzaca,
        "priorytet": priorytet,
        "ideas": ideas,
        "need_instance": need_instance,
        "lista_uslug": lista_uslug,
        "cripy": cripy,
        "status_akceptacji_infrastruktury": status_akceptacji_infrastruktury,
        "status_akceptacji_sieci": status_akceptacji_sieci,
        "status_akceptacji_finansow": status_akceptacji_finansow,
        "status_akceptacji_uslug": status_akceptacji_uslug,
        "is_acceptable": is_acceptable,
        "purchase_list": purchase_list,
        "freeze_all": freeze_all,
        "freeze_infra": freeze_infra,
        "freeze_siec": freeze_siec,
        "freeze_uslugi": freeze_uslugi,
        "freeze_finanse": freeze_finanse,
        "recent_logs": recent_logs,
        "notes": notes,
        "dal_media": dal_media,
        "uslugi": uslugi,
        "zlecenia_kontrolingowe": zlecenia_kontrolingowe,
    }

    context.update(common_context(request))
    return context


def logujneeds(need_instance, request, dzialanie):
    wpis_do_logu = LogNeed()
    if request.user.is_authenticated:
        wpis_do_logu.user = request.user
    wpis_do_logu.akcja = dzialanie
    wpis_do_logu.save()
    need_instance.log.add(wpis_do_logu)


def zapisz_needs(form, need_instance, request):
    """
    Zapisuje formularz, a jeśli dane zostały zmienione, loguje zmiany.

    Args:
        form: Formularz do zapisania.
        need_instance: Instancja kontraktu związana z formularzem.
        request: Obiekt żądania HTTP zawierający informacje o użytkowniku.
    """
    instance = form.save(commit=False)
    changed_fields = []

    # Sprawdzenie zmian w polach formularza
    for field in form.changed_data:
        old_value = form.initial.get(field)
        new_value = form.cleaned_data[field]

        old_value, new_value, czy_konwersja = konwertuj_wartosci_do_porownania(
            old_value, new_value
        )

        # Porównanie starych i nowych wartości
        if old_value != new_value:
            if czy_konwersja:
                change_description = f"{field} zmienione na {new_value} z {old_value}"
            else:
                change_description = f"{field} zmienione na {new_value}"
            change_description = (
                (change_description[:297] + "...")
                if len(change_description) > 300
                else change_description
            )
            logujneeds(need_instance, request, change_description)
            changed_fields.append(field)

    # Jeśli są zmiany, zapisz instancję do bazy danych
    if changed_fields:
        instance.save()

    # Zapisz pola typu ModelMultipleChoiceField
    if form.cleaned_data.get("pozycje_z_planu_CRIP"):
        instance.pozycje_z_planu_CRIP.set(form.cleaned_data["pozycje_z_planu_CRIP"])
        instance.save()

    if form.cleaned_data.get("rodzaj_kupowanych_uslug"):
        instance.rodzaj_kupowanych_uslug.set(
            form.cleaned_data["rodzaj_kupowanych_uslug"]
        )
        instance.save()

    if form.cleaned_data.get("uslugi"):
        instance.uslugi.set(form.cleaned_data["uslugi"])
        instance.save()

    if form.cleaned_data.get("zlecenia_kontrolingowe"):
        instance.zlecenia_kontrolingowe.set(form.cleaned_data["zlecenia_kontrolingowe"])
        instance.save()


@csrf_protect
def edit_need_short(request):
    stamp = Stamp.objects.create(
        nazwa="need_edit",
        opis="Czas wykonania funkcji edycji formularza potrzeby (edit_need_short)",
        sekwencja="edit_need_short",
        typ_zdarzenia="",
    )
    if not request.GET:  # Jeśli brak parametrów w adresie URL
        return redirect('dashboard')  # Przekierowanie na nazwę widoku 'dashboard'
    if "need_edit" not in request.session:
        request.session["need_edit"] = request.META.get(
            "HTTP_REFERER", "/needs/wszystkiepotrzeby/"
        )

    need_id = request.GET.get("need_id")

    need_instance = Needs.objects.get(pk=need_id)
    target_url = f"/needs/wszystkiepotrzeby/edit_need_short/?need_id={need_instance.id}"

    context = get_need_context("", need_instance, request)

    is_need_allocator = context["is_need_allocator"]
    is_need_editor = context["is_need_editor"]
    is_need_viewer = context["is_need_viewer"]

    is_need_acceptor = context["is_need_acceptor"]
    is_need_recommender = context["is_need_recommender"]
    is_need_infra_acceptor = context["is_need_infra_acceptor"]
    is_need_net_acceptor = context["is_need_net_acceptor"]
    is_need_finanse_acceptor = context["is_need_finanse_acceptor"]
    is_need_service_acceptor = context["is_need_service_acceptor"]

    is_superuser = context["is_superuser"]
    is_recommender = context["is_recommender"]

    status_akceptacji_finansow = context["status_akceptacji_finansow"]
    status_akceptacji_sieci = context["status_akceptacji_sieci"]
    status_akceptacji_infrastruktury = context["status_akceptacji_infrastruktury"]
    status_akceptacji_uslug = context["status_akceptacji_uslug"]
    status_akceptacji = context["status_akceptacji"]

    freeze_all = context["freeze_all"]
    freeze_infra = context["freeze_infra"]
    freeze_siec = context["freeze_siec"]
    freeze_uslugi = context["freeze_uslugi"]
    freeze_finanse = context["freeze_finanse"]
    freeze_arch_resp = context["freeze_arch_resp"]

    target_if_no_rights = f"/account/login/?next={request.path}?need_id={need_id}"
    if request.user.is_authenticated:
        if not is_need_viewer:
            return redirect(target_if_no_rights)
    else:
        return redirect(target_if_no_rights)

    display_fields = []
    if not freeze_all:
        display_fields.extend(
            [
                "subject",
                "komentarz",
                "wymagana_data_realizacji",
                "opis",
                "uzasadnienie",
                "produkty",
                "orientacynjy_budzet",
                "client",
                "osoba_kontakowa_u_klienta",
                "rodzaj_inicjatywy",
                "wlasciciel_biznesowy",
                "czy_inicjatywa_dotyczy_aplikacji",
                "pilnosc",
                "priorytet",
                "proponowany_sposob_realizacji",
                "godziny_dostepnosci_rozwiazania",
                "oczekiwany_czas_reakcji",
                "oczekiwany_czas_przywrocenia",
                "klasyfikacja_w_sensie_procedury_jakosci",
                "odpowiedz_do_akceptujacego",
                "uslugi",
                "zlecenia_kontrolingowe",
            ]
        )

    if not freeze_arch_resp:
        display_fields.extend(
            [
                "odpowiedz_koordynatora_do_architekta",
            ]
        )

    if not freeze_finanse:
        display_fields.extend(
            [
                "odpowiedz_na_finansowy",
                "czy_przedmiotem_jest_zakup_licencji_subskrypcji",
                "czy_licencje_sa_wieczyste",
                "start_licencji",
                "koniec_licencji",
                "czas_licencji",
                "czy_licencje_sa_objete_uslugami_wsparcia_producenta",
                "start_wsparcia_licencji",
                "koniec_wsparcia_licencji",
                "okres_wsparcia_licencji",
                "czy_koszt_wsparcia_jest_wliczony_w_wartosc_zakupionych_licencji",
                "czy_koszt_wsparcia_licencji_jest_wyodrebniany",
                "czy_zakup_wsparcia_licencji_dotyczy_licencji_juz_zakupionych",
                "nazwy_i_ilosci_posiadanych_licencji",
                "czy_zakup_licencji_jest_powiazany_z_zakupem_usług",
                "czy_przedmiotem_sa_uslugi_wsparcia_producenta",
                "czy_przedmiotem_zakupu_jest_sprzet",
                "czy_w_ramach_zakupu_sprzetu_kupowane_sa_licencje",
                "czy_licencje_sa_przypisane_do_sprzetu",
                "czy_koszt_licencji_bedzie_na_fakturze",
                "czy_w_ramach_sprzetu_sa_uslugi_wsparcia",
                "czy_uslugi_wsparcia_sa_przypisane_do_sprzetu",
                "czy_koszt_uslug_wsparcia_bedzie_wyodrebniony_na_fakturze",
                "czy_w_wyniku_zakupu_bedzie_wycofywany_stary_sprzet",
                "czy_wymiana_sprzetu_na_nowy",
                "czy_przedmiotem_zakupu_sa_uslugi_inne_niz_wsparcia",
                "rodzaj_kupowanych_uslug",
                "czy_zakup_uslug_jest_powiazany_z_zakupem_sprzetu",
                "czy_koszt_sprzetu_bedzie_wyodrebniony_na_fakturze",
                "czy_zakup_usług_jest_powiazany_ze_wsparci_producenta",
                "czy_koszt_uslug_wsparcia_producenta_bedzie_na_fakturze",
                "czy_zakup_uslug_jest_zwiazany_z_zakupem_licencji",
                "czy_koszt_licencji_bedzie_wyodrebniony_na_fakturze",
                "czy_zadanie_zgodne_z_PDG",
                "czy_zadanie_zostalo_zaplanowane",
                "pozycje_z_planu_CRIP",
                "sposob_okreslenia_budzetu",
                "rozwojowy",
                "odtworzeniowy",
                "data_poczatku_uslug_wsparcia",
                "data_konca_uslug_wsparcia",
                "numery_seryjne_nazwy_wycofywnego_sprzetu",
                "przyczyny_nie_zaplanowania_zadania",
                "capex",
                "opex",
                "harmonogram_platnosci_OPEX",
                "harmonogram_platnosci_CAPEX",
                "numer_zadania_inwestycyjnego",
                "pozycja_PDG",
                "waluta",
                "czas_trwania_wsparcia",
            ]
        )

    if not freeze_infra:
        display_fields.extend(
            [
                "odpowiedz_na_infrastrukturalny",
                "czy_wymagana_jest_infrastruktura",
                "wymagane_komponenty_infrastruktury",
                "wymagane_parametry_infrastruktury",
                "czy_wymagany_zakup_infrastruktury",
                "zakres_infrastruktury_do_zakupu",
                "czy_wymagany_zakup_uslug_utrzymania_infrastruktury",
                "zakres_uslug_do_zakupu",
                "czy_wymagany_backup",
                "oczekiwania_wobec_backupu_infrastruktury",
                "wymagana_dostepnosc_rozwiazania",
                "sposob_realizacji_okien_serwisowych",
                "wymagania_dotyczace_monitorowania_infrastruktury",
                "czy_adminstratorzy_maja_kompetencje",
            ]
        )

    if not freeze_siec:
        display_fields.extend(
            [
                "odpowiedz_na_sieciowy",
                "czy_beda_wymagane_uslugi_zewnetrzne",
                "czy_bedzie_wymagany_load_balancer",
                "zakres_uslug_zewnetrznych",
            ]
        )

    if not freeze_uslugi:
        display_fields.extend(
            [
                "odpowiedz_na_uslugowy",
                "czy_inicjatywa_dotyczy_uslug_w_ramach_umow_SLA",
                "czy_inicjatywa_wymaga_akceptacji_klienow",
                "czy_wymagana_bedzie_zmiana_w_kartach_uslug",
            ]
        )

    display_fields.extend(
        [
            "link_do_clarity",
            "link_do_dokumentacji",
        ]
    )

    if is_need_editor:
        display_fields.extend(
            ["odlinkowany_purchase", "podlinkowany_purchase", "ezz_do_powiazania"]
        )

    if is_need_recommender:
        display_fields.append("komentarz_architekta")

    if status_akceptacji_finansow == "do akceptacji" and is_need_finanse_acceptor:
        display_fields.append("komentarz_finansowy")
    if status_akceptacji_sieci == "do akceptacji" and is_need_net_acceptor:
        display_fields.append("komentarz_sieciowy")
    if status_akceptacji_infrastruktury == "do akceptacji" and is_need_infra_acceptor:
        display_fields.append("komentarz_infrastrukturalny")
    if status_akceptacji_uslug == "do akceptacji" and is_need_service_acceptor:
        display_fields.append("komentarz_uslugowy")

    if status_akceptacji == "do akceptacji" and is_need_acceptor:
        display_fields.append("komentarz_akceptujacego")

    if is_need_allocator and not freeze_all:
        display_fields.append("section")
        display_fields.append("osoba_prowadzaca")

    if request.method == "POST":
        form = DynamicneedsFormShort(
            request.POST,
            instance=need_instance,
            display_fields=display_fields,
            is_need_allocator=is_need_allocator,
            is_need_editor=is_need_editor,
            is_need_viewer=is_need_viewer,
        )

        if "Anuluj" in request.POST:
            return redirect(return_need_path(request))

        if form.is_valid():

            if "update_resolution" in request.POST and is_recommender:
                res_value = request.POST["resolution_text"]
                # Pobieramy najnowsze postanowienie (Resolution) związane z Needs, z najnowszym posiedzeniem (Meeting)
                latest_resolution = (
                    Resolution.objects.filter(need=need_instance)
                    .order_by("-meeting__meeting_date")
                    .first()
                )
                if latest_resolution:
                    # Aktualizacja pola resolution_text dla wybranego postanowienia
                    latest_resolution.resolution_text = res_value
                    latest_resolution.save()
                return redirect(target_url)

            elif "notka" in request.POST and is_need_editor:
                tresc = request.POST.get("tresc_notatki")
                user = request.user
                if len(tresc) > Note._meta.get_field("content").max_length:
                    return redirect(target_url)
                if tresc:
                    note = Note.objects.create(
                        content=tresc,
                        user=user,
                        content_type=ContentType.objects.get_for_model(Needs),
                        object_id=need_instance.id,
                    )
                return redirect(target_url)

            elif "unlinkj_purchase" in request.POST and is_need_editor:
                odlinkowany_purchase = form.cleaned_data.get("odlinkowany_purchase")
                if odlinkowany_purchase:
                    odlinkowany_purchase.need = None
                    odlinkowany_purchase.save()
                    logujneeds(need_instance, request, "unlink zakup")
                    utworz_mail_do_wyslania(
                        need_instance.osoba_prowadzaca,
                        f"Od potrzeby {need_instance.id} został odłączony zakup {odlinkowany_purchase.id}",
                        get_current_url(request),
                    )

            elif "link_purchase" in request.POST and is_need_editor:
                podlinkowany_purchase = form.cleaned_data.get("podlinkowany_purchase")
                if podlinkowany_purchase:
                    podlinkowany_purchase.need = need_instance
                    podlinkowany_purchase.save()
                    logujneeds(need_instance, request, "link zakup")
                    utworz_mail_do_wyslania(
                        need_instance.osoba_prowadzaca,
                        f"Do potrzeby {need_instance.id} został podłączony zakup {podlinkowany_purchase.id}",
                        get_current_url(request),
                    )

            elif "link_EZZ" in request.POST and is_need_editor:
                # Tworzymy nowy Purchases tylko jeśli wybrano EZZ
                ezz_do_powiazania = form.cleaned_data.get("ezz_do_powiazania")
                if ezz_do_powiazania:
                    podlinkowany_purchase = Purchases.objects.create(
                        ezz=ezz_do_powiazania,
                        need=need_instance,  # Przypisujemy do aktualnego Needs
                    )
                    sklonuj_need_to_purchase(need_instance, podlinkowany_purchase)
                    logujneeds(need_instance, request, "link ezz")
                    utworz_mail_do_wyslania(
                        need_instance.osoba_prowadzaca,
                        f"Do potrzeby {need_instance.id} został podłączony zakup {podlinkowany_purchase.id}",
                        get_current_url(request),
                    )

            elif "realizuj" in request.POST and is_need_editor:
                need_instance.status_potrzeby = StatusNeed.objects.get(
                    status="realizowana"
                )
                logujneeds(need_instance, request, "Realizuj")
                utworz_mail_do_wyslania(
                    need_instance.osoba_prowadzaca,
                    f"Potrzeba {need_instance.id} przeszła do fazy realizacji",
                    get_current_url(request),
                )

            elif "zamknij" in request.POST and is_need_editor:
                need_instance.status_potrzeby = StatusNeed.objects.get(
                    status="zamknięta"
                )
                logujneeds(need_instance, request, "zamknij")
                utworz_mail_do_wyslania(
                    need_instance.osoba_prowadzaca,
                    f"Potrzeba {need_instance.id} została porzucona",
                    get_current_url(request),
                )

            elif "zakoncz" in request.POST and is_need_editor:
                need_instance.status_potrzeby = StatusNeed.objects.get(
                    status="zrealizowana"
                )
                logujneeds(need_instance, request, "zakończ")
                utworz_mail_do_wyslania(
                    need_instance.osoba_prowadzaca,
                    f"Potrzeba {need_instance.id} została zrealizowana",
                    get_current_url(request),
                )

            elif "przywroc" in request.POST and is_need_editor:
                need_instance.status_potrzeby = StatusNeed.objects.get(
                    status="realizowana"
                )
                logujneeds(need_instance, request, "przywróć")
                utworz_mail_do_wyslania(
                    need_instance.osoba_prowadzaca,
                    f"Potrzeba {need_instance.id} została przywrócona",
                    get_current_url(request),
                )

            elif "gotowe" in request.POST and is_need_recommender:
                need_instance.status_akceptacji = Status_akceptacji.objects.get(
                    akceptacja="do akceptacji"
                )
                need_instance.status_potrzeby = StatusNeed.objects.get(
                    status="realizowana"
                )
                logujneeds(need_instance, request, "gotowe do akceptacji")
                utworz_mail_do_wyslania(
                    need_instance.osoba_prowadzaca,
                    f"Potrzeba {need_instance.id} skierowana do akceptacji",
                    get_current_url(request),
                )
                wyslij_mail_do_grupy(
                    "need_acceptor",
                    f"Podejmij decyzję dotyczącą potrzeby {need_instance.id}",
                    get_current_url(request),
                )

            elif "akcept" in request.POST and is_need_acceptor:
                need_instance.status_akceptacji = Status_akceptacji.objects.get(
                    akceptacja="zaakceptowane"
                )
                logujneeds(need_instance, request, "zaakceptowane")
                utworz_mail_do_wyslania(
                    need_instance.osoba_prowadzaca,
                    f"Potrzeba {need_instance.id} została zaakceptowana",
                    get_current_url(request),
                )

            elif "arch_yes" in request.POST and is_need_editor:
                need_instance.czy_dotyczy_architektury = True
                logujneeds(need_instance, request, "Dotyczy architektury")
                utworz_mail_do_wyslania(
                    need_instance.osoba_prowadzaca,
                    f"Potrzeba {need_instance.id} dotyczy architektury",
                    get_current_url(request),
                )

            elif "arch_no" in request.POST and is_need_editor:
                need_instance.czy_dotyczy_architektury = False
                logujneeds(need_instance, request, "Nie dotyczy architektury")
                utworz_mail_do_wyslania(
                    need_instance.osoba_prowadzaca,
                    f"Potrzeba {need_instance.id} nie dotyczy architektury",
                    get_current_url(request),
                )

            elif "Reset" in request.POST and is_need_editor:
                need_instance.status_potrzeby = StatusNeed.objects.get(
                    status="realizowana"
                )
                need_instance.status_akceptacji = Status_akceptacji.objects.get(
                    akceptacja="niegotowe"
                )
                logujneeds(need_instance, request, "Reset")
                utworz_mail_do_wyslania(
                    need_instance.osoba_prowadzaca,
                    f"Potrzeba {need_instance.id} została zresetowana",
                    get_current_url(request),
                )

            elif "cofnij_akceptacje" in request.POST and is_need_editor:
                need_instance.status_akceptacji = Status_akceptacji.objects.get(
                    akceptacja="niegotowe"
                )
                need_instance.status_potrzeby = StatusNeed.objects.get(
                    status="realizowana"
                )
                logujneeds(need_instance, request, "confnij akceptację")
                utworz_mail_do_wyslania(
                    need_instance.osoba_prowadzaca,
                    f"Wycofano akceptację dla potrzeby {need_instance.id}",
                    get_current_url(request),
                )

            elif "rada" in request.POST and is_need_recommender:
                need_instance.status_akceptacji = Status_akceptacji.objects.get(
                    akceptacja="niegotowe"
                )
                need_instance.status_potrzeby = StatusNeed.objects.get(
                    status="rada architektury"
                )
                logujneeds(need_instance, request, "rada")
                utworz_mail_do_wyslania(
                    need_instance.osoba_prowadzaca,
                    f"Potrzeba {need_instance.id} została skierowana na radę architektury",
                    get_current_url(request),
                )
                wyslij_mail_do_grupy(
                    "need_recommender",
                    f"Potrzeba {need_instance.id} została skierowana na radę architektury",
                    get_current_url(request),
                )

            elif "analiza" in request.POST and is_need_editor:
                need_instance.status_akceptacji = Status_akceptacji.objects.get(
                    akceptacja="niegotowe"
                )
                need_instance.status_potrzeby = StatusNeed.objects.get(status="analiza")
                logujneeds(need_instance, request, "analiza")
                utworz_mail_do_wyslania(
                    need_instance.osoba_prowadzaca,
                    f"Potrzeba {need_instance.id} została skierowana do analizy",
                    get_current_url(request),
                )
                wyslij_mail_do_grupy(
                    "need_recommender",
                    f"Potrzeba {need_instance.id} została skierowana do analizy",
                    get_current_url(request),
                )

            elif "wstrzymane" in request.POST and is_need_recommender:
                need_instance.status_akceptacji = Status_akceptacji.objects.get(
                    akceptacja="niegotowe"
                )
                need_instance.status_potrzeby = StatusNeed.objects.get(
                    status="wstrzymane"
                )
                logujneeds(need_instance, request, "wstrzymane")
                utworz_mail_do_wyslania(
                    need_instance.osoba_prowadzaca,
                    f"Potrzeba {need_instance.id} została wstrzymana",
                    get_current_url(request),
                )
                wyslij_mail_do_grupy(
                    "need_recommender",
                    f"Potrzeba {need_instance.id} została wstrzymana",
                    get_current_url(request),
                )

            elif "popraw" in request.POST and (is_need_acceptor or is_need_recommender):
                need_instance.status_akceptacji = Status_akceptacji.objects.get(
                    akceptacja="do poprawy"
                )
                need_instance.status_potrzeby = StatusNeed.objects.get(
                    status="realizowana"
                )
                logujneeds(need_instance, request, "do poprawy")
                utworz_mail_do_wyslania(
                    need_instance.osoba_prowadzaca,
                    f"Popraw potrzebę {need_instance.id}",
                    get_current_url(request),
                )

            elif "Usun" in request.POST and is_need_editor:
                if need_instance.status_potrzeby.status == "nowa":
                    need_instance.delete()
                    return redirect(return_need_path(request))
                else:
                    return redirect(target_url)
            elif "Zapisz" in request.POST and is_need_editor:
                pass

            elif "Submit" in request.POST and is_need_editor:
                zapisz_needs(form, need_instance, request)
                return redirect(return_need_path(request))

            elif "do_akceptacji_infra" in request.POST and is_need_editor:
                need_instance.status_akceptacji_infrastruktury = (
                    Status_akceptacji.objects.get(akceptacja="do akceptacji")
                )
                logujneeds(need_instance, request, "Do akceptacji infrastruktury")
                utworz_mail_do_wyslania(
                    need_instance.osoba_prowadzaca,
                    f"Potrzeba {need_instance.id} została sierowana do akceptacji w zakresie infrastruktury",
                    get_current_url(request),
                )
                wyslij_mail_do_grupy(
                    "need_infra_acceptor",
                    f"Potrzeba {need_instance.id} została skierowana do akceptacji w zakresie infrastruktury",
                    get_current_url(request),
                )

            elif "akceptuj_infra" in request.POST and is_need_infra_acceptor:
                need_instance.status_akceptacji_infrastruktury = (
                    Status_akceptacji.objects.get(akceptacja="zaakceptowane")
                )
                logujneeds(need_instance, request, "zaakceptowana infrastruktura")
                utworz_mail_do_wyslania(
                    need_instance.osoba_prowadzaca,
                    f"Potrzeba {need_instance.id} została zaakceptowana w zakresie infrastruktury",
                    get_current_url(request),
                )

            elif "cofnij_infra" in request.POST and is_need_editor:
                need_instance.status_akceptacji_infrastruktury = (
                    Status_akceptacji.objects.get(akceptacja="niegotowe")
                )
                logujneeds(need_instance, request, "wycofana infrastruktura")
                utworz_mail_do_wyslania(
                    need_instance.osoba_prowadzaca,
                    f"Wycofano akceptację potrzeby {need_instance.id} w zakresie infrastruktury",
                    get_current_url(request),
                )

            elif "do_poprawy_infra" in request.POST and (
                is_need_infra_acceptor or is_superuser
            ):
                need_instance.status_akceptacji_infrastruktury = (
                    Status_akceptacji.objects.get(akceptacja="do poprawy")
                )
                logujneeds(need_instance, request, "infrastruktury do poprawy")
                utworz_mail_do_wyslania(
                    need_instance.osoba_prowadzaca,
                    f"Popraw potrzebę {need_instance.id} w zakresie infrastruktury",
                    get_current_url(request),
                )

            elif "do_akceptacji_siec" in request.POST and is_need_editor:
                need_instance.status_akceptacji_sieci = Status_akceptacji.objects.get(
                    akceptacja="do akceptacji"
                )
                logujneeds(need_instance, request, "Do akceptacji sieci")
                utworz_mail_do_wyslania(
                    need_instance.osoba_prowadzaca,
                    f"Potrzeba {need_instance.id} została sierowana do akceptacji w zakresie sieci",
                    get_current_url(request),
                )
                wyslij_mail_do_grupy(
                    "need_net_acceptor",
                    f"Potrzeba {need_instance.id} została skierowana do akceptacji w zakresie sieci",
                    get_current_url(request),
                )

            elif "akceptuj_siec" in request.POST and is_need_net_acceptor:
                need_instance.status_akceptacji_sieci = Status_akceptacji.objects.get(
                    akceptacja="zaakceptowane"
                )
                logujneeds(need_instance, request, "zaakceptowana sieć")
                utworz_mail_do_wyslania(
                    need_instance.osoba_prowadzaca,
                    f"Potrzeba {need_instance.id} została zaakceptowana w zakresie sieci",
                    get_current_url(request),
                )

            elif "cofnij_siec" in request.POST and is_need_editor:
                need_instance.status_akceptacji_sieci = Status_akceptacji.objects.get(
                    akceptacja="niegotowe"
                )
                logujneeds(need_instance, request, "wycofana sieć")
                utworz_mail_do_wyslania(
                    need_instance.osoba_prowadzaca,
                    f"Wycofano akceptację potrzeby {need_instance.id} w zakresie sieci",
                    get_current_url(request),
                )

            elif "do_poprawy_siec" in request.POST and (
                is_need_net_acceptor or is_superuser
            ):
                need_instance.status_akceptacji_sieci = Status_akceptacji.objects.get(
                    akceptacja="do poprawy"
                )
                logujneeds(need_instance, request, "sieć do poprawy")
                utworz_mail_do_wyslania(
                    need_instance.osoba_prowadzaca,
                    f"Popraw potrzebę {need_instance.id} w zakresie sieci",
                    get_current_url(request),
                )

            elif "do_akceptacji_uslugi" in request.POST and is_need_editor:
                need_instance.status_akceptacji_uslug = Status_akceptacji.objects.get(
                    akceptacja="do akceptacji"
                )
                logujneeds(need_instance, request, "Do akceptacji usługi")
                utworz_mail_do_wyslania(
                    need_instance.osoba_prowadzaca,
                    f"Potrzeba {need_instance.id} została sierowana do akceptacji w zakresie usług",
                    get_current_url(request),
                )
                wyslij_mail_do_grupy(
                    "need_service_acceptor",
                    f"Potrzeba {need_instance.id} została skierowana do akceptacji w zakresie usług",
                    get_current_url(request),
                )

            elif "akceptuj_uslugi" in request.POST and is_need_service_acceptor:
                need_instance.status_akceptacji_uslug = Status_akceptacji.objects.get(
                    akceptacja="zaakceptowane"
                )
                logujneeds(need_instance, request, "zaakceptowane usługi")
                utworz_mail_do_wyslania(
                    need_instance.osoba_prowadzaca,
                    f"Potrzeba {need_instance.id} została zaakceptowana w zakresie usług",
                    get_current_url(request),
                )

            elif "cofnij_uslugi" in request.POST and is_need_editor:
                need_instance.status_akceptacji_uslug = Status_akceptacji.objects.get(
                    akceptacja="niegotowe"
                )
                logujneeds(need_instance, request, "wycofane usługi")
                utworz_mail_do_wyslania(
                    need_instance.osoba_prowadzaca,
                    f"Wycofano akceptację potrzeby {need_instance.id} w zakresie usług",
                    get_current_url(request),
                )

            elif "do_poprawy_uslugi" in request.POST and (
                is_need_service_acceptor or is_superuser
            ):
                need_instance.status_akceptacji_uslug = Status_akceptacji.objects.get(
                    akceptacja="do poprawy"
                )
                logujneeds(need_instance, request, "usługi do poprawy")
                utworz_mail_do_wyslania(
                    need_instance.osoba_prowadzaca,
                    f"Popraw potrzebę {need_instance.id} w zakresie usług",
                    get_current_url(request),
                )

            elif "do_akceptacji_finanse" in request.POST and is_need_editor:
                need_instance.status_akceptacji_finansow = (
                    Status_akceptacji.objects.get(akceptacja="do akceptacji")
                )
                logujneeds(need_instance, request, "Do akceptacji finanse")
                utworz_mail_do_wyslania(
                    need_instance.osoba_prowadzaca,
                    f"Potrzeba {need_instance.id} została sierowana do akceptacji w zakresie finansów",
                    get_current_url(request),
                )
                wyslij_mail_do_grupy(
                    "need_finanse_acceptor",
                    f"Potrzeba {need_instance.id} została skierowana do akceptacji w zakresie finansów",
                    get_current_url(request),
                )

            elif "akceptuj_finanse" in request.POST and is_need_finanse_acceptor:
                need_instance.status_akceptacji_finansow = (
                    Status_akceptacji.objects.get(akceptacja="zaakceptowane")
                )
                logujneeds(need_instance, request, "zaakceptowane finanse")
                utworz_mail_do_wyslania(
                    need_instance.osoba_prowadzaca,
                    f"Potrzeba {need_instance.id} została zaakceptowana w zakresie finansów",
                    get_current_url(request),
                )

            elif "cofnij_finanse" in request.POST and is_need_editor:
                need_instance.status_akceptacji_finansow = (
                    Status_akceptacji.objects.get(akceptacja="niegotowe")
                )
                logujneeds(need_instance, request, "wycofane finanse")
                utworz_mail_do_wyslania(
                    need_instance.osoba_prowadzaca,
                    f"Wycofano akceptację potrzeby {need_instance.id} w zakresie finansów",
                    get_current_url(request),
                )

            elif "do_poprawy_finanse" in request.POST and (
                is_need_finanse_acceptor or is_superuser
            ):
                need_instance.status_akceptacji_finansow = (
                    Status_akceptacji.objects.get(akceptacja="do poprawy")
                )
                logujneeds(need_instance, request, "finanse do poprawy")
                utworz_mail_do_wyslania(
                    need_instance.osoba_prowadzaca,
                    f"Popraw potrzebę {need_instance.id} w zakresie finansów",
                    get_current_url(request),
                )
            else:
                logger.warning("nieoczekiwane zdarzenie w formularzu edycji potrzeby")
                return redirect(target_url)

            zapisz_needs(form, need_instance, request)
            need_instance.save()
            stamp.zapisz_czas_trwania("POST-VALID")
            return redirect(target_url)
        else:
            logger.warning(f"Błędy w formularzu edycji potrzeby {need_instance.id}")
            for field, errors in form.errors.items():
                for error in errors:
                    logger.warning(f"Błąd w polu '{field}': {error}")
            stamp.zapisz_czas_trwania("POST-form error")
        #  return redirect(target_url)
    else:
        form = DynamicneedsFormShort(
            instance=need_instance,
            display_fields=display_fields,
            is_need_allocator=is_need_allocator,
            is_need_editor=is_need_editor,
            is_need_viewer=is_need_viewer,
        )

    context.update({"form": form})
    stamp.zapisz_czas_trwania("GET")
    return render(request, "edit_need_short.html", context)
