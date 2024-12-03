import logging
from datetime import date, datetime
from urllib.parse import urlparse

from dal import autocomplete
from django import forms
from django.contrib.auth.models import Group, User
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.shortcuts import render, redirect
from django.urls import resolve, Resolver404
from django.views.decorators.csrf import csrf_protect

from contracts.models import Contracts
from general.common_context import common_context
from general.common_view import get_current_url
from general.konwertuj_wartosci_do_porownania import konwertuj_wartosci_do_porownania
from general.mail import utworz_mail_do_wyslania, wyslij_mail_do_grupy
from general.models import (
    Acceptor,
    Clients,
    Crip,
    Dostepnosci_rozwiazania,
    Note,
    Pilnosc,
    Poziomy_dostepnosci,
    Priorytet_inicjatywy,
    Rodzaj_inicjatywy,
    Rodzaje_uslug,
    Sections,
    Sposob_wyceny,
    Sposob_zakupu,
    Stamp,
    Status_akceptacji,
    Status_procesu,
    Zgodnosc_mapy,
)
from general.parametry import get_param_int
from ideas.models import Ideas
from needs.models import Needs
from .models import Purchases, LogPurchase, Postepowania
from general.widgets import (
    CharCountTextArea,
    create_char_count_field,
    create_float_field,
)

logger = logging.getLogger("avantic")


def create_stand_field(field_name, rows=3, cols=114, required=False):
    return create_char_count_field(
        field_name=field_name,
        rows=rows,
        cols=cols,
        model=Purchases,
        required=required,
        # attrs={
        #     "style": "background-color: #ff0000;",
        # },
    )


def create_comm_field(field_name, rows=3, cols=114, required=False):
    return create_char_count_field(
        field_name=field_name,
        rows=rows,
        cols=cols,
        model=Purchases,
        required=required,
        attrs={
            "style": "background-color: #ffff99;",
        },
    )


class DynamicpurchasesFormShort(forms.ModelForm):
    przedmiot_zakupu = create_stand_field("przedmiot_zakupu", required=True)
    uzasadnienie_zakupu = create_stand_field("uzasadnienie_zakupu")
    zakres_zakupu = create_stand_field("zakres_zakupu")
    cel_i_produkty = create_stand_field("cel_i_produkty")
    komentarz = create_stand_field("komentarz")
    komentarz_akceptujacego = create_comm_field("komentarz_akceptujacego")
    link_do_ezz = forms.CharField(
        widget=forms.Textarea(attrs={"rows": 1, "cols": 40}), required=False
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
        widget=forms.Textarea(attrs={"rows": 1, "cols": 5}), required=False
    )
    pilnosc = forms.ModelChoiceField(
        label="Pilność", queryset=Pilnosc.objects.all(), required=False
    )
    budzet_capex_netto = create_float_field(label="capex")
    budzet_opex_netto = create_float_field(label="opex")
    sposob_wyceny = forms.ModelChoiceField(
        queryset=Sposob_wyceny.objects.all(), required=False
    )
    sposob_zakupu = forms.ModelChoiceField(
        queryset=Sposob_zakupu.objects.all(),
        widget=forms.Select(attrs={"style": "width: 770px;", "size": 1}),
        required=False,
    )
    id_sap = forms.CharField(
        widget=forms.Textarea(attrs={"rows": 1, "cols": 8}), required=False
    )
    dostawca = forms.CharField(
        widget=forms.Textarea(attrs={"rows": 1, "cols": 80}), required=False
    )
    wymagana_data_zawarcia_umowy = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={"type": "date", "style": "width: 15ch;"}),
    )
    atrapa = forms.CharField(
        widget=forms.Textarea(attrs={"rows": 1, "cols": 5}), required=False
    )

    def __init__(
        self,
        *args,
        display_fields=None,
        is_purchase_allocator=False,
        is_purchase_viewer=False,
        is_purchase_editor=False,
        **kwargs,
    ):
        super(DynamicpurchasesFormShort, self).__init__(*args, **kwargs)

        if display_fields:
            for field_name in self.fields.copy().keys():
                if field_name not in display_fields:
                    self.fields.pop(field_name)

    class Meta:
        model = Purchases
        fields = "__all__"

        widgets = {
            "crip_id": autocomplete.ModelSelect2Multiple(
                url="crips-autocomplete",
                attrs={
                    "class": "selector",
                    "data-placeholder": "Wybierz numer crip",
                },
            ),
        }


def get_contracts_ideas_and_needs(purchase_instance):
    need_instance = purchase_instance.need
    need_list = [need_instance]
    ideas = Ideas.objects.filter(needs=need_instance).distinct()
    contract_list = Contracts.objects.filter(ideas__in=ideas).distinct()
    return contract_list, ideas, need_list


