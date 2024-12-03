from django.http import HttpResponse
from django.views.decorators.csrf import csrf_protect
import openpyxl
from general.models import uslugi


@csrf_protect
def uslugi_export(request):
    if not request.user.groups.filter(name="accountant").exists():
        target_if_no_rights = f"/account/login"
        return redirect(target_if_no_rights)
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Usługi"
    # Fetch data from database
    lista_uslug = uslugi.objects.all()
    # Add data to worksheet
    for usluga in lista_uslug:
        ws.append([usluga.numer, usluga.nazwa])
    # Prepare the response
    response = HttpResponse(
        content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
    response["Content-Disposition"] = 'attachment; filename="uslugi.xlsx"'
    # Save the workbook to the response
    wb.save(response)
    return response
