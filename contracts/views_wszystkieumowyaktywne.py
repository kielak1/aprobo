from .common_contract import BazaContractView
from .models import Contracts
import django_tables2 as tables
from django.utils.html import format_html
from django.db.models import Q


class ContractsShortTable(tables.Table):
    link = tables.URLColumn(verbose_name="", accessor="get_link_short", orderable=False)
    # liczba_aneksow = tables.Column(verbose_name='A', orderable=False)
    id = tables.Column(orderable=False)
    section = tables.Column(orderable=False)
    numer_umowy = tables.Column(orderable=False)
    data_zawarcia = tables.Column(orderable=False)
    subject = tables.Column(orderable=False)
    kontrahent = tables.Column(orderable=False)
    wartosc = tables.Column(orderable=False)
    waluta = tables.Column(orderable=False)
    czy_wymagana_kontynuacja = tables.Column(orderable=False)
    wymagana_data_zawarcia_kolejnej_umowy = tables.Column(orderable=False)
    przedmiot_kolejnej_umowy = tables.Column(orderable=False)

    class Meta:
        model = Contracts
        fields = (
            "link",
            "id",
            "section",
            "numer_umowy",
            "data_zawarcia",
            "subject",
            "kontrahent",
            "wartosc",
            "waluta",
            "czy_wymagana_kontynuacja",
            "wymagana_data_zawarcia_kolejnej_umowy",
            "przedmiot_kolejnej_umowy",
        )
        template_name = "django_tables2/bootstrap.html"
        per_page = 10

    def render_link(self, value):
        image_url = "/static/general/images/edit.jpg"
        return format_html('<img src="{}" alt="E">', image_url)


class WszystkieUmowyAktywne(BazaContractView):
    template_name = "wszystkie_umowy.html"

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter((Q(obslugiwana=True)))
