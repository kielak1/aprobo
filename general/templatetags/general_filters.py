from django import template
from datetime import date
import re
from django.utils.safestring import mark_safe
import logging
from django.template.defaultfilters import floatformat
from django.contrib.humanize.templatetags.humanize import intcomma
from purchases.models import Purchases, Postepowania
from django.utils.safestring import mark_safe

logger = logging.getLogger("avantic")
register = template.Library()


@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)


@register.filter
def days_until(date):
    if date:
        delta = date - date.today()
        return delta.days
    return ""


@register.filter
def get_class_for_column(column_name):
    if column_name == "subject":
        return "fixed-width-subject"
    if column_name == "id":
        return "fixed-width-id"
    if column_name == "komentarz":
        return "fixed-width-komentarz"
    return ""


@register.filter(name="make_links")
def make_links(value):
    # Regex to match URLs
    url_pattern = re.compile(r"(https?://[^\s]+)")

    # Function to replace URLs with anchor tags
    def replace_url(match):
        url = match.group(0)
        return f'<a href="{url}" target="_blank">{url}</a>'

    # Apply the replacement
    result = url_pattern.sub(replace_url, value)
    return mark_safe(result)


def generate_links(items, url_template, title_template, as_text=False):
    """
    Generuje HTML linki dla podanych elementów lub sam tekst.
    :param items: lista obiektów (np. pomysłów, potrzeb, zakupów)
    :param url_template: szablon URL, np. "/ideas/wszystkiepomysly/edit_idea_short/?idea_id={id}"
    :param title_template: szablon tytułu linku, np. "Edycja pomysłu"
    :param as_text: czy generować sam tekst zamiast linków
    :return: połączone linki lub tekst jako string
    """
    if as_text:
        # Zwraca tylko ID elementów oddzielone kropkami
        return ".".join(str(item.id) for item in items)
    else:
        # Generuje HTML linki
        return ".".join(
            f'<a href="{url_template.format(id=item.id)}" title="{title_template.format(id=item.id)}">{item.id}</a>'
            for item in items
        )


def get_is_client(context):
    """
    Pobiera wartość zmiennej `is_client` z kontekstu.
    Jeśli `is_client` nie jest zdefiniowane, zwraca domyślną wartość False.
    """
    return context.get("is_client", False)


from django.utils.safestring import mark_safe


def get_is_client(context):
    """
    Pobiera wartość zmiennej `is_client` z kontekstu.

    :param context: Kontekst szablonu Django.
    :type context: dict
    :return: Wartość `is_client` (True lub False). Domyślnie False, jeśli zmienna nie istnieje.
    :rtype: bool
    """
    return context.get("is_client", False)


@register.simple_tag(takes_context=True)
def generate_need(context, ideas, need_instance, purchase_list):
    """
    Generuje reprezentację potrzeby z powiązanymi pomysłami i zakupami.

    :param context: Kontekst szablonu Django, zawierający m.in. wartość `is_client`.
    :type context: dict
    :param ideas: Lista powiązanych pomysłów.
    :type ideas: list[Model]
    :param need_instance: Obiekt reprezentujący potrzebę.
    :type need_instance: Model
    :param purchase_list: Lista powiązanych zakupów.
    :type purchase_list: list[Model]
    :return: HTML reprezentujący potrzebę z powiązanymi linkami lub tekstem.
    :rtype: str
    """
    is_client = get_is_client(context)
    content = [
        "Potrzeba ",
        generate_links(
            ideas,
            "/ideas/wszystkiepomysly/edit_idea_short/?idea_id={id}",
            "Edycja pomysłu",
            as_text=is_client,
        ),
        f" | <b>{need_instance.id}</b> | ",
        generate_links(
            purchase_list,
            "/purchases/wszystkiezakupy/edit_purchase_short/?purchase_id={id}",
            "Edycja zakupu",
            as_text=is_client,
        ),
    ]
    return mark_safe("".join(content))


@register.simple_tag(takes_context=True)
def generate_idea(context, idea_instance, need_list, purchase_list):
    """
    Generuje reprezentację pomysłu z powiązanymi potrzebami i zakupami.

    :param context: Kontekst szablonu Django, zawierający m.in. wartość `is_client`.
    :type context: dict
    :param idea_instance: Obiekt reprezentujący pomysł.
    :type idea_instance: Model
    :param need_list: Lista powiązanych potrzeb.
    :type need_list: list[Model]
    :param purchase_list: Lista powiązanych zakupów.
    :type purchase_list: list[Model]
    :return: HTML reprezentujący pomysł z powiązanymi linkami lub tekstem.
    :rtype: str
    """
    is_client = get_is_client(context)
    content = [f"Pomysł <b>{idea_instance.id}</b>"]

    # Generowanie linków do potrzeb
    content.append("|")
    if need_list:
        content.append(
            generate_links(
                need_list,
                "/needs/wszystkiepotrzeby/edit_need_short/?need_id={id}",
                "Edycja potrzeby",
                as_text=is_client,
            )
        )
    else:
        content.append("-")

    # Generowanie linków do zakupów
    content.append("|")
    if purchase_list:
        content.append(
            generate_links(
                purchase_list,
                "/purchases/wszystkiezakupy/edit_purchase_short/?purchase_id={id}",
                "Edycja zakupu",
                as_text=is_client,
            )
        )
    else:
        content.append("-")
    return mark_safe("".join(content))


