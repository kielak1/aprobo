from django import forms
from django.shortcuts import render, redirect
from general.models import Crip

from django.urls import resolve, Resolver404
from urllib.parse import urlparse
from purchases.models import Purchases
from needs.models import Needs
from django.views.decorators.csrf import csrf_protect
from general.common_context import common_context


class DynamiccripsFormShort(forms.ModelForm):

    crip_id = forms.CharField(
        widget=forms.Textarea(attrs={"rows": 1, "cols": 42}), required=False
    )
    nazwa_projektu = forms.CharField(
        widget=forms.Textarea(attrs={"rows": 1, "cols": 82}), required=False
    )
    jednostka = forms.CharField(
        widget=forms.Textarea(attrs={"rows": 1, "cols": 4}), required=False
    )
    sekcja = forms.CharField(
        widget=forms.Textarea(attrs={"rows": 1, "cols": 4}), required=False
    )

    class Meta:
        model = Crip
        fields = "__all__"


def validate_and_return_url(request, default_url="/general/crip-list/"):
    full_url = request.session.get("crip_edit", default_url)
    path = urlparse(full_url).path

    try:
        resolve(path)  # Sprawdza, czy ścieżka jest poprawna
        return full_url  # Zwraca pełny URL, włącznie z parametrami zapytania
    except Resolver404:
        return default_url  # Zwraca URL domyślny, jeśli podany URL jest nieprawidłowy


@csrf_protect
def return_crip_path(request):
    return_page = validate_and_return_url(request)
    if "crip_edit" in request.session:
        del request.session["crip_edit"]
    return return_page


def get_needs_and_purchases(crip_instance):
    if crip_instance.id is None:
        return [], []  # Zwróć puste listy, jeśli crip_instance nie jest zapisany

    # Pobierz listę potrzeb (Needs) powiązanych z obiektem Crip
    need_list = Needs.objects.filter(pozycje_z_planu_CRIP=crip_instance).order_by(
        "-wymagana_data_realizacji"
    )
    # Pobierz listę zakupów (Purchases) powiązanych z obiektem Crip
    purchase_list = Purchases.objects.filter(crip_id=crip_instance)
    return need_list, purchase_list


def get_crip_context(form, crip_instance, request):

    is_superuser = False
    is_advanced = False
    is_accountant = False
    if request.user.is_authenticated:
        if request.user.groups.filter(name="superuser").exists():
            is_superuser = True
            is_accountant = True
        # is_advanced = True
        if request.user.groups.filter(name="advanced").exists():
            is_advanced = True
        if request.user.groups.filter(name="accountant").exists():
            is_accountant = True

    is_freeze = True
    if is_superuser or is_accountant:
        is_freeze = False
    if crip_instance.id is None:
        full = False
    else:
        full = True

    need_list, purchase_list = get_needs_and_purchases(crip_instance)
    context = {
        "form": form,
        "is_superuser": is_superuser,
        "is_accountant": is_accountant,
        "is_advanced": is_advanced,
        "is_freeze": is_freeze,
        "crip_instance": crip_instance,
        "need_list": need_list,
        "purchase_list": purchase_list,
        "full": full,
    }
    context.update(common_context(request))
    return context


@csrf_protect
def edit_crip_short(request):
    if "crip_edit" not in request.session:
        request.session["crip_edit"] = request.META.get(
            "HTTP_REFERER", "/general/crip-list/"
        )
    crip_id = request.GET.get("crip_id")
    crip_instance = Crip.objects.get(pk=crip_id)

    context = get_crip_context("", crip_instance, request)
    is_superuser = context["is_superuser"]
    is_freeze = context["is_freeze"]
    is_accountant = context["is_accountant"]
    is_advanced = context["is_advanced"]

    target_if_no_rights = f"/account/login"
    if request.user.is_authenticated:
        if not is_superuser and not is_accountant and not is_advanced:
            return redirect(target_if_no_rights)
    else:
        return redirect(target_if_no_rights)

    display_fields = []

    if not is_freeze:
        display_fields.extend(["crip_id", "nazwa_projektu", "jednostka", "sekcja"])

    if request.method == "POST":
        form = DynamiccripsFormShort(request.POST, instance=crip_instance)
        if "Anuluj" in request.POST:
            return redirect(return_crip_path(request))
        if form.is_valid():
            context = get_crip_context(form, crip_instance, request)
            if "Zapisz" in request.POST:
                if is_superuser or is_accountant:
                    form.save()
                return render(request, "edit_crip_short.html", context)
            if "Submit" in request.POST:
                if is_superuser or is_accountant:
                    form.save()
                return redirect(return_crip_path(request))
            if "Usun" in request.POST:
                if is_superuser or is_accountant:
                    crip_instance.delete()
                return redirect(return_crip_path(request))
        else:
            pass
    else:
        form = DynamiccripsFormShort(instance=crip_instance)
    context = get_crip_context(form, crip_instance, request)
    context.update(common_context(request))
    return render(request, "edit_crip_short.html", context)


@csrf_protect
def edit_crip_short_new(request):
    if "crip_edit" not in request.session:
        request.session["crip_edit"] = request.META.get(
            "HTTP_REFERER", "/general/crip-list/"
        )
    crip_instance = Crip()

    context = get_crip_context("", crip_instance, request)

    is_superuser = context["is_superuser"]
    is_freeze = context["is_freeze"]
    is_accountant = context["is_accountant"]

    target_if_no_rights = f"/account/login"
    if request.user.is_authenticated:
        if not is_superuser and not is_accountant:
            return redirect(target_if_no_rights)
    else:
        return redirect(target_if_no_rights)

    display_fields = []

    if not is_freeze:
        display_fields.extend(["crip_id", "nazwa_projektu", "jednostka", "sekcja"])

    if request.method == "POST":
        form = DynamiccripsFormShort(request.POST, instance=crip_instance)
        if "Anuluj" in request.POST:
            return redirect(return_crip_path(request))

        if form.is_valid():
            context = get_crip_context(form, crip_instance, request)
            if "Zapisz" in request.POST:
                if is_superuser or is_accountant:
                    form.save()
                    crip_instance.save()
                    crip_id = crip_instance.id
                    url = f"/general/crip-list/edit_crip_short/?crip_id={crip_id}"
                    return redirect(url)
        else:
            pass
    else:
        form = DynamiccripsFormShort(instance=crip_instance)
    context = get_crip_context(form, crip_instance, request)
    context.update(common_context(request))
    return render(request, "edit_crip_short.html", context)
