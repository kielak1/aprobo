from django.shortcuts import render
from .models import Purchases
from django_filters.views import FilterView
from django_tables2.views import SingleTableMixin
import django_filters
import django_tables2 as tables
from django.utils.html import format_html


class PurchasesTable(tables.Table):
    link = tables.URLColumn(verbose_name="", accessor="get_link", orderable=False)
    status_procesu = tables.Column(
        attrs={"td": {"style": "width: 1%;"}}, verbose_name="Status"
    )
    przedmiot_zakupu = tables.Column(
        attrs={"td": {"style": "width: 10%;"}}, verbose_name="Przedmiot"
    )
    uzasadnienie_zakupu = tables.Column(
        attrs={"td": {"style": "width: 10%;"}}, verbose_name="Uzasadnienie"
    )
    zakres_zakupu = tables.Column(
        attrs={"td": {"style": "width: 10%;"}}, verbose_name="Zakres"
    )
    cel_i_produkty = tables.Column(
        attrs={"td": {"style": "width: 10%;"}}, verbose_name="Cel i produkty"
    )
    section = tables.Column(attrs={"td": {"style": "width: 1%;"}}, verbose_name="dz")

    class Meta:
        model = Purchases
        fields = (
            "link",
            "status_procesu",
            "przedmiot_zakupu",
            "uzasadnienie_zakupu",
            "zakres_zakupu",
            "cel_i_produkty",
            "ezz",
            "section",
            "client",
            "status_akceptacji",
            "pilnosc",
            "odtworzeniowy",
            "rozwojowy",
            "planowany_termin_platnosci",
            "waluta",
            "id_sap",
            "budzet_capex_netto",
            "budzet_opex_netto",
            "crip_id",
            "sposob_wyceny",
            "zgodnosc_mapy",
            "dostawca",
            "sposob_zakupu",
        )
        template_name = "django_tables2/bootstrap.html"
        per_page = 100
        attrs = {
            "class": "table table-striped table-hover",
            "style": "width: 4000px;",  # Szerokość tabeli wynosi 3000 pikseli
        }

    def render_link(self, value):
        image_url = "/static/purchases/images/edit.jpg"
        return format_html('<img src="{}" alt="E">', image_url)

    # def get_table_data(self):
    #     queryset = super().get_table_data()
    #     # Wyklucz rekordy spełniające określony warunek
    #     queryset = queryset.exclude(dostawca !='anulowany')
    #     return queryset


class PurchasesFilter(django_filters.FilterSet):
    class Meta:
        model = Purchases
        fields = {
            "przedmiot_zakupu": ["icontains"],
            "section__short_name": ["icontains"],
            "ezz__EZZ_number": ["icontains"],
            "client__short_name": ["icontains"],
        }

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     self.filters['dostawca'].field.widget.attrs['value'] = 'anulowany'


class FilteredPurchasesListView(SingleTableMixin, FilterView):
    table_class = PurchasesTable
    model = Purchases
    template_name = "purchases/index.html"
    filterset_class = PurchasesFilter
