from datetime import datetime, timedelta, date
from urllib.parse import urlparse

from django import forms
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.shortcuts import render, redirect
from django.urls import resolve, Resolver404
from django.utils.decorators import method_decorator
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
    Rodzaj_inicjatywy,
    Priorytet_inicjatywy,
    Sposob_zakupu,
    Note,
    Resolution,
    Stamp,
)
from general.parametry import get_param_int
from ideas.models import Ideas, StatusIdei, LogIdea
from needs.models import Needs, StatusNeed
from purchases.models import Purchases
from general.linki import generate_idea_url
import logging
from general.widgets import (
    CharCountTextArea,
    create_char_count_field,
    FormattedFloatWidget,
    create_float_field,
)

logger = logging.getLogger("avantic")


def create_stand_field(field_name, rows=3, cols=114, required=False):
    return create_char_count_field(
        field_name=field_name,
        rows=rows,
        cols=cols,
        model=Ideas,
        required=required,
    )


def create_comm_field(field_name, rows=3, cols=114, required=False):
    return create_char_count_field(
        field_name=field_name,
        rows=rows,
        cols=cols,
        model=Ideas,
        required=required,
        attrs={
            "style": "background-color: #ffff99;",
        },
    )


def create_resp_field(field_name, rows=3, cols=114, required=False):
    return create_char_count_field(
        field_name=field_name,
        rows=rows,
        cols=cols,
        model=Ideas,
        required=required,
        attrs={
            "style": "background-color: #0fff99;",
        },
    )


class DynamicIdeasFormShort(forms.ModelForm):

    status_idei = forms.ModelChoiceField(
        label="Status idei", queryset=StatusIdei.objects.all(), required=False
    )
    status_akceptacji = forms.ModelChoiceField(
        label="Status akceptacji",
        queryset=Status_akceptacji.objects.all(),
        required=False,
    )
    subject = create_stand_field("subject")
    data_utworzenia = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={"type": "date", "style": "width: 13ch;"}),
    )
    komentarz = create_stand_field("komentarz")
    wymagana_data_realizacji = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={"type": "date", "style": "width: 13ch;"}),
    )

    section = forms.ModelChoiceField(
        label="Dział", queryset=Sections.objects.all(), required=False
    )
    client = forms.ModelChoiceField(
        label="Klient", queryset=Clients.objects.all(), required=False
    )
    osoba_prowadzaca = forms.ModelChoiceField(
        label="Właściciel pomysłu", queryset=User.objects.all(), required=False
    )
    osoba_kontakowa_u_klienta = forms.CharField(
        label="Osoba kontaktowa w biznesie",
        widget=forms.Textarea(attrs={"rows": 1, "cols": 20}),
        required=False,
    )
    do_kiedy_zawieszona = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={"type": "date", "style": "width: 13ch;"}),
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
        widget=forms.Textarea(attrs={"rows": 1, "cols": 28}),
        required=False,
    )
    produkty = create_stand_field("produkty")
    proponowany_sposob_realizacji = forms.ModelChoiceField(
        queryset=Sposob_zakupu.objects.all(),
        widget=forms.Select(attrs={"style": "width: 1000px;", "size": 5}),
        required=False,
    )
    komentarz_akceptujacego = create_comm_field("komentarz_akceptujacego")
    atrapa = forms.CharField(required=False)
    komentarz_architekta = create_comm_field("komentarz_architekta")
    odpowiedz_koordynatora_do_architekta = create_resp_field(
        "odpowiedz_koordynatora_do_architekta"
    )
    powiazane_idee = forms.ModelMultipleChoiceField(
        queryset=Ideas.objects.filter(status_idei__status="realizowana"),
        widget=forms.SelectMultiple(attrs={"class": "custom-select"}),
        required=False,
    )
    dodaj_powiazany_pomysl = forms.ModelChoiceField(
        queryset=Ideas.objects.all(),
        required=False,
        label="Dodaj powiązaną ideę",
        help_text="Wybierz ideę do powiązania",
        widget=forms.Select(attrs={"style": "width: 830px;"}),
    )
    usun_powiazany_pomysl = forms.ModelChoiceField(
        queryset=Ideas.objects.none(),
        required=False,
        label="Usuń powiązaną ideę",
        help_text="Wybierz ideę do usunięcia z powiązań",
        widget=forms.Select(attrs={"style": "width: 830px;"}),
    )

    orientacynjy_budzet = create_float_field(label="Orientacyjny budżet")

    def __init__(
        self,
        *args,
        display_fields=None,
        is_idea_allocator=False,
        is_idea_viewer=False,
        is_idea_editor=False,
        **kwargs,
    ):
        super(DynamicIdeasFormShort, self).__init__(*args, **kwargs)
        self.idea_instance = kwargs.pop("instance", None)
        # Ustawianie queryset dla usun_powiazany_pomysl, jeśli mamy instancję
        if self.idea_instance:
            self.fields["usun_powiazany_pomysl"].queryset = (
                self.idea_instance.powiazane_idee.all()
            )

        if display_fields:
            for field_name in self.fields.copy().keys():
                if field_name not in display_fields:
                    self.fields.pop(field_name)

    class Meta:
        model = Ideas
        fields = "__all__"


