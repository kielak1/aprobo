from django.core.exceptions import ValidationError
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_protect
from zipfile import BadZipFile
import openpyxl
from django.db import transaction
import logging

from general.models import Crip
from .forms import ImportForm
import re
from general.common_context import common_context

# Ustawienia loggera
logger = logging.getLogger("avantic")


def crip_row_verification(row):
    """Weryfikuje, czy wiersz spełnia oczekiwany format i długości pól."""

    if not isinstance(row[0], str) or not row[0].strip():
        return False, "crip_id jest pusty"

    id_pattern = r"^PL-[A-Z]{3}-[A-Z]{3}-\d{4}-\d{6}$"
    if not re.match(id_pattern, row[0].strip()):
        return False, "Niepoprawny format crip_id"

    if len(row[0].strip()) > 23:
        return False, "crip_id przekracza dopuszczalną długość (23 znaki)"
    if len(row[1].strip()) > 200:
        return False, "Nazwa projektu przekracza dopuszczalną długość (200 znaków)"
    if len(row[2].strip()) > 4:
        return False, "Jednostka przekracza dopuszczalną długość (4 znaki)"
    if len(row[3].strip()) > 10:
        return False, "Sekcja przekracza dopuszczalną długość (10 znaków)"

    return True, None


@csrf_protect
@transaction.atomic  # Użycie transakcji dla operacji na bazie danych
def crip_import(request):
    """Obsługa importu danych CRIP z pliku Excel."""
    if not request.user.groups.filter(name="accountant").exists():
        return redirect("/account/login")

    form = ImportForm(request.POST or None, request.FILES or None)

    if request.method == "POST" and form.is_valid():
        try:
            excel_file = request.FILES["excel_file"]
            wb = openpyxl.load_workbook(excel_file)
            ws = wb.active

            existing_records = {crip.crip_id: crip for crip in Crip.objects.all()}
            lista = []  # Poprawnie zaimportowane wiersze
            odrzucone_wiersze = []  # Wiersze odrzucone w procesie weryfikacji
            number_of_records = 0
            number_of_new_records = 0

            for row in ws.iter_rows(values_only=True):
                is_valid, reason = crip_row_verification(row)
                if is_valid:
                    number_of_records += 1
                    record = existing_records.get(row[0].strip())
                    if not record:
                        record = Crip(crip_id=row[0].strip())
                        number_of_new_records += 1
                        lista.append((row[0], row[1], row[2], row[3]))
                    record.nazwa_projektu = row[1]
                    record.jednostka = row[2]
                    record.sekcja = row[3]
                    record.save()
                else:
                    odrzucone_wiersze.append({"row": row, "reason": reason})

            wb.close()

            context = {
                "lista": lista,
                "number_of_records": number_of_records,
                "number_of_new_records": number_of_new_records,
                "odrzucone_wiersze": odrzucone_wiersze,
            }
            context.update(common_context(request))
            return render(request, "purchases/crip_import.html", context)

        except (
            ValidationError,
            KeyError,
            BadZipFile,
            NameError,
            TypeError,
            IOError,
        ) as e:
            logger.error(f"Błąd podczas importu CRIP: {e}")
            error_message = "Wystąpił błąd podczas przetwarzania pliku. Proszę sprawdzić format pliku."
            context = {"error": error_message}
            context.update(common_context(request))
            return render(request, "purchases/crip_import.html", context)

    context = {"form": form}
    context.update(common_context(request))
    return render(request, "purchases/crip_import_form.html", context)
