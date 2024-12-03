from django import template
from general.models import Resolution
from general.parametry import get_param_int
from purchases.forms import ImportForm
import logging

logger = logging.getLogger("avantic")
register = template.Library()


@register.inclusion_tag("filtr_field.html", takes_context=True)
def filtr_field(context, field_name, name):
    """
    Generuje kontekst do renderowania pola filtra w szablonie.

    :param context: Aktualny kontekst przekazany do szablonu.
    :type context: dict
    :param field_name: Nazwa pola filtra.
    :type field_name: str
    :param name: Wyświetlana nazwa dla pola filtra.
    :type name: str
    :return: Zaktualizowany kontekst do użycia w szablonie.
    :rtype: dict
    """
    request = context["request"]
    filter_instance = context.get("filter")
    choices = None

    if filter_instance:
        filter_field = filter_instance.form.fields.get(field_name)
        if filter_field and hasattr(filter_field, "choices"):
            choices = filter_field.choices

    context.update(
        {
            "field_name": field_name,
            "name": name,
            "choices": choices,
            "parameters": request.GET,
        }
    )
    return context


@register.inclusion_tag("drop_down.html", takes_context=True)
def drop_down(context, sciezka, etykieta):
    """
    Generuje kontekst do renderowania rozwijanego menu w szablonie.

    :param context: Aktualny kontekst przekazany do szablonu.
    :type context: dict
    :param sciezka: Ścieżka URL, do której będą kierować elementy menu.
    :type sciezka: str
    :param etykieta: Etykieta dla rozwijanego menu.
    :type etykieta: str
    :return: Zaktualizowany kontekst do użycia w szablonie.
    :rtype: dict
    """
    if "?" in sciezka:
        sciezka += "&"
    else:
        sciezka += "?"
    context.update(
        {
            "sciezka": sciezka,
            "etykieta": etykieta,
        }
    )
    return context


@register.inclusion_tag("drop_down_klient.html", takes_context=True)
def drop_down_klient(context, sciezka, etykieta):
    """
    Generuje kontekst do renderowania rozwijanego menu dla klientów w szablonie.

    :param context: Aktualny kontekst przekazany do szablonu.
    :type context: dict
    :param sciezka: Ścieżka URL, do której będą kierować elementy menu.
    :type sciezka: str
    :param etykieta: Etykieta dla rozwijanego menu.
    :type etykieta: str
    :return: Zaktualizowany kontekst do użycia w szablonie.
    :rtype: dict
    """
    if "?" in sciezka:
        sciezka += "&"
    else:
        sciezka += "?"
    context.update(
        {
            "sciezka": sciezka,
            "etykieta": etykieta,
        }
    )
    return context


@register.inclusion_tag("resolutions.html", takes_context=True)
def resolutions(context):
    """
    Generuje kontekst do wyświetlenia listy uchwał dla danego obiektu Idea lub Need.

    :param context: Aktualny kontekst przekazany do szablonu.
    :type context: dict
    :return: Kontekst z listą uchwał i dodatkowymi informacjami.
    :rtype: dict
    """
    request = context["request"]
    idea_instance = context.get("idea_instance", None)
    need_instance = context.get("need_instance", None)

    # Sprawdzanie zmiennej obsluga_rady_architektury
    obsluga_rady_architektury = get_param_int("obsluga_rady_architektury", 0)
    if obsluga_rady_architektury != 1:
        return {}  # Nic nie wyświetlaj

    # Sprawdzenie, czy użytkownik jest rekomendatorem
    is_recommender = False
    if request.user.is_authenticated:
        if (
            request.user.groups.filter(name="idea_recommender").exists()
            or request.user.groups.filter(name="need_recommender").exists()
        ):
            is_recommender = True

    # Domyślnie pusty queryset
    resolutions_queryset = Resolution.objects.none()

    if idea_instance:
        resolutions_queryset = Resolution.objects.filter(idea=idea_instance).order_by(
            "-meeting__meeting_date"
        )
    elif need_instance:
        resolutions_queryset = Resolution.objects.filter(need=need_instance).order_by(
            "-meeting__meeting_date"
        )

    resolutions_list = list(resolutions_queryset)
    editable_resolution = None

    if resolutions_list:
        latest_resolution = resolutions_list[0]
        if (
            latest_resolution.meeting.meeting_status.status == "otwarte"
            and is_recommender
        ):
            editable_resolution = latest_resolution
    is_client = context["is_client"]
    return {
        "resolutions": resolutions_list,
        "editable_resolution": editable_resolution,
        "idea_instance": idea_instance,
        "need_instance": need_instance,
        "is_recommender": is_recommender,
        "is_client": is_client,
    }


@register.inclusion_tag("excell_import.html")
def excell_import(header_text, button_text):
    """
    Generuje kontekst dla formularza importu danych z plików Excel.

    :param header_text: Nagłówek wyświetlany nad formularzem.
    :type header_text: str
    :param button_text: Tekst na przycisku wysyłania formularza.
    :type button_text: str
    :return: Kontekst z formularzem importu i dodatkowymi informacjami.
    :rtype: dict
    """
    form = ImportForm()
    return {"form": form, "header_text": header_text, "button_text": button_text}
