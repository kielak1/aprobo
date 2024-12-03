from django.shortcuts import render, redirect
from .models import CBU
from django_filters.views import FilterView
from django_tables2.views import SingleTableMixin
import django_filters
import django_tables2 as tables
from django.contrib.auth.mixins import LoginRequiredMixin
from general.common_context import common_context


class CBUTable(tables.Table):
    class Meta:
        model = CBU
        fields = (
            "sygnatura",
            "data_zawarcia",
            "data_zakonczenia",
            "status",
            "nazwa_kontrahenta",
            "osoba_prowadzaca",
            "wartosc_wydatkowa",
            "wartosc_wplywowa",
            "wartosc_odbiorow_wydatkowych",
            "wartosc_odbiorow_wplywowych",
            "temat",
            "idemand",
            "mandant",
        )

        template_name = (
            "django_tables2/bootstrap.html"  # Wybierz szablon wyświetlania tabeli
        )
        per_page = 50


class CBUFilter(django_filters.FilterSet):
    class Meta:
        model = CBU
        fields = {
            "sygnatura": ["icontains"],
            "data_zawarcia": ["year"],
            "status": ["icontains"],
            "osoba_prowadzaca": ["icontains"],
            "temat": ["icontains"],
        }  # Filtruj po zawieraniu


class FilteredCBUListView(LoginRequiredMixin, SingleTableMixin, FilterView):
    table_class = CBUTable
    model = CBU
    template_name = (
        "wszystkie_umowy.html"  # Wprowadź ścieżkę do swojego własnego szablonu
    )
    filterset_class = CBUFilter
    login_url = "/account/login/"  # URL do przekierowania, jeśli nie zalogowany

    def dispatch(self, request, *args, **kwargs):
        if not request.user.groups.filter(name="contract_editor").exists():
            return redirect(self.login_url)
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(common_context(self.request))
        return context
