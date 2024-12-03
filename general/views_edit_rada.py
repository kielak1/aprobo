import logging
from datetime import datetime, timedelta, date

from django import forms
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect
from django.db import models

from dal import autocomplete

from .models import Meeting, Resolution, MeetingStatus
from ideas.models import Ideas
from needs.models import Needs
from general.common_context import common_context
from general.mail import utworz_mail_do_wyslania, wyslij_mail_do_grupy
from general.common_view import get_current_url
from general.parametry import get_param_int
from general.linki import generate_idea_url, generate_need_url

logger = logging.getLogger("avantic")


class DynamicRadaFormShort(forms.ModelForm):
    """
    Formularz dynamiczny dla modelu Meeting z polami dodawanymi dynamicznie
    oraz obsługą pól ManyToManyField z modelem pośredniczącym (Resolution).
    """

    class Meta:
        model = Meeting
        fields = []  # Pola dynamicznie dodawane w __init__

    def __init__(self, *args, **kwargs):
        """
        Konstruktor klasy formularza. Dodaje dynamicznie pola na podstawie
        przekazanych argumentów oraz ustawia wartości początkowe dla pól.
        """
        fields_to_display = kwargs.pop(
            "fields_to_display", None
        )  # Pobieramy listę pól do wyświetlenia
        super(DynamicRadaFormShort, self).__init__(*args, **kwargs)

        if fields_to_display:
            for field in fields_to_display:
                #            logger.warning(f"Adding field: {field}")
                model_field = self.Meta.model._meta.get_field(field)
                max_length = (
                    model_field.max_length
                    if hasattr(model_field, "max_length")
                    else None
                )
                # Konstrukcja warunkowa dla dynamicznego dodawania pól z różnymi konfiguracjami
                if field == "meeting_date":
                    # Dodajemy pole `meeting_date` jako DateField
                    self.fields[field] = forms.DateField(
                        required=False,
                        initial=self.instance.meeting_date,  # Ustawienie wartości początkowej
                        widget=forms.DateInput(
                            attrs={"type": "date", "style": "width: 13ch;"}
                        ),
                    )
                elif field == "general_resolution":
                    # Dodajemy pole `general_resolution` jako CharField z Textarea
                    self.fields[field] = forms.CharField(
                        required=False,
                        initial=self.instance.general_resolution,  # Ustawienie wartości początkowej
                        widget=forms.Textarea(
                            attrs={"rows": 4, "cols": 40, "style": "width: 100%;"}
                        ),
                    )
                elif field == "sort_field":
                    # Dodaj pole `sort_field` jako wybór (ChoiceField)
                    self.fields[field] = forms.ChoiceField(
                        choices=[
                            ("id", "ID"),
                            ("section", "Sekcja"),
                            ("client", "Klient"),
                        ],
                        required=False,
                        initial=self.instance.sort_field,
                        widget=forms.Select(
                            attrs={"class": "form-control", "style": "width: 14ch;"}
                        ),
                    )
                elif field == "sort_order":
                    # Dodaj pole `sort_order` jako wybór (ChoiceField)
                    self.fields[field] = forms.ChoiceField(
                        choices=[
                            ("asc", "Rosnąco"),
                            ("desc", "Malejąco"),
                        ],
                        required=False,
                        initial=self.instance.sort_order,
                        widget=forms.Select(
                            attrs={"class": "form-control", "style": "width: 14ch;"}
                        ),
                    )
                elif field == "invitations":
                    # ManyToManyField dla `invitations` - ustawiamy wartości początkowe
                    self.fields[field] = forms.ModelMultipleChoiceField(
                        queryset=User.objects.all(),
                        required=False,
                        initial=self.instance.invitations.all(),  # Pobranie wszystkich zaproszonych użytkowników
                        widget=autocomplete.ModelSelect2Multiple(
                            url="invitations-autocomplete",
                            attrs={
                                "class": "selector",
                                "data-placeholder": "Wybierz zaproszonych użytkowników",
                            },
                        ),
                    )
                elif field == "attendance_list":
                    # ManyToManyField dla `attendance_list` - ustawiamy wartości początkowe
                    self.fields[field] = forms.ModelMultipleChoiceField(
                        queryset=User.objects.all(),
                        required=False,
                        initial=self.instance.attendance_list.all(),  # Pobranie wszystkich obecnych użytkowników
                        widget=autocomplete.ModelSelect2Multiple(
                            url="attendance_list-autocomplete",
                            attrs={
                                "class": "selector",
                                "data-placeholder": "Wybierz obecnych użytkowników",
                            },
                        ),
                    )
                elif field == "discussed_ideas":
                    # Pobieranie powiązanych `Ideas` z modelu `Resolution`
                    discussed_ideas_initial = self.instance.resolutions.filter(
                        idea__isnull=False
                    ).values_list("idea", flat=True)
                    self.fields[field] = forms.ModelMultipleChoiceField(
                        queryset=Ideas.objects.all(),
                        required=False,
                        initial=discussed_ideas_initial,  # Pobieranie wszystkich powiązanych pomysłów
                        widget=autocomplete.ModelSelect2Multiple(
                            url="discussed_ideas-autocomplete",
                            attrs={
                                "class": "selector",
                                "data-placeholder": "Wybierz Pomysły",
                            },
                        ),
                    )
                elif field == "discussed_needs":
                    # Pobieranie powiązanych `Needs` z modelu `Resolution`
                    discussed_needs_initial = self.instance.resolutions.filter(
                        need__isnull=False
                    ).values_list("need", flat=True)
                    self.fields[field] = forms.ModelMultipleChoiceField(
                        queryset=Needs.objects.all(),
                        required=False,
                        initial=discussed_needs_initial,  # Pobieranie wszystkich powiązanych potrzeb
                        widget=autocomplete.ModelSelect2Multiple(
                            url="discussed_needs-autocomplete",
                            attrs={
                                "class": "selector",
                                "data-placeholder": "Wybierz Potrzeby",
                            },
                        ),
                    )
                else:
                    # Domyślne zachowanie dla innych pól
                    try:
                        self.fields[field] = self.Meta.model._meta.get_field(
                            field
                        ).formfield()
                    except Exception as e:
                        logger.error(f"Error adding field {field}: {e}")
                if max_length:
                    self.fields[field].max_length = max_length

    def zapisz(self):
        """
        Funkcja zapisująca dane z formularza do bazy. Obsługuje relacje ManyToManyField,
        w tym te z modelem pośredniczącym (Resolution).
        """
        invitations_value = self.cleaned_data.get("invitations", None)
        if invitations_value is not None:
            # logger.warning(f"Setting invitations: {invitations_value}")
            self.instance.invitations.set(invitations_value)

        # Iterujemy po polach formularza
        for field in self.fields:
            field_value = self.cleaned_data.get(field, None)
            instance_value = getattr(self.instance, field, None)

            # Obsługa ManyToManyField za pomocą metody `.set()`
            if isinstance(
                self.Meta.model._meta.get_field(field), models.ManyToManyField
            ):
                # Porównanie identyfikatorów, aby sprawdzić, czy wartości są różne
                if set(field_value) != set(instance_value.values_list("id", flat=True)):
                    # logger.warning(f"Updating field: {field}, New Value: {field_value}")
                    getattr(self.instance, field).set(field_value)

            # Obsługa standardowych pól
            else:
                if field_value != instance_value:
                    # logger.warning(f"Field: {field}, New Value: {field_value}")
                    setattr(self.instance, field, field_value)

        # Na końcu zapisujemy zmiany w bazie danych
        self.instance.save()

        # Obsługa relacji z modelem `through` (Resolution) dla pomysłów
        discussed_ideas = self.cleaned_data.get("discussed_ideas")
        existing_ideas_resolutions = self.instance.resolutions.filter(
            idea__isnull=False
        )
        existing_ideas_map = {res.idea_id: res for res in existing_ideas_resolutions}

        if discussed_ideas:
            for idea in discussed_ideas:
                if idea.id in existing_ideas_map:
                    # Pomysł już istnieje, więc pozostawiamy istniejący wpis
                    resolution = existing_ideas_map[idea.id]
                    # Możesz zaktualizować dodatkowe pola, jeśli istnieją
                else:
                    # Tworzymy nową rezolucję, jeśli pomysł jeszcze nie istnieje
                    resolution = Resolution.objects.create(
                        meeting=self.instance, idea=idea
                    )

                # Aktualizacja pól rezolucji (tu możesz dodać więcej pól, jeśli zajdzie taka potrzeba)
                # Na przykład można tutaj obsłużyć aktualizację resolution_text:
                # resolution.resolution_text = <some_value> (jeśli pole jest edytowane w formularzu)
                resolution.save()

        # Obsługa rezolucji związanych z potrzebami (Needs)
        discussed_needs = self.cleaned_data.get("discussed_needs")
        existing_needs_resolutions = self.instance.resolutions.filter(
            need__isnull=False
        )
        existing_needs_map = {res.need_id: res for res in existing_needs_resolutions}

        if discussed_needs:
            for need in discussed_needs:
                if need.id in existing_needs_map:
                    # Potrzeba już istnieje, więc pozostawiamy istniejący wpis
                    resolution = existing_needs_map[need.id]
                    # Możesz zaktualizować dodatkowe pola, jeśli istnieją
                else:
                    # Tworzymy nową rezolucję, jeśli potrzeba jeszcze nie istnieje
                    resolution = Resolution.objects.create(
                        meeting=self.instance, need=need
                    )

                # Aktualizacja pól rezolucji (jak wyżej)
                # resolution.resolution_text = <some_value>
                resolution.save()
        self.instance.save()

    def is_valid(self):
        """
        Nadpisanie metody `is_valid` w celu walidacji dynamicznych pól.
        Iteruje po wszystkich polach w `self.fields` i stosuje walidację w zależności od typu pola.
        """
        valid = super(DynamicRadaFormShort, self).is_valid()
        #         logger.warning(f"super valid={valid}")
        for field_name, field in self.fields.items():
            #          logger.warning(f"name={field_name} field={field}")
            # Pobieramy wartość pola
            value = self.cleaned_data.get(field_name)
            #           logger.warning(f"value={value} ")
            # Przykładowa walidacja dla CharField z max_length
            if isinstance(field, forms.CharField) and field.max_length:
                if value and len(value) > field.max_length:
                    self.add_error(
                        field_name,
                        f"Tekst jest zbyt długi (maksymalnie {field.max_length} znaków).",
                    )
                    valid = False

            # Możesz dodać więcej warunków dla innych typów pól
            # Przykład dla pola ModelMultipleChoiceField:
            # if isinstance(field, forms.ModelMultipleChoiceField):
            #     # Logika walidacji dla ModelMultipleChoiceField

        return valid