def get_purchase_context(form, purchase_instance, request):

    is_purchase_editor = False
    if request.user.is_authenticated:
        if request.user.groups.filter(name="purchase_editor").exists():
            is_purchase_editor = True
    status_akceptacji = "niegotowe"
    status_purchase = "roboczy"
    if purchase_instance.status_procesu:
        status_purchase = purchase_instance.status_procesu.status
    if purchase_instance.status_akceptacji:
        status_akceptacji = purchase_instance.status_akceptacji.akceptacja
    if (
        status_akceptacji != "zaakceptowane"
        and status_akceptacji != "do akceptacji"
        and is_purchase_editor
    ):
        is_editable = True
    else:
        is_editable = False
    postepowanie_instances = Postepowania.objects.filter(
        numer_ZZ=purchase_instance.ezz.EZZ_number
    )
    if postepowanie_instances.exists():
        postepowanie_instance = postepowanie_instances.first()
    else:
        postepowanie_instance = None

    contract_list, ideas, need_list = get_contracts_ideas_and_needs(purchase_instance)
    cripy = []
    for x in purchase_instance.crip_id.all():
        cripy.append(x)

    acceptor = []
    for x in purchase_instance.acceptors.all():
        acceptor.append(x)

    liczba_logow = get_param_int("log_entry", 20)
    recent_logs = purchase_instance.log.all().order_by("-data")[:liczba_logow]

    notes = Note.objects.filter(
        content_type=ContentType.objects.get_for_model(Purchases),
        object_id=purchase_instance.id,
    ).order_by("-timestamp")

    is_true = True
    context = {
        "form": form,
        "is_editable": is_editable,
        "status_purchase": status_purchase,
        "status_akceptacji": status_akceptacji,
        "purchase_instance": purchase_instance,
        "postepowanie_instance": postepowanie_instance,
        "cripy": cripy,
        "need_list": need_list,
        "ideas": ideas,
        "contract_list": contract_list,
        "recent_logs": recent_logs,
        "notes": notes,
        "is_true": is_true,
    }
    context.update(common_context(request))
    return context


def logujpurchase(purchase_instance, request, dzialanie):
    wpis_do_logu = LogPurchase()
    if request.user.is_authenticated:
        wpis_do_logu.user = request.user
    wpis_do_logu.akcja = dzialanie
    wpis_do_logu.save()
    purchase_instance.log.add(wpis_do_logu)


def validate_and_return_url(request, default_url="/purchases/wszystkiezakupy/"):
    full_url = request.session.get("purchase_edit", default_url)
    path = urlparse(
        full_url
    ).path  # Usuwa parametry zapytania, zostawiając tylko ścieżkę
    try:
        resolve(path)  # Sprawdza, czy ścieżka jest poprawna
        return full_url  # Zwraca pełny URL, włącznie z parametrami zapytania
    except Resolver404:
        return default_url  # Zwraca URL domyślny, jeśli podany URL jest nieprawidłowy


@csrf_protect
def return_purchase_path(request):
    return_page = validate_and_return_url(request)
    if "purchase_edit" in request.session:
        del request.session["purchase_edit"]
    return return_page


