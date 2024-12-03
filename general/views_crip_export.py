from django.http import HttpResponse
from django.views.decorators.csrf import csrf_protect
import openpyxl
from general.models import Crip


@csrf_protect
def crip_export(request):
    if not request.user.groups.filter(name="accountant").exists():
        target_if_no_rights = f"/account/login"
        return redirect(target_if_no_rights)
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Crip"
    # Fetch data from database
    lista_crip = Crip.objects.all()
    # Add data to worksheet
    for crip_element in lista_crip:
        ws.append(
            [
                crip_element.crip_id,
                crip_element.nazwa_projektu,
                crip_element.jednostka,
                crip_element.sekcja,
            ]
        )

    # Prepare the response
    response = HttpResponse(
        content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
    response["Content-Disposition"] = 'attachment; filename="crip.xlsx"'
    # Save the workbook to the response
    wb.save(response)
    return response