@csrf_protect
def edit_rada(request, meeting_id):
    """
    Widok edycji spotkania (Meeting). Obsługuje zarówno wyświetlanie formularza,
    jak i zapis zmian do bazy.

    :param request: Obiekt HttpRequest
    :param meeting_id: ID spotkania, które ma zostać edytowane
    :return: Renderowany szablon formularza edycji spotkania
    """
    # Pobranie instancji spotkania lub zwrócenie 404
    meeting = get_object_or_404(Meeting, id=meeting_id)
    context_common = common_context(request)
    is_recommender = context_common["is_recommender"]
    if is_recommender and meeting.meeting_status == MeetingStatus.objects.get(
        status="otwarte"
    ):
        is_editable = True
    else:
        is_editable = False

    # Lista pól do wyświetlenia w formularzu
    if is_editable:
        fields_to_display = [
            "general_resolution",
            "meeting_date",
            "invitations",
            "attendance_list",
            "discussed_ideas",
            "discussed_needs",
            "sort_field",
            "sort_order",
        ]
    else:
        fields_to_display = []

    if request.method == "POST":
        # Formularz z danymi POST
        form = DynamicRadaFormShort(
            request.POST, instance=meeting, fields_to_display=fields_to_display
        )
        if form.is_valid():
            if "zapisz" in request.POST and is_recommender:
                # Zapis zmian, przekierowanie do edytowanego formularza po zapisaniu
                form.zapisz()
                return redirect("edit_rada", meeting_id=meeting.id)
            if "otworz" in request.POST and is_recommender:
                # zmiana statusu na otwarte i zapis zmian, przekierowanie do edytowanego formularza po zapisaniu
                meeting.meeting_status = MeetingStatus.objects.get(status="otwarte")
                form.zapisz()
                return redirect("edit_rada", meeting_id=meeting.id)
            if "zamknij" in request.POST and is_recommender:
                # zmiana statusu na zamknięte i zapis zmian, przekierowanie do edytowanego formularza po zapisaniu
                meeting.meeting_status = MeetingStatus.objects.get(status="zamknięte")
                form.zapisz()
                return redirect("edit_rada", meeting_id=meeting.id)
            if (
                "Usun" in request.POST
                and is_recommender
                and meeting.meeting_status.status == "nowe"
            ):
                meeting.delete()
                return redirect("rady-list-all")
            if "lista" in request.POST:
                return redirect("rady-list-all")

            if "z_poprzedniego" in request.POST and is_recommender:
                previous_meeting = (
                    Meeting.objects.filter(
                        meeting_date__lt=meeting.meeting_date  # Znajdź wcześniejsze spotkania
                    )
                    .order_by("-meeting_date")
                    .first()
                )  # Pobierz najnowsze z wcześniejszych
                if previous_meeting:
                    # Skopiuj zaproszenia z poprzedniego spotkania
                    previous_invitations = previous_meeting.invitations.all()
                    # Przypisz zaproszenia do bieżącego spotkania
                    meeting.invitations.set(previous_invitations)
                    # meeting.save()
                else:
                    logger.warning("Nie znaleziono wcześniejszego spotkania")
                return redirect("edit_rada", meeting_id=meeting.id)

            if "wszyscy" in request.POST and is_recommender:
                # Pobierz zaproszenia z bieżącego spotkania
                invitations = meeting.invitations.all()
                if invitations:
                    # Przypisz zaproszenia do listy obecności
                    meeting.attendance_list.set(invitations)
                    # Zapisz bieżące spotkanie
                    # meeting.zapisz()
                return redirect("edit_rada", meeting_id=meeting.id)
            if "dodajdyskutowane" in request.POST and is_recommender:
                # Pobierz pomysły (Ideas) o statusie 'rada_architektury'
                ideas_to_add = Ideas.objects.filter(
                    status_idei__status="rada architektury"
                )
                # Dodaj te pomysły do discussed_ideas bieżącego spotkania
                for idea in ideas_to_add:
                    Resolution.objects.get_or_create(meeting=meeting, idea=idea)

                # Pobierz potrzeby (Needs) o statusie 'rada_architektury'
                needs_to_add = Needs.objects.filter(
                    status_potrzeby__status="rada architektury"
                )

                # Dodaj te potrzeby do discussed_needs bieżącego spotkania
                for need in needs_to_add:
                    Resolution.objects.get_or_create(meeting=meeting, need=need)

                return redirect("edit_rada", meeting_id=meeting.id)

            if "wyslijagende" in request.POST and is_recommender:
                subject = f"Agenda na Radę Architektury {meeting.meeting_date}"
                sender = "rada@pgnig.pl"

                discussed_ideas = meeting.resolutions.filter(
                    idea__isnull=False
                ).select_related("idea")
                discussed_needs = meeting.resolutions.filter(
                    need__isnull=False
                ).select_related("need")

                body_lines = []

                body_lines.append(
                    f"Agenda posiedzenia Rady Architektury w dniu {meeting.meeting_date}\n"
                )

                body_lines.append("Pomysły:\n")
                # Dodaj pomysły do treści maila
                for resolution in discussed_ideas:
                    idea = resolution.idea
                    adres_url = generate_idea_url(idea.id)
                    body_lines.append(
                        f"{idea.id} \t{idea.section} \t{idea.osoba_prowadzaca} \t{idea.subject} \t{adres_url}"
                    )
                body_lines.append("\nPotrzeby:\n")
                # Dodaj potrzeby do treści maila
                for resolution in discussed_needs:
                    need = resolution.need
                    adres_url = generate_need_url(need.id)
                    body_lines.append(
                        f"{need.id} \t{need.section} \t{need.osoba_prowadzaca} \t{need.subject} \t{adres_url}"
                    )

                # Połącz wszystkie linie w jedną treść maila

                body_lines.append("\n\n\t\t\t\tRada Architektury")

                adres_rady = get_current_url(request)
                body_lines.append(f"\n\n{adres_rady}")
                body = "\n".join(body_lines)
                # Uzyskaj wszystkie zaproszenia jako listę obiektów
                invitations = meeting.invitations.all()

                for invitation in invitations:
                    utworz_mail_do_wyslania(invitation, subject, body, sender)

                return redirect("edit_rada", meeting_id=meeting.id)

            for key in request.POST:
                if key.startswith("idea") and is_recommender:
                    # Wyciągnięcie pełnego klucza
                    full_key = key
                    # Zakładamy, że format klucza to 'idea_XXX' i wyciągamy 'XXX'
                    suffix = full_key.split("_")[1]

                    res_key = "edit_i_" + suffix
                    res_value = request.POST[res_key]

                    try:
                        # Odczytujemy rekord Resolution powiązany z danym pomysłem (idea) i spotkaniem (meeting)
                        resolution = Resolution.objects.get(
                            idea_id=suffix, meeting=meeting
                        )

                        # Aktualizujemy pole resolution_text wartością z formularza
                        resolution.resolution_text = res_value
                        resolution.save()
                    except Resolution.DoesNotExist:
                        logger.error(
                            f"Resolution dla idea_id {suffix} i meeting_id {meeting.id} nie istnieje."
                        )

                    return redirect("edit_rada", meeting_id=meeting.id)

            for key in request.POST:
                if key.startswith("need") and is_recommender:
                    # Wyciągnięcie pełnego klucza
                    full_key = key
                    # Zakładamy, że format klucza to 'need_XXX' i wyciągamy 'XXX'
                    suffix = full_key.split("_")[1]

                    res_key = "edit_n_" + suffix
                    res_value = request.POST[res_key]

                    try:
                        # Odczytujemy rekord Resolution powiązany z danym pomysłem (idea) i spotkaniem (meeting)
                        resolution = Resolution.objects.get(
                            need_id=suffix, meeting=meeting
                        )

                        # Aktualizujemy pole resolution_text wartością z formularza
                        resolution.resolution_text = res_value
                        resolution.save()

                    except Resolution.DoesNotExist:
                        logger.error(
                            f"Resolution dla need_id {suffix} i meeting_id {meeting.id} nie istnieje."
                        )

                    return redirect("edit_rada", meeting_id=meeting.id)

        else:
            #           logger.warnig("form edit_rada is invalid")
            logger.warning(f"Błędy w formularzu edycji rady {meeting.id}")
            for field, errors in form.errors.items():
                for error in errors:
                    logger.warning(f"Błąd w polu '{field}': {error}")

    else:
        # Formularz w trybie GET (wyświetlanie danych)
        form = DynamicRadaFormShort(
            instance=meeting, fields_to_display=fields_to_display
        )

    # Pobierz wszystkie powiązane rekordy Ideas, Needs i Resolution dla tego spotkania
    discussed_ideas = meeting.resolutions.filter(idea__isnull=False).select_related(
        "idea"
    )
    discussed_needs = meeting.resolutions.filter(need__isnull=False).select_related(
        "need"
    )

    # Stwórz identyfikatory tekstowe dla każdego pomysłu i potrzeby
    discussed_ideas_with_id = [
        {
            "idea": res.idea,
            "resolution_text": res.resolution_text,
            "id": f"idea_{res.idea.id}",
            "edit": f"edit_i_{res.idea.id}",
        }
        for res in discussed_ideas
    ]
    discussed_needs_with_id = [
        {
            "need": res.need,
            "resolution_text": res.resolution_text,
            "id": f"need_{res.need.id}",
            "edit": f"edit_n_{res.need.id}",
        }
        for res in discussed_needs
    ]

    # Pobierz sposób sortowania z obiektu `Meeting`
    sort_field = meeting.sort_field or "id"  # Domyślnie sortuj po 'id'
    sort_order = meeting.sort_order or "asc"  # Domyślnie rosnąco
    reverse = sort_order == "desc"

    # Mapowanie pola sortowania na właściwości obiektu dla Ideas
    sort_key_mapping_ideas = {
        "id": "id",
        "section": lambda x: (
            x["idea"].section.short_name if "idea" in x and x["idea"].section else ""
        ),  # Zastępujemy None pustym stringiem
        "client": lambda x: (
            x["idea"].client.short_name if "idea" in x and x["idea"].client else ""
        ),  # Zastępujemy None pustym stringiem
    }

    # Mapowanie pola sortowania na właściwości obiektu dla Needs
    sort_key_mapping_needs = {
        "id": "id",
        "section": lambda x: (
            x["need"].section.short_name if "need" in x and x["need"].section else ""
        ),  # Zastępujemy None pustym stringiem
        "client": lambda x: (
            x["need"].client.short_name if "need" in x and x["need"].client else ""
        ),  # Zastępujemy None pustym stringiem
    }


    # Pobierz klucz sortowania dla Ideas
    sort_key_ideas = sort_key_mapping_ideas.get(sort_field, "id")

    # Pobierz klucz sortowania dla Needs
    sort_key_needs = sort_key_mapping_needs.get(sort_field, "id")

    # Funkcja sortowania dla `discussed_ideas_with_id`
    if callable(sort_key_ideas):
        discussed_ideas_with_id = sorted(
            discussed_ideas_with_id, key=sort_key_ideas, reverse=reverse
        )
    else:
        discussed_ideas_with_id = sorted(
            discussed_ideas_with_id,
            key=lambda x: getattr(x["idea"], sort_key_ideas, None),
            reverse=reverse,
        )

    # Funkcja sortowania dla `discussed_needs_with_id`
    if callable(sort_key_needs):
        discussed_needs_with_id = sorted(
            discussed_needs_with_id, key=sort_key_needs, reverse=reverse
        )
    else:
        discussed_needs_with_id = sorted(
            discussed_needs_with_id,
            key=lambda x: getattr(x["need"], sort_key_needs, None),
            reverse=reverse,
        )

    # Uzupełnienie kontekstu o dane
    context = {
        "form": form,
        "instance": meeting,
        "is_editable": is_editable,
        "discussed_ideas_with_id": discussed_ideas_with_id,  # Przekazanie powiązanych pomysłów z identyfikatorami
        "discussed_needs_with_id": discussed_needs_with_id,  # Przekazanie powiązanych potrzeb z identyfikatorami
    }
    context.update(context_common)

    # Renderowanie szablonu z formularzem
    return render(request, "edit_rada.html", context)


@csrf_protect
def new_rada(request):
    meeting = Meeting()
    meeting.meeting_status = MeetingStatus.objects.get(status="nowe")

    meeting.save()
    return redirect("edit_rada", meeting_id=meeting.id)
