from django import forms
from .models import Contracts, LogContract
from django.shortcuts import render, redirect
from general.models import Sections, Status_akceptacji, Stamp
from ideas.models import Ideas, StatusIdei
from django.contrib.auth.models import Group
from django.http import Http404
from django.urls import resolve, Resolver404
from urllib.parse import urlparse
from datetime import date, datetime
from general.models import Note
from django.contrib.contenttypes.models import ContentType
from general.konwertuj_wartosci_do_porownania import konwertuj_wartosci_do_porownania
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_protect
from purchases.models import Purchases
from needs.models import Needs
from general.parametry import get_param_int
from general.common_context import common_context
import logging
from general.widgets import (
    CharCountTextArea,
    create_char_count_field,
    create_float_field,
)

logger = logging.getLogger("avantic")


class DynamicContractsFormShort(forms.ModelForm):

    numer_umowy = forms.CharField(
        label="Numer umowy", widget=forms.Textarea(attrs={"rows": 1, "cols": 13})
    )
    section = forms.ModelChoiceField(
        label="Dział", queryset=Sections.objects.all(), required=False
    )
    koordynator = forms.ModelChoiceField(
        label="Właściciel pomysłu", queryset=User.objects.all(), required=False
    )

    data_zawarcia = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={"type": "date", "style": "width: 13ch;"}),
    )
    wymagana_data_zawarcia_kolejnej_umowy = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={"type": "date", "style": "width: 13ch;"}),
    )

    przedmiot_kolejnej_umowy = create_char_count_field("przedmiot_kolejnej_umowy")
    komentarz = create_char_count_field("komentarz")
    zakres = create_char_count_field("zakres")

    subject = create_char_count_field("subject", required=True)
    kontrahent = create_char_count_field("kontrahent", rows=1)

    czy_wymagana_kontynuacja = forms.NullBooleanField(
        label="Czy wymagane jest zawarcie kolejnej umowy",
        required=False,
        widget=forms.Select(choices=((None, "???"), (True, "Tak"), (False, "Nie"))),
    )
    obslugiwana = forms.NullBooleanField(
        label="Czy umowa jest obsługiwana",
        required=False,
        widget=forms.Select(choices=((None, "???"), (True, "Tak"), (False, "Nie"))),
    )

    wartosc = create_float_field(label="wartość")

    waluta = forms.CharField(
        label="Waluta",
        widget=forms.Textarea(attrs={"rows": 1, "cols": 3}),
        required=False,
    )
    osoba_prowadzaca = forms.CharField(
        widget=forms.Textarea(attrs={"rows": 1, "cols": 22}), required=False
    )

    liczba_aneksow = forms.IntegerField(
        widget=forms.NumberInput(attrs={"style": "width: 4ch;"}), required=False
    )

    ideas_to_add = forms.ModelChoiceField(
        queryset=Ideas.objects.filter(
            status_idei__status__in=["realizowana", "nowa"]
        ).order_by("subject"),
        widget=forms.Select(attrs={"style": "width: 830px;"}),
        required=False,
        label="Dodaj idee",
        empty_label="-----",
    )
    ideas_to_remove = forms.ModelChoiceField(
        queryset=Ideas.objects.none().order_by(
            "subject"
        ),  # Dynamicznie załadowane w widoku
        widget=forms.Select(attrs={"style": "width: 830px;"}),
        required=False,
        label="Usuń idee",
        empty_label="-----",
    )

    def __init__(
        self,
        *args,
        display_fields=None,
        is_contract_allocator=False,
        is_contract_viewer=False,
        is_contract_editor=False,
        **kwargs,
    ):
        super(DynamicContractsFormShort, self).__init__(*args, **kwargs)

        # wypelnienie kotrolki pomyslow, które mozna usunąć
        if self.instance:
            self.fields["ideas_to_remove"].queryset = self.instance.ideas.all()

        if display_fields:
            for field_name in self.fields.copy().keys():
                if field_name not in display_fields:
                    self.fields.pop(field_name)

        # Ustawienie wartości początkowych na "" dla pól tekstowych, jeśli są None
        for field_name, field in self.fields.items():
            if (
                isinstance(field, forms.CharField)
                and self.initial.get(field_name) is None
            ):
                self.initial[field_name] = ""

    def clean(self):
        cleaned_data = super().clean()
        for field_name, value in cleaned_data.items():
            # Sprawdzenie, czy pole jest typu CharField lub TextField
            field = self.fields[field_name]
            if isinstance(field, (forms.CharField, forms.TextInput)) and value is None:
                cleaned_data[field_name] = (
                    ""  # Zamiana None na pusty ciąg tylko dla pól tekstowych
                )
        return cleaned_data

    def format_value(self, value):
        return "" if value is None else super().format_value(value)

    def get_bound_field(self, field_name):
        field_value = self.data.get(field_name) or self.initial.get(field_name)
        # Zamień None na pusty ciąg, jeśli wartość jest None
        return "" if field_value is None else field_value

    class Meta:
        model = Contracts
        fields = "__all__"


