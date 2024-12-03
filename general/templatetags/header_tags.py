from django import template
from general.parametry import get_param_int
import unicodedata

register = template.Library()

@register.inclusion_tag("header_field.html", takes_context=True)
def header_field(context, warunek, field, instance, etykieta, klasa):
    request = context["request"]
    szerokosc = get_param_int("szerokosc", 1000)
    szerokosc_pola = round(szerokosc / 4) - 1

    # Konwersja zmiennej 'klasa' na ciąg znaków, zamiana spacji na myślniki i usunięcie polskich znaków
    klasa = str(klasa).replace(" ", "-")
    klasa = "".join(
        c
        for c in unicodedata.normalize("NFD", klasa)
        if unicodedata.category(c) != "Mn"
    )

    # Uaktualniamy kontekst bez przekazywania samego context
    updated_context = {
        "warunek": warunek,
        "field": field,
        "instance": instance,
        "etykieta": etykieta,
        "klasa": klasa,
        "szerokosc_pola": szerokosc_pola,
        "parameters": request.GET,
    }

    return updated_context
