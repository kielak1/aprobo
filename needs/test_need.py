import logging

from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.forms.models import ModelChoiceIterator, ModelMultipleChoiceField
from dal import autocomplete
from django.views.decorators.csrf import csrf_protect
from needs.models import Needs
from general.models import uslugi

logger = logging.getLogger(__name__)


@csrf_protect
def testauto(request):
    """
    Przykładowa funkcja widoku wiążąca usługi z Potrzebą
    """
    need_id = request.GET.get("need_id")
    logger.error("need_id= %s", need_id)
    need_instance = get_object_or_404(Needs, id=need_id)

    if request.method == "POST":
        need_instance.subject = request.POST.get("subject")
        uslugi_ids = request.POST.getlist("uslugi")
        need_instance.uslugi.set(uslugi_ids)
        need_instance.save()
        return redirect(f"/needs/testauto?need_id={need_id}")

    dal_media = autocomplete.Select2().media

    url = reverse_lazy("uslugi-autocomplete")
    field = ModelMultipleChoiceField(queryset=uslugi.objects.all())

    widget = autocomplete.ModelSelect2Multiple(
        url=url,
        attrs={
            "class": "selector",
            "id": "uslugi",
            "data-placeholder": "Wybierz usługi",
        },
    )
    widget.choices = ModelChoiceIterator(field)

    default = list(need_instance.uslugi.all().values_list("id", flat=True))
    logger.error("default= %s", default)
    widget_html = widget.render("uslugi", default)

    context = {
        "dal_media": dal_media,
        "widget_html": widget_html,
        "need_instance": need_instance,
    }

    return render(request, "testauto.html", context)


from django import forms
from dal import autocomplete
from needs.models import Needs
from general.models import uslugi


class DynamicAutoFormShort(forms.ModelForm):
    class Meta:
        model = Needs
        fields = ["subject", "uslugi"]
        widgets = {
            "uslugi": autocomplete.ModelSelect2Multiple(
                url="uslugi-autocomplete",
                attrs={
                    "class": "selector",
                    "data-placeholder": "Wybierz usługi",
                },
            ),
        }


import logging
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.csrf import csrf_protect
from needs.models import Needs


logger = logging.getLogger(__name__)


@csrf_protect
def testautodynamic(request):
    """
    Funkcja widoku edytująca potrzebę z użyciem formularza DynamicAutoFormShort
    """
    need_id = request.GET.get("need_id")
    logger.error("need_id= %s", need_id)
    need_instance = get_object_or_404(Needs, id=need_id)

    if request.method == "POST":
        form = DynamicAutoFormShort(request.POST, instance=need_instance)

        if "Anuluj" in request.POST:
            return redirect(f"/needs/testautodynamic?need_id={need_id}")

        if form.is_valid():
            form.save()
            return redirect(f"/needs/testautodynamic?need_id={need_id}")
    else:
        form = DynamicAutoFormShort(instance=need_instance)

    context = {
        "form": form,
        "need_instance": need_instance,
    }

    return render(request, "testautodynamic.html", context)
