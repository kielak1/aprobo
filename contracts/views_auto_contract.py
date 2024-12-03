from .models import Contracts
from django.shortcuts import redirect, render
from datetime import date
from django.urls import resolve, Resolver404
from urllib.parse import urlparse
from django.views.decorators.csrf import csrf_protect
from general.models import Variable
from django import forms


@csrf_protect
def auto_contract(request):
    # Sprawdzenie uprawnień użytkownika
    if not request.user.groups.filter(name="contract_editor").exists():
        return redirect("/account/login")

    if request.method == "POST":
        form = forms.Form(request.POST)
        if form.is_valid():
            # Logika przetwarzania danych z Contracts
            rekordy = Contracts.objects.select_related("cbu", "ezzc").all()

            to_update = []
            for rekord in rekordy:
                modified = False

                if rekord.cbu is not None:
                    if (
                        rekord.cbu.data_zawarcia is not None
                        and rekord.cbu.data_zawarcia != date(1990, 1, 1)
                    ):
                        rekord.data_zawarcia = rekord.cbu.data_zawarcia
                        modified = True
                    if rekord.cbu.sygnatura is not None:
                        rekord.numer_umowy = rekord.cbu.sygnatura
                        modified = True
                    if rekord.cbu.wartosc_wydatkowa is not None:
                        rekord.wartosc = rekord.cbu.wartosc_wydatkowa
                        modified = True
                    if rekord.cbu.nazwa_kontrahenta is not None:
                        rekord.kontrahent = rekord.cbu.nazwa_kontrahenta
                        modified = True

                if rekord.ezzc is not None:
                    if (
                        rekord.ezzc.od_kiedy is not None
                        and rekord.ezzc.od_kiedy != date(1990, 1, 1)
                    ):
                        rekord.data_zawarcia = rekord.ezzc.od_kiedy
                        modified = True
                    if rekord.ezzc.sygnatura is not None:
                        rekord.numer_umowy = rekord.ezzc.sygnatura
                        modified = True
                    if rekord.ezzc.wartosc is not None:
                        rekord.wartosc = rekord.ezzc.wartosc
                        modified = True
                    if rekord.ezzc.waluta is not None:
                        rekord.waluta = rekord.ezzc.waluta
                        modified = True
                    if rekord.ezzc.dostawca is not None:
                        rekord.kontrahent = rekord.ezzc.dostawca
                        modified = True

                if rekord.data_zawarcia < date(2018, 1, 1) or rekord.wartosc < 2000:
                    rekord.obslugiwana = False
                    modified = True

                if modified:
                    to_update.append(rekord)

            # Zbiorczy zapis zmodyfikowanych rekordów
            if to_update:
                Contracts.objects.bulk_update(
                    to_update,
                    [
                        "data_zawarcia",
                        "numer_umowy",
                        "wartosc",
                        "waluta",
                        "kontrahent",
                        "obslugiwana",
                    ],
                )

            # Ustawienie statusu importu umów
            Variable.set("status_importu_umow", 0)

            # Przekierowanie po zakończeniu operacji
            return redirect("index_contracts")
    else:
        form = forms.Form()

    # Wyświetlanie formularza w szablonie
    context = {"form": form}
    return render(request, "auto_contract.html", context)
