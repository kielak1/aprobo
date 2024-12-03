from django.shortcuts import render, redirect
from general.models import zlecenia_kontrolingowe
from django.core.exceptions import ValidationError
from zipfile import BadZipFile
from purchases.forms import ImportForm
import openpyxl
from django.views.decorators.csrf import csrf_protect
from general.common_context import common_context
import logging
import re

logger = logging.getLogger("avantic")

# Regular expressions for verification
order_code_pattern = re.compile(r"^C\d{5}[A-Z0]{2}\d{4}$")
description_pattern = re.compile(r"^[\w\s\.\:\-,&–—ąćęłńóśźżĄĆĘŁŃÓŚŹŻ\'\(\)/]+$")


def zlecenia_row_verification(row):
    """Verify that the row has valid order code and description, returning reason if invalid."""
    # Validate the order code (first column)
    if not order_code_pattern.match(row[0].strip()):
        return False, f"Invalid order code: {row[0]}"

    # Validate the description (second column)
    if not description_pattern.match(row[1].strip()):
        return False, f"Invalid description: {row[1]}"

    return True, None


@csrf_protect
def zlecenia_import(request):
    if not request.user.groups.filter(name="accountant").exists():
        return redirect("/account/login")

    if request.method == "POST":
        form = ImportForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                excel_file = request.FILES["excel_file"]
                wb = openpyxl.load_workbook(excel_file)
                ws = wb.active
                lista = []
                rejected = []
                number_of_records = 0
                number_of_new_records = 0

                for row in ws.iter_rows(values_only=True):
                    is_valid, reason = zlecenia_row_verification(row)
                    if is_valid:
                        number_of_records += 1
                        record = zlecenia_kontrolingowe.objects.filter(
                            numer=row[0].strip()
                        ).first()
                        if not record:
                            record = zlecenia_kontrolingowe(numer=row[0].strip())
                            number_of_new_records += 1
                            lista.append((row[0], row[1]))
                        record.nazwa = row[1]
                        record.save()
                    else:
                        rejected.append((row[0], row[1], reason))

                wb.close()
                context = {
                    "lista": lista,
                    "rejected": rejected,
                    "number_of_records": number_of_records,
                    "number_of_new_records": number_of_new_records,
                }
                context.update(common_context(request))
                return render(request, "general/zlecenia_import.html", context)

            except (ValidationError, KeyError, BadZipFile, NameError, TypeError) as e:
                logger.error(f"Błąd: {e}")
                context = {"error": e}
                context.update(common_context(request))
                return render(request, "general/zlecenia_import.html", context)
    else:
        form = ImportForm()

    context = {"form": form}
    context.update(common_context(request))
    return render(request, "general/zlecenia_import_form.html", context)