@register.simple_tag(takes_context=True)
def generate_purchase(context, purchase_instance, ideas, need_list):
    """
    Generuje reprezentację zakupu z powiązanymi pomysłami i potrzebami.

    :param context: Kontekst szablonu Django, zawierający m.in. wartość `is_client`.
    :type context: dict
    :param purchase_instance: Obiekt reprezentujący zakup.
    :type purchase_instance: Model
    :param ideas: Lista powiązanych pomysłów.
    :type ideas: list[Model]
    :param need_list: Lista powiązanych potrzeb.
    :type need_list: list[Model]
    :return: HTML reprezentujący zakup z powiązanymi linkami lub tekstem.
    :rtype: str
    """
    is_client = get_is_client(context)
    content = [
        "Zakup | ",
        generate_links(
            ideas,
            "/ideas/wszystkiepomysly/edit_idea_short/?idea_id={id}",
            "Edycja pomysłu",
            as_text=is_client,
        ),
        " | ",
        generate_links(
            need_list,
            "/needs/wszystkiepotrzeby/edit_need_short/?need_id={id}",
            "Edycja potrzeby",
            as_text=is_client,
        ),
        " | ",
        f"<b>{purchase_instance.id}</b>",
    ]
    return mark_safe("".join(content))


@register.filter(name="none_to_warning")
def none_to_warning(value):
    if value is None:
        return mark_safe('<span style="color: red; font-weight: bold;">???</span>')
    return value


@register.filter(name="link_or_warning")
def link_or_warning(value):
    # Wyrażenie regularne do sprawdzenia, czy value jest poprawnym URL-em (http lub https)
    url_pattern = re.compile(r"^(http|https)://")

    if not value or not url_pattern.match(value):
        # Jeśli pole jest puste, None lub nie jest poprawnym URL-em, zwróć ostrzeżenie
        return mark_safe('<span style="color: red; font-weight: bold;">???</span>')

    # Jeśli pole zawiera poprawny URL, zwróć pełny link
    return mark_safe(f'<a href="{value}">link</a>')


@register.filter(name="add_class")
def add_class(value, css_class):
    return value.as_widget(attrs={"class": css_class})


@register.filter
def space_intcomma(value):
    formatted_value = floatformat(value, 2)  # Zaokrąglenie do 2 miejsc po przecinku
    formatted_value = intcomma(formatted_value)  # Dodanie przecinków
    return formatted_value.replace(",", " ")  # Zamiana przecinków na spacje


@register.filter
def format_instance(value):
    if isinstance(value, float):
        return space_intcomma(
            floatformat(value, 2)
        )  # Lub użyj space_intcomma, jeśli masz taki filtr
    return value


@register.filter
def get_kupiec(value):
    """
    Filtr sprawdzający powiązany numer EZZ w tabeli Postepowania
    i zwracający tekst z nazwą kupca lub odpowiedni komunikat.
    """
    try:
        # Pobranie numeru EZZ z rekordu Purchases
        ezz_number = value.ezz.EZZ_number

        # Znalezienie powiązanego rekordu w tabeli Postepowania
        postepowanie = Postepowania.objects.filter(numer_ZZ=ezz_number).first()

        if postepowanie and postepowanie.kupiec:
            return f"Kupiec: {postepowanie.kupiec}"
        else:
            return "Kupiec nieprzypisany"
    except AttributeError:
        return "Kupiec nieprzypisany"


@register.filter
def get_SAP_CRM(value):
    """
    Filtr sprawdzający powiązany numer EZZ w tabeli Postepowania
    i zwracający tekst z numerem SAP_CRM  lub odpowiedni komunikat.
    """
    try:
        # Pobranie numeru EZZ z rekordu Purchases
        ezz_number = value.ezz.EZZ_number

        # Znalezienie powiązanego rekordu w tabeli Postepowania
        postepowanie = Postepowania.objects.filter(numer_ZZ=ezz_number).first()

        if postepowanie and postepowanie.numer_SRM_SAP:
            return f"SAP_CRM: {postepowanie.numer_SRM_SAP}"
        else:
            return "SAP_CRM_NIEZNAY"
    except AttributeError:
        return "SAP_CRM_NIEZNAY"


@register.filter
def get_connect(value):
    """
    Filtr sprawdzający powiązany numer EZZ w tabeli Postepowania
    i zwracający tekst ze sttusem w Connect  lub odpowiedni komunikat.
    """
    try:
        # Pobranie numeru EZZ z rekordu Purchases
        ezz_number = value.ezz.EZZ_number

        # Znalezienie powiązanego rekordu w tabeli Postepowania
        postepowanie = Postepowania.objects.filter(numer_ZZ=ezz_number).first()

        if postepowanie and postepowanie.connect:
            return f"Connect: {postepowanie.connect}"
        else:
            return "---"
    except AttributeError:
        return "---"