def validate_and_return_url(request, default_url="/ideas/wszystkiepomysly/"):
    full_url = request.session.get("idea_edit", default_url)
    path = urlparse(
        full_url
    ).path  # Usuwa parametry zapytania, zostawiając tylko ścieżkę

    try:
        resolve(path)  # Sprawdza, czy ścieżka jest poprawna
        return full_url  # Zwraca pełny URL, włącznie z parametrami zapytania
    except Resolver404:
        return default_url  # Zwraca URL domyślny, jeśli podany URL jest nieprawidłowy


@csrf_protect
def return_idea_path(request):
    return_page = validate_and_return_url(request)
    if "idea_edit" in request.session:
        del request.session["idea_edit"]
    return return_page


def get_contracts_needs_and_purchases(idea_instance, request):
    idea_id = request.GET.get("idea_id")

    purchase_list = []
    need_list = []

    if idea_id is not None:
        need_list = list(idea_instance.needs.all())
        purchase_list = Purchases.objects.filter(need__in=need_list)

    contract_list = Contracts.objects.filter(ideas=idea_instance)

    return contract_list, need_list, purchase_list


def get_idea_context(form, idea_instance, request):
    contract_list, need_list, purchase_list = get_contracts_needs_and_purchases(
        idea_instance, request
    )
    powiazane_pomysly = []
    for x in idea_instance.powiazane_idee.all():
        powiazane_pomysly.append(x)

    liczba_logow = get_param_int("log_entry", 20)
    recent_logs = idea_instance.log.all().order_by("-data")[:liczba_logow]

    status_akceptacji = "niegotowe"
    status_idei = "nowe"
    if idea_instance.status_idei:
        status_idei = idea_instance.status_idei.status
    if idea_instance.status_akceptacji:
        status_akceptacji = idea_instance.status_akceptacji.akceptacja

    #   is_client = request.user.groups.filter(name="client").exists()
    is_idea_editor = request.user.groups.filter(name="idea_editor").exists()
    is_lead_maker = request.user.groups.filter(name="lead_maker").exists()

    is_edition_blocked = True
    if (
        status_akceptacji != "do akceptacji"
        and status_akceptacji != "zaakceptowane"
        and status_idei != "zrealizowana"
        and status_idei != "zamknięta"
        and (is_idea_editor or is_lead_maker)
    ):
        is_edition_blocked = False
    priorytet = idea_instance.priorytet

    data_utworzenia = idea_instance.data_utworzenia
    osoba_prowadzaca = idea_instance.osoba_prowadzaca

    notes = Note.objects.filter(
        content_type=ContentType.objects.get_for_model(Ideas),
        object_id=idea_instance.id,
    ).order_by("-timestamp")

    context = {
        "form": form,
        "contract_list": contract_list,
        "need_list": need_list,
        "status_idei": status_idei,
        "status_akceptacji": status_akceptacji,
        "data_utworzenia": data_utworzenia,
        "osoba_prowadzaca": osoba_prowadzaca,
        "priorytet": priorytet,
        "is_edition_blocked": is_edition_blocked,
        "idea_instance": idea_instance,
        "recent_logs": recent_logs,
        "powiazane_pomysly": powiazane_pomysly,
        "purchase_list": purchase_list,
        "notes": notes,
    }
    context.update(common_context(request))
    return context


def logujideas(idea_instance, request, dzialanie):
    wpis_do_logu = LogIdea()
    if request.user.is_authenticated:
        wpis_do_logu.user = request.user
    wpis_do_logu.akcja = dzialanie
    wpis_do_logu.save()
    idea_instance.log.add(wpis_do_logu)


