from datetime import datetime, date
from django.db.models.query import QuerySet
from general.models import Sposob_wyceny, Crip
from decimal import Decimal, ROUND_HALF_UP
import logging

# Pobierz logger
logger = logging.getLogger("django")


def konwertuj_wartosci_do_porownania(old_value, new_value):
    """
    Konwertuje wartości do porównywalnego formatu, jeśli to konieczne.

    Args:
        old_value: Stara wartość do porównania.
        new_value: Nowa wartość do porównania.

    Returns:
        tuple: Zawiera skonwertowane wartości (old_value, new_value) i flagę czy_konwersja.
    """
    czy_konwersja = False

    logger.debug(
        "old=%s (%s), new=%s (%s)",
        old_value,
        type(old_value),
        new_value,
        type(new_value),
    )

    if old_value is None:
        old_value = "???"
    if new_value is None:
        new_value = "???"

    if isinstance(old_value, str) and isinstance(new_value, str):
        old_value = old_value.strip()
        new_value = new_value.strip()
        czy_konwersja = True
    elif isinstance(new_value, Decimal) and isinstance(old_value, (int, float)):
        old_value = Decimal(old_value).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
        new_value = Decimal(new_value).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
        czy_konwersja = True
    elif isinstance(old_value, bool) or isinstance(new_value, bool):
        old_value = bool(old_value) if old_value != "???" else "???"
        new_value = bool(new_value) if new_value != "???" else "???"
        czy_konwersja = True
    elif isinstance(old_value, (int, float)) and isinstance(new_value, (int, float)):
        old_value = float(old_value)
        new_value = float(new_value)
        czy_konwersja = True
    elif isinstance(old_value, (date, datetime)) and isinstance(
        new_value, (date, datetime)
    ):
        old_value = old_value.isoformat()
        new_value = new_value.isoformat()
        czy_konwersja = True
    elif isinstance(old_value, list) and isinstance(new_value, QuerySet):
        old_value = ", ".join([str(item) for item in old_value])
        new_value = ", ".join([str(item) for item in new_value])
        czy_konwersja = True
    elif isinstance(new_value, QuerySet):
        old_value = ", ".join([str(item) for item in old_value.all()])
        new_value = ", ".join([str(item) for item in new_value])
        czy_konwersja = True
    elif isinstance(new_value, (Sposob_wyceny, Crip)):
        old_value = str(old_value) if old_value else ""
        new_value = str(new_value)
        czy_konwersja = True

    return old_value, new_value, czy_konwersja
