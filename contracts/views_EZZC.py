from django.shortcuts import render, redirect
from .models import EZZC
from django_filters.views import FilterView
from django_tables2.views import SingleTableMixin
import django_filters
import django_tables2 as tables
from django.contrib.auth.mixins import LoginRequiredMixin
from general.common_context import common_context


class EZZCTable(tables.Table):
    class Meta:
        model = EZZC
        fields = (
            "sygnatura",
            "sygnatura_nadrzedna",
            "przedmiot",
            "numer_SRM",
            "numer_ZZZT",
            "wartosc",
            "typ_umowy",
            "komorka",
            "podstawa_prawna",
            "waluta",
            "wlasciciel_merytoryczny",
            "opiekun_BZ",
            "dostawca",
            "koordynatorzy",
            "typ_zakresu",
            "status",
            "od_kiedy",
            "do_kiedy",
        )

        template_name = (
            "django_tables2/bootstrap.html"  # Wybierz szablon wyświetlania tabeli
        )
        per_page = 20


class EZZCFilter(django_filters.FilterSet):
    class Meta:
        model = EZZC
        fields = {
            "sygnatura": ["icontains"],
            "przedmiot": ["icontains"],
            "przedmiot": ["icontains"],
            "komorka": ["icontains"],
            "dostawca": ["icontains"],
            "status": ["icontains"],
            "od_kiedy": ["year"],
        }  # Filtruj po zawieraniu


class FilteredEZZCListView(LoginRequiredMixin, SingleTableMixin, FilterView):
    table_class = EZZCTable
    model = EZZC
    template_name = (
        "wszystkie_umowy.html"  # Wprowadź ścieżkę do swojego własnego szablonu
    )
    filterset_class = EZZCFilter
    login_url = "/account/login/"  # URL do przekierowania, jeśli nie zalogowany

    def dispatch(self, request, *args, **kwargs):
        if not request.user.groups.filter(name="contract_editor").exists():
            return redirect(self.login_url)
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(common_context(self.request))
        return context
