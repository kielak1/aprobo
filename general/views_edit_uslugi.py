from django import forms
from django.shortcuts import render, redirect
from general.models import uslugi

from django.urls import resolve, Resolver404
from urllib.parse import urlparse
from purchases.models import Purchases
from needs.models import Needs
from django.views.decorators.csrf import csrf_protect
from general.common_context import common_context


class DynamicuslugisFormShort(forms.ModelForm):

    numer = forms.CharField(
        widget=forms.Textarea(attrs={"rows": 1, "cols": 42}), required=False
    )
    nazwa = forms.CharField(
        widget=forms.Textarea(attrs={"rows": 1, "cols": 82}), required=False
    )

    class Meta:
        model = uslugi
        fields = "__all__"


def validate_and_return_url(request, default_url="/general/uslugi-list/"):
    full_url = request.session.get("uslugi_edit", default_url)
    path = urlparse(full_url).path

    try:
        resolve(path)  # Sprawdza, czy ścieżka jest poprawna
        return full_url  # Zwraca pełny URL, włącznie z parametrami zapytania
    except Resolver404:
        return default_url  # Zwraca URL domyślny, jeśli podany URL jest nieprawidłowy


@csrf_protect
def return_uslugi_path(request):
    return_page = validate_and_return_url(request)
    if "uslugi_edit" in request.session:
        del request.session["uslugi_edit"]
    return return_page


def get_needs_and_purchases(uslugi_instance):
    if uslugi_instance.id is None:
        return []  # , []  # Zwróć puste listy, jeśli uslugi_instance nie jest zapisany

    # Pobierz listę potrzeb (Needs) powiązanych z obiektem uslugi
    need_list = Needs.objects.filter(uslugi=uslugi_instance).order_by(
        "-wymagana_data_realizacji"
    )

    # Pobierz listę zakupów (Purchases) powiązanych z obiektem uslugi
    # purchase_list = Purchases.objects.filter(uslugi_id=uslugi_instance)
    # return need_list, purchase_list
    return need_list


def get_uslugi_context(form, uslugi_instance, request):

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
    if uslugi_instance.id is None:
        full = False
    else:
        full = True

    #  need_list, purchase_list = get_needs_and_purchases(uslugi_instance)

    need_list = get_needs_and_purchases(uslugi_instance)
    context = {
        "form": form,
        "is_superuser": is_superuser,
        "is_accountant": is_accountant,
        "is_advanced": is_advanced,
        "is_freeze": is_freeze,
        "uslugi_instance": uslugi_instance,
        "need_list": need_list,
        #           'purchase_list': purchase_list,
        "full": full,
    }
    context.update(common_context(request))
    return context


@csrf_protect
def edit_uslugi_short(request):
    if "uslugi_edit" not in request.session:
        request.session["uslugi_edit"] = request.META.get(
            "HTTP_REFERER", "/general/uslugi-list/"
        )
    uslugi_id = request.GET.get("numer")
    uslugi_instance = uslugi.objects.get(pk=uslugi_id)

    context = get_uslugi_context("", uslugi_instance, request)
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
        display_fields.extend(
            [
                "numer",
                "nazwa",
            ]
        )

    if request.method == "POST":
        form = DynamicuslugisFormShort(request.POST, instance=uslugi_instance)
        if "Anuluj" in request.POST:
            return redirect(return_uslugi_path(request))
        if form.is_valid():
            context = get_uslugi_context(form, uslugi_instance, request)
            if "Zapisz" in request.POST:
                if is_superuser or is_accountant:
                    form.save()
                return render(request, "edit_uslugi_short.html", context)
            if "Submit" in request.POST:
                if is_superuser or is_accountant:
                    form.save()
                return redirect(return_uslugi_path(request))
            if "Usun" in request.POST:
                if is_superuser or is_accountant:
                    uslugi_instance.delete()
                return redirect(return_uslugi_path(request))
        else:
            pass
    else:
        form = DynamicuslugisFormShort(instance=uslugi_instance)
    context = get_uslugi_context(form, uslugi_instance, request)
    return render(request, "edit_uslugi_short.html", context)


@csrf_protect
def edit_uslugi_short_new(request):
    if "uslugi_edit" not in request.session:
        request.session["uslugi_edit"] = request.META.get(
            "HTTP_REFERER", "/general/uslugi-list/"
        )
    uslugi_instance = uslugi()

    context = get_uslugi_context("", uslugi_instance, request)

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
        display_fields.extend(
            [
                "numer",
                "nazwa",
            ]
        )

    if request.method == "POST":
        form = DynamicuslugisFormShort(request.POST, instance=uslugi_instance)
        if "Anuluj" in request.POST:
            return redirect(return_uslugi_path(request))

        if form.is_valid():
            context = get_uslugi_context(form, uslugi_instance, request)
            if "Zapisz" in request.POST:
                if is_superuser or is_accountant:
                    form.save()
                    uslugi_instance.save()
                    uslugi_id = uslugi_instance.id
                    url = f"/general/uslug-list/edit_uslugi_short/?numer={uslugi_id}"
                    return redirect(url)
        else:
            pass
    else:
        form = DynamicuslugisFormShort(instance=uslugi_instance)
    context = get_uslugi_context(form, uslugi_instance, request)
    return render(request, "edit_uslugi_short.html", context)