def get_ideas_needs_and_purchases(contract_instance):

    idea_list = list(contract_instance.ideas.all())

    # Pobieranie wszystkich potrzeb powiązanych z pomysłami w jednym zapytaniu
    need_list = Needs.objects.filter(ideas__in=idea_list).distinct()

    # Pobieranie wszystkich zakupów powiązanych z potrzebami w jednym zapytaniu
    purchase_list = Purchases.objects.filter(need__in=need_list).distinct()

    # Zwrócenie trzech list
    return idea_list, need_list, purchase_list


def get_contract_context(form, contract_instance, request):
    cbu_instance = contract_instance.cbu
    ezzc_instance = contract_instance.ezzc
    idea_list, need_list, purchase_list = get_ideas_needs_and_purchases(
        contract_instance
    )
    if contract_instance.ideas.exists():
        pomysly = True
    else:
        pomysly = False

    notes = Note.objects.filter(
        content_type=ContentType.objects.get_for_model(Contracts),
        object_id=contract_instance.id,
    ).order_by("-timestamp")

    liczba_logow = get_param_int("log_entry", 20)
    recent_logs = contract_instance.log.all().order_by("-data")[:liczba_logow]
    context = {
        "form": form,
        "cbu_instance": cbu_instance,
        "ezzc_instance": ezzc_instance,
        "ideas": idea_list,
        "need_list": need_list,
        "contract_instance": contract_instance,
        "pomysly": pomysly,
        "purchase_list": purchase_list,
        "recent_logs": recent_logs,
        "notes": notes,
    }
    context.update(common_context(request))
    return context


def validate_and_return_url(request, default_url="/contracts/wszystkieumowy/"):
    full_url = request.session.get("contract_edit", default_url)
    path = urlparse(
        full_url
    ).path  # Usuwa parametry zapytania, zostawiając tylko ścieżkę

    try:
        resolve(path)  # Sprawdza, czy ścieżka jest poprawna
        return full_url  # Zwraca pełny URL, włącznie z parametrami zapytania
    except Resolver404:
        return default_url  # Zwraca URL domyślny, jeśli podany URL jest nieprawidłowy


@csrf_protect
def return_contract_path(request):
    return_page = validate_and_return_url(request)
    if "contract_edit" in request.session:
        del request.session["contract_edit"]
    return return_page


def loguj_contracts(contract_instance, request, dzialanie):
    wpis_do_logu = LogContract()
    if request.user.is_authenticated:
        wpis_do_logu.user = request.user
    wpis_do_logu.akcja = dzialanie
    wpis_do_logu.save()
    contract_instance.log.add(wpis_do_logu)


def zapisz_contracts(form, contract_instance, request):
    """
    Zapisuje formularz, a jeśli dane zostały zmienione, loguje zmiany.

    Args:
        form: Formularz do zapisania.
        contract_instance: Instancja kontraktu związana z formularzem.
        request: Obiekt żądania HTTP zawierający informacje o użytkowniku.
    """
    instance = form.save(commit=False)
    changed_fields = []

    # Sprawdzenie zmian w polach formularza
    for field in form.changed_data:
        old_value = form.initial.get(field)  # , '???')  # Domyślna wartość jako '???'
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
            loguj_contracts(contract_instance, request, change_description)
            changed_fields.append(field)

    # Jeśli są zmiany, zapisz instancję do bazy danych
    if changed_fields:
        instance.save()


