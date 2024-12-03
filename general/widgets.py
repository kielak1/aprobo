import locale
import logging
import re
from django import forms
from contracts.models import Contracts


logger = logging.getLogger("avantic")


class FormattedFloatWidget(forms.TextInput):
    def __init__(self, *args, **kwargs):
        # Dodanie domyślnych atrybutów, aby ograniczyć wprowadzanie znaków do cyfr i kropki
        attrs = kwargs.get("attrs", {})
        attrs.update(
            {
                "pattern": r"^[0-9\s,]*\.?[0-9]*$",
                "inputmode": "decimal",
                "style": "width: 14ch;",
            }
        )
        kwargs["attrs"] = attrs

        super().__init__(*args, **kwargs)

        # Ustawienie dla polskiej lokalizacji
        locale.setlocale(locale.LC_ALL, "pl_PL.UTF-8")

    def format_value(self, value):
        if value is None:
            return ""
        # Formatowanie liczby z odstępem co trzy cyfry
        return locale.format_string("%.2f", value, grouping=True)

    def value_from_datadict(self, data, files, name):
        value = data.get(name, None)
        if value:
            # Usunięcie wszystkich rodzajów spacji przed konwersją do float
            value = re.sub(r"\s+", "", value)
            return float(value.replace(",", "."))
        return None

def create_float_field(
    label="float field", max_digits=12, decimal_places=2, width="14ch", required=False
):
    return forms.DecimalField(
        label=label,
        max_digits=max_digits,
        decimal_places=decimal_places,
        widget=FormattedFloatWidget(
            attrs={"placeholder": "0.00", "style": f"width: {width};"}
        ),
        required=required,
    )


class CharCountTextArea(forms.Textarea):
    template_name = "widgets/char_count_textinput.html"

    def __init__(self, attrs=None):
        default_attrs = {"rows": 3}
        if attrs:
            default_attrs.update(attrs)
        super().__init__(default_attrs)
        self.max_length = default_attrs.get("maxlength", None)

    def get_context(self, name, value, attrs):

        context = super().get_context(name, value, attrs)

        # Usunięcie `cols` z `attrs`, jeśli jest obecny
        if "cols" in context["widget"]["attrs"]:
            del context["widget"]["attrs"]["cols"]

        context["max_length"] = self.max_length
        return context


def create_char_count_field(
    field_name, model=Contracts, rows=3, cols=117, required=False, attrs=None
):
    # Inicjalizacja attrs jako pustego słownika, jeśli nie został przekazany
    if attrs is None:
        attrs = {}
    max_length = model._meta.get_field(field_name).max_length
    # Przeliczanie wartości cols na szerokość w pikselach
    col_width_px = round(cols * 8.5)
    # Ustawienie stylu szerokości
    default_style = f"width: {col_width_px}px !important;"

    # Usunięcie atrybutu `cols` z `attrs` (jeśli istnieje)
    attrs.pop("cols", None)
    # Sprawdzenie, czy istnieje atrybut style w attrs i połączenie z domyślnym stylem
    if "style" in attrs:
        # Dodanie przeliczonej szerokości do istniejącego stylu
        attrs["style"] += f" {default_style}"
    else:
        # Ustawienie przeliczonej szerokości jako nowy styl
        attrs["style"] = default_style
    # Aktualizacja atrybutów bez przekazywania `cols`
    attrs.update(
        {
            "maxlength": max_length,
            "rows": rows,
        }
    )
    return forms.CharField(
        required=required,
        max_length=max_length,
        widget=CharCountTextArea(attrs=attrs),
    )