def zapisz_ideas(form, idea_instance, request):
    """
    Zapisuje formularz, a jeśli dane zostały zmienione, loguje zmiany.

    Args:
        form: Formularz do zapisania.
        idea_instance: Instancja kontraktu związana z formularzem.
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
            logujideas(idea_instance, request, change_description)
            changed_fields.append(field)
            if field == "osoba_prowadzaca":
                utworz_mail_do_wyslania(
                    idea_instance.osoba_prowadzaca,
                    f"Zostałeś przydzielony do pomysłu {idea_instance.id} jako koordynator",
                    get_current_url(request),
                )
    # Jeśli są zmiany, zapisz instancję do bazy danych
    if changed_fields:
        instance.save()

    if form.cleaned_data.get("powiazane_idee"):
        instance.powiazane_idee.set(form.cleaned_data["powiazane_idee"])
        instance.save()


@csrf_protect
def edit_idea_short(request):
    stamp = Stamp.objects.create(
        nazwa="idea_edit",
        opis="Czas wykonania funkcji edycji formularza pomysłu (edit_idea_short)",
        sekwencja="edit_idea_short",
        typ_zdarzenia="",
    )
    if not request.GET:  # Jeśli brak parametrów w adresie URL
        return redirect('dashboard')  # Przekierowanie na nazwę widoku 'dashboard'
 
    if "idea_edit" not in request.session:
        request.session["idea_edit"] = request.META.get(
            "HTTP_REFERER", "/ideas/wszystkiepomysly/"
        )

    idea_id = request.GET.get("idea_id")
    target_if_no_rights = f"/login/?next={request.path}?idea_id={idea_id}"
    if idea_id is None:
        idea_instance = Ideas()
        idea_instance.status_idei = StatusIdei.objects.get(status="nowa")
        idea_instance.status_akceptacji = Status_akceptacji.objects.get(
            akceptacja="niegotowe"
        )
        if request.user.is_authenticated:
            is_client = False
            if request.user.groups.filter(name="client").exists():
                is_client = True
            idea_instance.inicjator = request.user

            if is_client == False:
                idea_instance.osoba_prowadzaca = request.user

                user = request.user
                user_sections = user.custom_models.all()
                if user_sections:
                    idea_instance.section = user_sections.first()
                else:
                    idea_instance.section = Sections.objects.get(short_name="SIN")
            else:
                klienci = Clients.objects.filter(users=request.user)
                if not klienci.exists():
                    logger.warning(
                        f"Brak przypisanych klientów dla użytkownika {request.user}"
                    )
                    return redirect("dashboard")
                idea_instance.osoba_prowadzaca = klienci.first().opiekun
                idea_instance.section = Sections.objects.filter(
                    users=idea_instance.osoba_prowadzaca
                ).first()
                idea_instance.client = klienci.first()
                idea_instance.osoba_kontakowa_u_klienta = f"{idea_instance.inicjator.first_name} {idea_instance.inicjator.last_name}"
        idea_instance.save()

        utworz_mail_do_wyslania(
            idea_instance.osoba_prowadzaca,
            f"Zostałeś przydzielony do pomysłu {idea_instance.id} jako koordynator",
            generate_idea_url(idea_instance.id),
        )
        target_url = f"/ideas/wszystkiepomysly/edit_idea_short/?idea_id={idea_instance.id}&pierwszy=1"
        return redirect(target_url)
    else:
        idea_instance = Ideas.objects.get(pk=idea_id)
    #     logger.warning(f"idea_instance={idea_instance}")
    # if not idea_instance:
    #     return redirect('dashboard')  # Przekierowanie na nazwę widoku 'dashboard'
    target_url = f"/ideas/wszystkiepomysly/edit_idea_short/?idea_id={idea_instance.id}"

    context = get_idea_context("", idea_instance, request)

    is_idea_allocator = context["is_idea_allocator"]
    is_idea_editor = context["is_idea_editor"]
    is_idea_viewer = context["is_idea_viewer"]
    is_need_maker = context["is_need_maker"]
    is_idea_acceptor = context["is_idea_acceptor"]
    is_idea_recommender = context["is_idea_recommender"]
    is_client = context["is_client"]
    is_recommender = context["is_recommender"]
    is_lead_maker = context["is_lead_maker"]

    if not is_idea_viewer and not is_client:
        return redirect(target_if_no_rights)

    if is_client:
        klienci = Clients.objects.filter(users=request.user)
        if not idea_instance.client in klienci:
            return redirect(target_if_no_rights)

    status_akceptacji = "niegotowe"
    status_idei = "nowe"
    if idea_instance.status_idei:
        status_idei = idea_instance.status_idei.status
    if idea_instance.status_akceptacji:
        status_akceptacji = idea_instance.status_akceptacji.akceptacja

    is_edition_blocked = context["is_edition_blocked"]

    if not is_edition_blocked:
        if is_client:
            display_fields = [
                "subject",
                "komentarz",
                "wymagana_data_realizacji",
                "orientacynjy_budzet",
                "osoba_kontakowa_u_klienta",
                "opis",
                "uzasadnienie",
                "produkty",
                "wlasciciel_biznesowy",
                "priorytet",
            ]
        else:
            display_fields = [
                "subject",
                "komentarz",
                "wymagana_data_realizacji",
                "orientacynjy_budzet",
                "osoba_kontakowa_u_klienta",
                "opis",
                "uzasadnienie",
                "produkty",
                "wlasciciel_biznesowy",
                "dodaj_powiazany_pomysl",
                "usun_powiazany_pomysl",
                "priorytet",
                "client",
                "rodzaj_inicjatywy",
                "proponowany_sposob_realizacji",
            ]
        if is_idea_allocator:
            display_fields.append("section")
            display_fields.append("osoba_prowadzaca")
    else:
        display_fields = ["atrapa"]

    if status_akceptacji == "do akceptacji":
        display_fields.append("komentarz_akceptujacego")

    if status_idei == "realizowana" and status_akceptacji == "do poprawy":
        display_fields.append("odpowiedz_koordynatora_do_architekta")

    if status_idei == "analiza" or status_idei == "rada architektury":
        display_fields.append("komentarz_architekta")
    if status_idei == "zawieszona":
        display_fields.append("do_kiedy_zawieszona")

    if request.method == "POST":
        form = DynamicIdeasFormShort(
            request.POST,
            instance=idea_instance,
            display_fields=display_fields,
            is_idea_allocator=is_idea_allocator,
            is_idea_editor=is_idea_editor,
            is_idea_viewer=is_idea_viewer,
        )

        if "Anuluj" in request.POST:
            return redirect(return_idea_path(request))

        if "Usun" in request.POST and (is_idea_editor or is_lead_maker):
            if (
                not idea_instance.status_idei
                or idea_instance.status_idei.status == "nowa"
            ):
                idea_instance.delete()
                return redirect(return_idea_path(request))
            else:
                return render(request, "edit_idea_short.html", context)

        if form.is_valid():

            if "update_resolution" in request.POST and is_recommender:
                res_value = request.POST["resolution_text"]
                # Pobieramy najnowsze postanowienie (Resolution) związane z Ideas, z najnowszym posiedzeniem (Meeting)
                latest_resolution = (
                    Resolution.objects.filter(idea=idea_instance)
                    .order_by("-meeting__meeting_date")
                    .first()
                )

                if latest_resolution:
                    # Aktualizacja pola resolution_text dla wybranego postanowienia
                    latest_resolution.resolution_text = res_value
                    latest_resolution.save()
                return redirect(target_url)

            elif "notka" in request.POST and (is_idea_editor or is_client):
                tresc = request.POST.get("tresc_notatki")
                user = request.user  # zakładam, że użytkownik jest zalogowany
                if len(tresc) > Note._meta.get_field("content").max_length:
                    return redirect(target_url)
                if tresc:
                    note = Note.objects.create(
                        content=tresc,
                        user=user,
                        content_type=ContentType.objects.get_for_model(Ideas),
                        object_id=idea_instance.id,
                    )
                return redirect(target_url)

            elif "unlink_related_idea" in request.POST and is_idea_editor:
                odlaczana_idea = form.cleaned_data.get("usun_powiazany_pomysl")
                if odlaczana_idea:
                    idea_instance.powiazane_idee.remove(odlaczana_idea)
                utworz_mail_do_wyslania(
                    idea_instance.osoba_prowadzaca,
                    f"Od pomysłu {idea_instance.id} został odwiązany pomysłem {podlaczana_idea.id}",
                    get_current_url(request),
                )

            elif "link_related_idea" in request.POST and is_idea_editor:
                podlaczana_idea = form.cleaned_data.get("dodaj_powiazany_pomysl")
                if podlaczana_idea:
                    idea_instance.powiazane_idee.add(podlaczana_idea)
                    idea_instance.save()
                utworz_mail_do_wyslania(
                    idea_instance.osoba_prowadzaca,
                    f"Pomysł {idea_instance.id} został powiązany z pomysłem {podlaczana_idea.id}",
                    get_current_url(request),
                )

            elif "realizuj" in request.POST and is_idea_editor:
                idea_instance.status_idei = StatusIdei.objects.get(status="realizowana")
                logujideas(idea_instance, request, "Realizuj")
                utworz_mail_do_wyslania(
                    idea_instance.osoba_prowadzaca,
                    f"Pomysł {idea_instance.id} przeszedł do fazy realizacji",
                    get_current_url(request),
                )

            elif "zawies" in request.POST and is_idea_editor:
                idea_instance.do_kiedy_zawieszona = datetime.now().date() + timedelta(
                    days=45
                )
                idea_instance.status_idei = StatusIdei.objects.get(status="zawieszona")
                logujideas(idea_instance, request, "Zawieś")
                utworz_mail_do_wyslania(
                    idea_instance.osoba_prowadzaca,
                    f"Pomysł {idea_instance.id} został zawieszony",
                    get_current_url(request),
                )

            elif "klonuj" in request.POST and is_idea_editor:
                sklonowana_idea = idea_instance.clone_idea()
                logujideas(
                    idea_instance, request, f"klon do pomysłu {sklonowana_idea.id}"
                )
                logujideas(sklonowana_idea, request, f"klon pomysłu {idea_instance.id}")
                zapisz_ideas(form, idea_instance, request)
                idea_instance.save()
                sklonowana_idea.inicjator = request.user
                sklonowana_idea.osoba_prowadzaca = request.user
                user = request.user
                user_sections = user.custom_models.all()
                if user_sections:
                    sklonowana_idea.section = user_sections.first()
                else:
                    sklonowana_idea.section = Sections.objects.get(short_name="SIN")
                sklonowana_idea.save()
                target_url = f"/ideas/wszystkiepomysly/edit_idea_short/?idea_id={sklonowana_idea.id}"
                utworz_mail_do_wyslania(
                    idea_instance.osoba_prowadzaca,
                    f"Pomysł {idea_instance.id} został sklonowany",
                    get_current_url(request),
                )
                return redirect(target_url)

            elif "odwies" in request.POST and is_idea_editor:
                idea_instance.status_idei = StatusIdei.objects.get(status="nowa")
                logujideas(idea_instance, request, "Odwieś")
                utworz_mail_do_wyslania(
                    idea_instance.osoba_prowadzaca,
                    f"Pomysł {idea_instance.id} został odwieszony",
                    get_current_url(request),
                )

            elif "popraw" in request.POST and (is_idea_acceptor or is_idea_recommender):
                idea_instance.status_akceptacji = Status_akceptacji.objects.get(
                    akceptacja="do poprawy"
                )
                idea_instance.status_idei = StatusIdei.objects.get(status="realizowana")
                logujideas(idea_instance, request, "Popraw")
                utworz_mail_do_wyslania(
                    idea_instance.osoba_prowadzaca,
                    f"Popraw pomysł {idea_instance.id}",
                    get_current_url(request),
                )

            elif "gotowe" in request.POST and is_idea_recommender:
                idea_instance.status_akceptacji = Status_akceptacji.objects.get(
                    akceptacja="do akceptacji"
                )
                idea_instance.status_idei = StatusIdei.objects.get(status="realizowana")
                logujideas(idea_instance, request, "Gotowe")
                wyslij_mail_do_grupy(
                    "idea_acceptor",
                    f"Podejmij decyzję dotyczącą pomysłu {idea_instance.id}",
                    get_current_url(request),
                )
                utworz_mail_do_wyslania(
                    idea_instance.osoba_prowadzaca,
                    f"Pomysł {idea_instance.id} został skierowany do akceptacji",
                    get_current_url(request),
                )

            elif "rada" in request.POST and is_idea_recommender:  # recommender?
                idea_instance.status_idei = StatusIdei.objects.get(
                    status="rada architektury"
                )
                logujideas(idea_instance, request, "Rada")
                wyslij_mail_do_grupy(
                    "idea_recommender",
                    f"Pomysł {idea_instance.id} został skierowany na Radę Architektury",
                    get_current_url(request),
                )
                utworz_mail_do_wyslania(
                    idea_instance.osoba_prowadzaca,
                    f"Pomysł {idea_instance.id} został skierowany na Radę Architektury",
                    get_current_url(request),
                )

            elif "analiza" in request.POST and is_idea_editor:
                idea_instance.status_idei = StatusIdei.objects.get(status="analiza")
                logujideas(idea_instance, request, "analiza")
                wyslij_mail_do_grupy(
                    "idea_recommender",
                    f"Pomysł {idea_instance.id} został skierowany do analizy",
                    get_current_url(request),
                )
                utworz_mail_do_wyslania(
                    idea_instance.osoba_prowadzaca,
                    f"Pomysł {idea_instance.id} został skierowany do analizy",
                    get_current_url(request),
                )

            elif "wstrzymane" in request.POST and is_idea_recommender:
                idea_instance.status_idei = StatusIdei.objects.get(status="wstrzymane")
                logujideas(idea_instance, request, "wstrzymane")
                wyslij_mail_do_grupy(
                    "idea_recommender",
                    f"Pomysł {idea_instance.id} został wstrzymany",
                    get_current_url(request),
                )
                utworz_mail_do_wyslania(
                    idea_instance.osoba_prowadzaca,
                    f"Pomysł {idea_instance.id} został wstrzymany",
                    get_current_url(request),
                )

            elif "akcept" in request.POST and is_idea_acceptor:
                idea_instance.status_idei = StatusIdei.objects.get(status="realizowana")
                idea_instance.status_akceptacji = Status_akceptacji.objects.get(
                    akceptacja="zaakceptowane"
                )
                logujideas(idea_instance, request, "Akcept")
                utworz_mail_do_wyslania(
                    idea_instance.osoba_prowadzaca,
                    f"Pomysł {idea_instance.id} uzyskał akceptację",
                    get_current_url(request),
                )

            elif "arch_yes" in request.POST and is_idea_recommender:
                idea_instance.czy_dotyczy_architektury = True
                logujideas(idea_instance, request, "Dotyczy architektury")
                utworz_mail_do_wyslania(
                    idea_instance.osoba_prowadzaca,
                    f"Pomysł {idea_instance.id} dotyczy architektury",
                    get_current_url(request),
                )

            elif "arch_no" in request.POST and is_idea_recommender:
                idea_instance.czy_dotyczy_architektury = False
                logujideas(idea_instance, request, "Nie dotyczy architektury")
                utworz_mail_do_wyslania(
                    idea_instance.osoba_prowadzaca,
                    f"Pomysł {idea_instance.id} nie dotyczy architektury",
                    get_current_url(request),
                )

            elif "Reset" in request.POST and is_idea_editor:
                idea_instance.status_idei = StatusIdei.objects.get(status="realizowana")
                idea_instance.status_akceptacji = Status_akceptacji.objects.get(
                    akceptacja="niegotowe"
                )
                logujideas(idea_instance, request, "Reset")
                utworz_mail_do_wyslania(
                    idea_instance.osoba_prowadzaca,
                    f"Pomysł {idea_instance.id} został zresetowany",
                    get_current_url(request),
                )

            elif "cofnij" in request.POST and is_idea_editor:
                idea_instance.status_idei = StatusIdei.objects.get(status="realizowana")
                idea_instance.status_akceptacji = Status_akceptacji.objects.get(
                    akceptacja="niegotowe"
                )
                logujideas(idea_instance, request, "cofnij Akcept")
                utworz_mail_do_wyslania(
                    idea_instance.osoba_prowadzaca,
                    f"Akceptacja pomysłu {idea_instance.id} została wycofana",
                    get_current_url(request),
                )

            elif "przywroc" in request.POST and is_idea_editor:
                idea_instance.status_idei = StatusIdei.objects.get(status="realizowana")
                idea_instance.status_akceptacji = Status_akceptacji.objects.get(
                    akceptacja="niegotowe"
                )
                logujideas(idea_instance, request, "Przywróć")
                utworz_mail_do_wyslania(
                    idea_instance.osoba_prowadzaca,
                    f"Pomysł {idea_instance.id} został przywrócony",
                    get_current_url(request),
                )

            elif "zamknij" in request.POST and is_idea_editor:
                idea_instance.status_idei = StatusIdei.objects.get(status="zamknięta")
                logujideas(idea_instance, request, "Zamknij")
                utworz_mail_do_wyslania(
                    idea_instance.osoba_prowadzaca,
                    f"Pomysł {idea_instance.id} został porzucony",
                    get_current_url(request),
                )

            elif "zakoncz" in request.POST and is_idea_editor:
                idea_instance.status_idei = StatusIdei.objects.get(
                    status="zrealizowana"
                )
                logujideas(idea_instance, request, "Zakończ")
                utworz_mail_do_wyslania(
                    idea_instance.osoba_prowadzaca,
                    f"Pomysł {idea_instance.id} został zrealizowany",
                    get_current_url(request),
                )

            elif "Zapisz" in request.POST and (is_idea_editor or is_client):
                pass

            elif "Submit" in request.POST and is_idea_editor:
                zapisz_ideas(form, idea_instance, request)
                return redirect(return_idea_path(request))

            elif "Need" in request.POST and is_idea_editor and is_need_maker:
                zapisz_ideas(form, idea_instance, request)
                nowa_potrzeba = Needs()
                nowa_potrzeba.status_potrzeby = StatusNeed.objects.get(status="nowa")
                nowa_potrzeba.status_akceptacji = Status_akceptacji.objects.get(
                    akceptacja="niegotowe"
                )
                nowa_potrzeba.subject = idea_instance.subject
                nowa_potrzeba.komentarz = idea_instance.komentarz
                nowa_potrzeba.wymagana_data_realizacji = (
                    idea_instance.wymagana_data_realizacji
                )
                nowa_potrzeba.orientacynjy_budzet = idea_instance.orientacynjy_budzet
                nowa_potrzeba.section = idea_instance.section
                nowa_potrzeba.client = idea_instance.client
                nowa_potrzeba.osoba_kontakowa_u_klienta = (
                    idea_instance.osoba_kontakowa_u_klienta
                )
                nowa_potrzeba.czy_dotyczy_architektury = (
                    idea_instance.czy_dotyczy_architektury
                )
                if request.user.is_authenticated:
                    nowa_potrzeba.osoba_prowadzaca = request.user

                nowa_potrzeba.rodzaj_inicjatywy = idea_instance.rodzaj_inicjatywy
                nowa_potrzeba.opis = idea_instance.opis
                nowa_potrzeba.uzasadnienie = idea_instance.uzasadnienie
                nowa_potrzeba.priorytet = idea_instance.priorytet
                nowa_potrzeba.wlasciciel_biznesowy = idea_instance.wlasciciel_biznesowy
                nowa_potrzeba.proponowany_sposob_realizacji = (
                    idea_instance.proponowany_sposob_realizacji
                )
                nowa_potrzeba.produkty = idea_instance.produkty

                form.save()
                nowa_potrzeba.save()
                idea_instance.needs.add(nowa_potrzeba)
                logujideas(idea_instance, request, "Need")
                idea_instance.save()
                form.save()

                target_url = f"/needs/edit_need_short/?need_id={nowa_potrzeba.id}"
                utworz_mail_do_wyslania(
                    idea_instance.osoba_prowadzaca,
                    f"Dla pomysłu {idea_instance.id} została utworzona potrzeba {nowa_potrzeba.id}",
                    get_current_url(request),
                )

                return redirect(target_url)

            else:
                logger.warning("nieoczekiwane zdarzenie w formularzu edycji pomysłu")
                return redirect(target_url)
            zapisz_ideas(form, idea_instance, request)
            idea_instance.save()
            stamp.zapisz_czas_trwania("POST-VALID")
            return redirect(target_url)
        else:
            logger.warning(f"Błędy w formularzu edycji pomysłu {idea_instance.id}")
            for field, errors in form.errors.items():
                for error in errors:
                    logger.warning(f"Błąd w polu '{field}': {error}")
            stamp.zapisz_czas_trwania("POST-form error")
    else:
        form = DynamicIdeasFormShort(
            instance=idea_instance,
            display_fields=display_fields,
            is_idea_allocator=is_idea_allocator,
            is_idea_editor=is_idea_editor,
            is_idea_viewer=is_idea_viewer,
        )

    context.update({"form": form})
    stamp.zapisz_czas_trwania("GET")
    return render(request, "edit_idea_short.html", context)
