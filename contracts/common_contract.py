from django.shortcuts import render, redirect
from .models import Contracts
from django_filters.views import FilterView
from django_tables2.views import SingleTableMixin
import django_filters
import django_tables2 as tables
from django.utils.html import format_html
from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from general.common_context import common_context


class ContractsTable(tables.Table):
    link = tables.URLColumn(verbose_name="", accessor="get_link_short", orderable=False)
    liczba_aneksow = tables.Column(verbose_name="A", orderable=False)
    #  obslugiwana = tables.Column(verbose_name='Obsługiwana ?' )
    data_zawarcia = tables.Column(verbose_name="Data zawarcia")
    wartosc = tables.Column(verbose_name="Wartość")
    subject = tables.Column(verbose_name="Przedmiot umowy")
    section = tables.Column(verbose_name="Dział")

    class Meta:
        model = Contracts
        fields = (
            "link",
            "id",
            "obslugiwana",
            "section",
            "numer_umowy",
            "liczba_aneksow",
            "data_zawarcia",
            "subject",
            "kontrahent",
            #   'zakres',
            "wartosc",
            "waluta",
            "czy_wymagana_kontynuacja",
            "wymagana_data_zawarcia_kolejnej_umowy",
            "przedmiot_kolejnej_umowy",
            #    'komentarz',
        )
        template_name = "django_tables2/bootstrap.html"
        per_page = 100

    def render_link(self, value):
        image_url = "/static/general/images/edit.jpg"
        return format_html('<img src="{}" alt="E">', image_url)


class ContractsFilter(django_filters.FilterSet):
    BOOL_CHOICES = (
        (True, "Tak"),
        (False, "Nie"),
    )

    czy_wymagana_kontynuacja = django_filters.ChoiceFilter(
        choices=BOOL_CHOICES, label=""
    )

    obslugiwana = django_filters.ChoiceFilter(choices=BOOL_CHOICES, label="")

    id = django_filters.CharFilter(lookup_expr="icontains", label="Id")
    subject = django_filters.CharFilter(lookup_expr="icontains", label="Temat")
    section__short_name = django_filters.CharFilter(
        lookup_expr="icontains", label="Dział"
    )
    kontrahent = django_filters.CharFilter(lookup_expr="exact", label="Kontrahent")
    numer_umowy = django_filters.CharFilter(lookup_expr="exact", label="Numer umowy")

    class Meta:
        model = Contracts
        fields = {}


class BazaContractView(LoginRequiredMixin, SingleTableMixin, FilterView):
    table_class = ContractsTable
    model = Contracts
    filterset_class = ContractsFilter
    login_url = "/account/login/"  # URL do przekierowania, jeśli nie zalogowany

    def dispatch(self, request, *args, **kwargs):
        if not request.user.groups.filter(name="contract_viewer").exists():
            return redirect(self.login_url)
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Dodaj parametry GET do kontekstu
        context["parameters"] = self.request.GET
        context.update(common_context(self.request))
        return context
