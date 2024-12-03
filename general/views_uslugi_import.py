import re
from django.shortcuts import render
from general.models import uslugi
from django.core.exceptions import ValidationError
from zipfile import BadZipFile
from django.shortcuts import render, redirect
from purchases.forms import ImportForm
import openpyxl
from django.views.decorators.csrf import csrf_protect
from general.common_context import common_context


def uslugi_row_verification(row):
    numer = row[0]
    nazwa = row[1]

    # Check if numer starts with 'PGN_'  'ZOP_'and has valid format
    if not numer or not re.match(r"^(PGN_|ZOP_)\d+(\.\d+)*$", numer.strip()):
        return False, "Invalid 'numer' format. Must start with PGN_ or ZOP_"

    # Check if nazwa is non-empty
    if not nazwa or len(nazwa.strip()) == 0:
        return False, "'nazwa' is empty"

    return True, None


@csrf_protect
def uslugi_import(request):
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
                    is_valid, reason = uslugi_row_verification(row)
                    number_of_records += 1
                    if is_valid:
                        record = uslugi.objects.filter(numer=row[0].strip()).first()
                        if not record:
                            record = uslugi(numer=row[0].strip())
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
                return render(request, "general/uslugi_import.html", context)

            except (
                ValidationError,
                KeyError,
                BadZipFile,
                NameError,
                TypeError,
                OSError,
                IOError,
            ) as e:
                context = {"error": e}
                context.update(common_context(request))
                return render(request, "general/uslugi_import.html", context)

    form = ImportForm()
    context = {"form": form}
    context.update(common_context(request))
    return render(request, "general/uslugi_import_form.html", context)
