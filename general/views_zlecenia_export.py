from django.http import HttpResponse
from django.views.decorators.csrf import csrf_protect
import openpyxl
from general.models import zlecenia_kontrolingowe


@csrf_protect
def zlecenia_export(request):
    if not request.user.groups.filter(name="accountant").exists():
        target_if_no_rights = f"/account/login"
        return redirect(target_if_no_rights)
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Zlecenia Kontrolingowe"
    # Fetch data from database
    zlecenia = zlecenia_kontrolingowe.objects.all()
    # Add data to worksheet
    for zlecenie in zlecenia:
        ws.append([zlecenie.numer, zlecenie.nazwa])
    # Prepare the response
    response = HttpResponse(
        content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
    response["Content-Disposition"] = (
        'attachment; filename="zlecenia_kontrolingowe.xlsx"'
    )
    # Save the workbook to the response
    wb.save(response)
    return response