@csrf_protect
def edit_contract_short(request):
    stamp = Stamp.objects.create(
        nazwa="edit_contract",
        opis="Czas wykonania funkcji edycji formularza umowy (edit_contract_short)",
        sekwencja="edit_contract_short",
        typ_zdarzenia="",
    )

    if "contract_edit" not in request.session:
        request.session["contract_edit"] = request.META.get(
            "HTTP_REFERER", "/contracts/wszystkieumowy/"
        )

    target_if_no_rights = f"/account/login"
    contract_id = request.GET.get("contract_id")
    contract_instance = Contracts.objects.get(pk=contract_id)
    target_url = f"/edit_contract_short/?contract_id={contract_instance.id}"

    context = get_contract_context("", contract_instance, request)

    is_lead_maker = context["is_lead_maker"]
    is_contract_allocator = context["is_contract_allocator"]
    is_contract_editor = context["is_contract_editor"]
    is_contract_viewer = context["is_contract_viewer"]
    is_client = context["is_client"]

    if not is_contract_viewer:
        return redirect(target_if_no_rights)

    if is_client:
        return redirect(target_if_no_rights)

    display_fields = ["ideas_to_remove", "ideas_to_add"]

    if is_contract_editor:
        display_fields.extend(
            [
                "subject",
                "zakres",
                "obslugiwana",
                "data_zawarcia",
                "kontrahent",
                "wartosc",
                "waluta",
                "liczba_aneksow",
                "czy_wymagana_kontynuacja",
                "wymagana_data_zawarcia_kolejnej_umowy",
                "przedmiot_kolejnej_umowy",
                "komentarz",
            ]
        )

    if is_contract_allocator:
        display_fields.append("section")
        display_fields.append("koordynator")
    if request.method == "POST":
        form = DynamicContractsFormShort(
            request.POST,
            instance=contract_instance,
            display_fields=display_fields,
            is_contract_allocator=is_contract_allocator,
            is_contract_editor=is_contract_editor,
            is_contract_viewer=is_contract_viewer,
        )
        current_path = request.path_info

        if "Anuluj" in request.POST:
            return redirect(return_contract_path(request))
        if form.is_valid():
            context = get_contract_context(form, contract_instance, request)

            if "notka" in request.POST:
                tresc = request.POST.get("tresc_notatki")
                user = request.user
                target_url = f"/edit_contract_short/?contract_id={contract_instance.id}"
                if len(tresc) > Note._meta.get_field("content").max_length:
                    return redirect(target_url)
                if tresc:
                    note = Note.objects.create(
                        content=tresc,
                        user=user,
                        content_type=ContentType.objects.get_for_model(Contracts),
                        object_id=contract_instance.id,
                    )
                return redirect(target_url)

            elif "DodajPomysl" in request.POST:
                if is_contract_editor:
                    # Obsługa dodawania idei
                    ideas_to_add = form.cleaned_data["ideas_to_add"]
                    if ideas_to_add:
                        contract_instance.ideas.add(ideas_to_add)
                        contract_instance.save()
                    loguj_contracts(contract_instance, request, "dodaj pomysł")
            elif "UsunPomysl" in request.POST:
                if is_contract_editor:
                    # Obsługa usuwania idei
                    ideas_to_remove = form.cleaned_data["ideas_to_remove"]
                    if ideas_to_remove:
                        contract_instance.ideas.remove(ideas_to_remove)
                        contract_instance.save()
                    loguj_contracts(contract_instance, request, "usuń pomysł")
            elif "Zapisz" in request.POST and is_contract_editor:
                pass

            elif "Submit" in request.POST and is_contract_editor:
                zapisz_contracts(form, contract_instance, request)
                return redirect(return_contract_path(request))
            elif "Idea" in request.POST and is_lead_maker:
                zapisz_contracts(form, contract_instance, request)
                nowy_pomysl = Ideas()
                nowy_pomysl.status_idei = StatusIdei.objects.get(status="nowa")
                nowy_pomysl.status_akceptacji = Status_akceptacji.objects.get(
                    akceptacja="niegotowe"
                )
                nowy_pomysl.section = contract_instance.section
                nowy_pomysl.subject = contract_instance.przedmiot_kolejnej_umowy
                nowy_pomysl.orientacynjy_budzet = contract_instance.wartosc
                nowy_pomysl.wymagana_data_realizacji = (
                    contract_instance.wymagana_data_zawarcia_kolejnej_umowy
                )
                if request.user.is_authenticated:
                    nowy_pomysl.osoba_prowadzaca = request.user
                if not nowy_pomysl.subject or len(nowy_pomysl.subject) < 3:
                    nowy_pomysl.subject = contract_instance.subject
                form.save()
                nowy_pomysl.save()
                contract_instance.ideas.add(nowy_pomysl)
                contract_instance.save()
                form.save()
                context = get_contract_context(form, contract_instance, request)
                loguj_contracts(contract_instance, request, "stwórz pomysł")
                target_url = (
                    f"/ideas/wszystkiepomysly/edit_idea_short/?idea_id={nowy_pomysl.id}"
                )
                return redirect(target_url)
            else:
                logger.warning("nieoczekiwane zdarzenie w formularzu edycji umowy")
                return redirect(target_url)
            zapisz_contracts(form, contract_instance, request)
            contract_instance.save()
            stamp.zapisz_czas_trwania("POST-VALID")
            return redirect(target_url)
        else:
            logger.warning(f"Błędy w formularzu edycji zakupu {contract_instance.id}")
            for field, errors in form.errors.items():
                for error in errors:
                    logger.warning(f"Błąd w polu '{field}': {error}")
            stamp.zapisz_czas_trwania("POST-form error")
    else:
        form = DynamicContractsFormShort(
            instance=contract_instance,
            display_fields=display_fields,
            is_contract_allocator=is_contract_allocator,
            is_contract_editor=is_contract_editor,
            is_contract_viewer=is_contract_viewer,
        )

    context.update({"form": form})
    stamp.zapisz_czas_trwania("GET")
    return render(request, "edit_contract_short.html", context)
