from .common_purchase import BazaPurchaseView
from .models import Purchases
import django_tables2 as tables
from django.utils.html import format_html


class PurchasesShortTable(tables.Table):
    link = tables.URLColumn(verbose_name="", accessor="get_link_short", orderable=False)
    id = tables.Column(orderable=False)
    osoba_prowadzaca = tables.Column(orderable=False)
    przedmiot_zakupu = tables.Column(orderable=False)
    ezz = tables.Column(orderable=False)
    section = tables.Column(orderable=False)
    client = tables.Column(orderable=False)
    status_procesu = tables.Column(orderable=False)
    #   status_akceptacji =  tables.Column(  orderable=False)
    waluta = tables.Column(orderable=False)
    budzet_capex_netto = tables.Column(orderable=False)
    budzet_opex_netto = tables.Column(orderable=False)

    class Meta:
        link = tables.URLColumn(verbose_name="", accessor="get_link", orderable=False)
        model = Purchases
        fields = (
            "link",
            "id",
            "osoba_prowadzaca",
            "przedmiot_zakupu",
            "ezz",
            "section",
            "client",
            "status_procesu",
            #   'status_akceptacji',
            "waluta",
            "budzet_capex_netto",
            "budzet_opex_netto",
        )
        template_name = "django_tables2/bootstrap.html"
        per_page = 10

    def render_link(self, value):
        image_url = "/static/general/images/edit.jpg"
        return format_html('<img src="{}" alt="E">', image_url)


class WszystkieZakupy(BazaPurchaseView):
    template_name = "purchases_table.html"

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter().order_by("-id")