def zapisz_purchases(form, purchase_instance, request):
    """
    Zapisuje formularz, a jeśli dane zostały zmienione, loguje zmiany.

    Args:
        form: Formularz do zapisania.
        purchase_instance: Instancja kontraktu związana z formularzem.
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
            if czy_konwersja == True:
                change_description = f"{field} zmienione na {new_value} z {old_value}"
            else:
                change_description = f"{field} zmienione na {new_value}"
            change_description = (
                (change_description[:297] + "...")
                if len(change_description) > 300
                else change_description
            )
            logujpurchase(purchase_instance, request, change_description)
            changed_fields.append(field)

    # Jeśli są zmiany, zapisz instancję do bazy danych
    if changed_fields:
        instance.save()
    if form.cleaned_data.get("crip_id"):
        instance.crip_id.set(form.cleaned_data["crip_id"])
        instance.save()
    if form.cleaned_data.get("acceptors"):
        instance.acceptors.set(form.cleaned_data["acceptors"])
        instance.save()


@csrf_protect
def edit_purchase_short(request):
    stamp = Stamp.objects.create(
        nazwa="purchase_edit",
        opis="Czas wykonania funkcji edycji formularza zakupu (edit_purchase_short)",
        sekwencja="edit_purchase_short",
        typ_zdarzenia="",
    )
    if not request.GET:  # Jeśli brak parametrów w adresie URL
        return redirect('dashboard')  # Przekierowanie na nazwę widoku 'dashboard'
    if "purchase_edit" not in request.session:
        request.session["purchase_edit"] = request.META.get(
            "HTTP_REFERER", "/purchases/wszystkiezakupy/"
        )
    purchase_id = request.GET.get("purchase_id")
    target_if_no_rights = f"/login/?next={request.path}?purchase_id={purchase_id}"
    purchase_instance = Purchases.objects.get(pk=purchase_id)
    target_url = f"/purchases/wszystkiezakupy/edit_purchase_short/?purchase_id={purchase_instance.id}"
    context = get_purchase_context("", purchase_instance, request)
    is_purchase_allocator = context["is_purchase_allocator"]
    is_purchase_editor = context["is_purchase_editor"]
    is_purchase_viewer = context["is_purchase_viewer"]
    is_purchase_acceptor = context["is_purchase_acceptor"]

    if not is_purchase_viewer:
        return redirect(target_if_no_rights)

    is_editable = context["is_editable"]

    display_fields = [
        "atrapa",
    ]

    if is_editable:
        display_fields.extend(
            [
                "pilnosc",
                "przedmiot_zakupu",
                "uzasadnienie_zakupu",
                "zakres_zakupu",
                "cel_i_produkty",
                "komentarz",
                "rozwojowy",
                "odtworzeniowy",
                "waluta",
                "budzet_capex_netto",
                "budzet_opex_netto",
                "sposob_wyceny",
                "sposob_zakupu",
                "id_sap",
                "dostawca",
                "crip_id",
                "link_do_ezz",
            ]
        )
    display_fields.extend(["wymagana_data_zawarcia_umowy"])

    if is_purchase_allocator:  # and is_editable:
        display_fields.append("section")
        display_fields.append("osoba_prowadzaca")

    if is_purchase_acceptor:
        display_fields.append("komentarz_akceptujacego")

    if request.method == "POST":
        form = DynamicpurchasesFormShort(
            request.POST,
            instance=purchase_instance,
            display_fields=display_fields,
            is_purchase_allocator=is_purchase_allocator,
            is_purchase_editor=is_purchase_editor,
            is_purchase_viewer=is_purchase_viewer,
        )
        current_path = request.path_info

        if "Anuluj" in request.POST:
            return redirect(return_purchase_path(request))

        if form.is_valid():

            context = get_purchase_context(form, purchase_instance, request)

            if "notka" in request.POST and is_purchase_editor:
                tresc = request.POST.get("tresc_notatki")
                user = request.user  # zakładam, że użytkownik jest zalogowany
                target_url = f"/purchases/wszystkiezakupy/edit_purchase_short/?purchase_id={purchase_instance.id}"
                if len(tresc) > Note._meta.get_field("content").max_length:
                    return redirect(target_url)
                if tresc:
                    note = Note.objects.create(
                        content=tresc,
                        user=user,
                        content_type=ContentType.objects.get_for_model(Purchases),
                        object_id=purchase_instance.id,
                    )
                target_url = f"/purchases/wszystkiezakupy/edit_purchase_short/?purchase_id={purchase_instance.id}"
                return redirect(target_url)

            elif "gotowe" in request.POST and is_purchase_editor:
                purchase_instance.status_akceptacji = Status_akceptacji.objects.get(
                    akceptacja="do akceptacji"
                )
                logujpurchase(purchase_instance, request, "gotowe do akceptacji")
                wyslij_mail_do_grupy(
                    "purchase_acceptor",
                    f"Podejmij decyzję dotyczącą zakupu {purchase_instance.id}",
                    get_current_url(request),
                )
                utworz_mail_do_wyslania(
                    purchase_instance.osoba_prowadzaca,
                    f"Zakup {purchase_instance.id} został skierowany do akceptacji",
                    get_current_url(request),
                )

            elif "akcept" in request.POST and is_purchase_acceptor:
                purchase_instance.status_akceptacji = Status_akceptacji.objects.get(
                    akceptacja="zaakceptowane"
                )
                logujpurchase(purchase_instance, request, "zaakceptowane")
                if "zakupydoakceptacji" in current_path:
                    target_url = f"/purchases/zakupydoakceptacji/edit_purchase_short/?purchase_id={purchase_instance.id}"
                utworz_mail_do_wyslania(
                    purchase_instance.osoba_prowadzaca,
                    f"Zakup {purchase_instance.id} został zaakceptowany",
                    get_current_url(request),
                )

            elif "popraw" in request.POST and is_purchase_acceptor:
                purchase_instance.status_akceptacji = Status_akceptacji.objects.get(
                    akceptacja="do poprawy"
                )
                logujpurchase(purchase_instance, request, "do poprawy")
                if "zakupydoakceptacji" in current_path:
                    target_url = f"/purchases/zakupydoakceptacji/edit_purchase_short/?purchase_id={purchase_instance.id}"
                utworz_mail_do_wyslania(
                    purchase_instance.osoba_prowadzaca,
                    f"Popraw zakup {purchase_instance.id}",
                    get_current_url(request),
                )

            elif "cofnij_akceptacje" in request.POST and is_purchase_acceptor:
                purchase_instance.status_akceptacji = Status_akceptacji.objects.get(
                    akceptacja="niegotowe"
                )
                logujpurchase(purchase_instance, request, "cofnij akceptację")
                utworz_mail_do_wyslania(
                    purchase_instance.osoba_prowadzaca,
                    f"Akceptacja zakupu {purchase_instance.id} została wycofana",
                    get_current_url(request),
                )

            elif "Zakupbgnig" in request.POST and is_purchase_editor:
                purchase_instance.status_procesu = Status_procesu.objects.get(
                    status="zakup BGNIG"
                )
                logujpurchase(purchase_instance, request, "zakup BGNIG")
                utworz_mail_do_wyslania(
                    purchase_instance.osoba_prowadzaca,
                    f"Zakup {purchase_instance.id} przeszedł do fazy: zakup BGNIG",
                    get_current_url(request),
                )

            elif "Zakupstandardowy" in request.POST and is_purchase_editor:
                purchase_instance.status_procesu = Status_procesu.objects.get(
                    status="w zakupach"
                )
                logujpurchase(purchase_instance, request, "w zakupach")
                utworz_mail_do_wyslania(
                    purchase_instance.osoba_prowadzaca,
                    f"Zakup {purchase_instance.id} przeszedł do fazy: zakup standardowy",
                    get_current_url(request),
                )

            elif "wrealizacji" in request.POST and is_purchase_editor:
                purchase_instance.status_procesu = Status_procesu.objects.get(
                    status="w realizacji"
                )
                logujpurchase(purchase_instance, request, "w realizacji")
                utworz_mail_do_wyslania(
                    purchase_instance.osoba_prowadzaca,
                    f"Zakup {purchase_instance.id} przeszedł do fazy: w realizacji",
                    get_current_url(request),
                )

            elif "anulowany" in request.POST and is_purchase_editor:
                purchase_instance.status_procesu = Status_procesu.objects.get(
                    status="anulowany"
                )
                logujpurchase(purchase_instance, request, "anulowany")
                utworz_mail_do_wyslania(
                    purchase_instance.osoba_prowadzaca,
                    f"Zakup {purchase_instance.id} przeszedł do fazy: anulowany",
                    get_current_url(request),
                )

            elif "roboczy" in request.POST and is_purchase_editor:
                purchase_instance.status_procesu = Status_procesu.objects.get(
                    status="roboczy"
                )
                logujpurchase(purchase_instance, request, "roboczy")
                utworz_mail_do_wyslania(
                    purchase_instance.osoba_prowadzaca,
                    f"Zakup {purchase_instance.id} przeszedł do fazy: roboczy",
                    get_current_url(request),
                )

            elif "wezz" in request.POST and is_purchase_editor:
                purchase_instance.status_procesu = Status_procesu.objects.get(
                    status="w EZZ"
                )
                logujpurchase(purchase_instance, request, "w EZZ")
                utworz_mail_do_wyslania(
                    purchase_instance.osoba_prowadzaca,
                    f"Zakup {purchase_instance.id} przeszedł do fazy: w ezz",
                    get_current_url(request),
                )

            elif "zakonczony" in request.POST and is_purchase_editor:
                purchase_instance.status_procesu = Status_procesu.objects.get(
                    status="zakończony"
                )
                logujpurchase(purchase_instance, request, "zakończony")
                utworz_mail_do_wyslania(
                    purchase_instance.osoba_prowadzaca,
                    f"Zakup {purchase_instance.id} przeszedł do fazy: zakończony",
                    get_current_url(request),
                )

            elif "Zapisz" in request.POST and is_purchase_editor:
                zapisz_purchases(form, purchase_instance, request)
                return render(request, "edit_purchase_short.html", context)

            elif "Submit" in request.POST and is_purchase_editor:
                pass
            else:
                logger.warning("nieoczekiwane zdarzenie w formularzu edycji zakupu")
                return redirect(target_url)
            zapisz_purchases(form, purchase_instance, request)
            purchase_instance.save()
            stamp.zapisz_czas_trwania("POST-VALID")
            return redirect(target_url)
        else:
            logger.warning(f"Błędy w formularzu edycji zakupu {purchase_instance.id}")
            for field, errors in form.errors.items():
                for error in errors:
                    logger.warning(f"Błąd w polu '{field}': {error}")
    else:
        form = DynamicpurchasesFormShort(
            instance=purchase_instance,
            display_fields=display_fields,
            is_purchase_allocator=is_purchase_allocator,
            is_purchase_editor=is_purchase_editor,
            is_purchase_viewer=is_purchase_viewer,
        )
    context.update({"form": form})
    stamp.zapisz_czas_trwania("GET")
    return render(request, "edit_purchase_short.html", context)
