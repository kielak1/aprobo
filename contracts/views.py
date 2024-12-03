from django.shortcuts import render, redirect
from .models import EZZC, CBU, Contracts

from general.common_dashboard import common_dashboard
from django.views.decorators.csrf import csrf_protect
from general.models import Variable
from django import forms
from general.common_context import common_context
import logging

logger = logging.getLogger("avantic")


@csrf_protect
def index(request):
    if not request.user.groups.filter(name="contract_viewer").exists():
        target_if_no_rights = f"/account/login"
        return redirect(target_if_no_rights)
    return common_dashboard("contracts/index.html", request)


@csrf_protect
def ezzc_add(request):
    # Sprawdzenie uprawnień użytkownika
    if not request.user.groups.filter(name="contract_editor").exists():
        return redirect("/account/login")

    if request.method == "POST":
        form = forms.Form(request.POST)
        logger.warning("form POST")
        if form.is_valid():
            logger.warning("form valid")
            # Pobranie rekordów z tabeli EZZC, które jeszcze nie mają powiązania w tabeli Contracts
            ezzc_without_contract = EZZC.objects.filter(ezzc__isnull=True)

            for ezzc_record in ezzc_without_contract:
                contracts_record = Contracts.objects.filter(
                    cbu__sygnatura=ezzc_record.sygnatura
                ).first()
                if contracts_record:
                    contracts_record.ezzc = ezzc_record
                    contracts_record.save()
                else:
                    Contracts.objects.create(
                        subject=ezzc_record.przedmiot, ezzc=ezzc_record
                    )

            cbu_without_contract = CBU.objects.filter(cbu__isnull=True)
            for cbu_record in cbu_without_contract:
                contracts_record = Contracts.objects.filter(
                    ezzc__sygnatura=cbu_record.sygnatura
                ).first()
                if contracts_record:
                    contracts_record.cbu = cbu_record
                    contracts_record.save()
                else:
                    Contracts.objects.create(subject=cbu_record.temat, cbu=cbu_record)

            # Ustawienie statusu importu umów
            Variable.set("status_importu_umow", 2)

            # Przekierowanie po zakończeniu
            return redirect("auto_contract")
    else:
        form = forms.Form()

    context = common_context(request)
    context.update({"form": form})
    return render(request, "ezzc_add.html", context)


@csrf_protect
def pusty(request):
    return render(request, "pusty.html", {})
