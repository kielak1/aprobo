from django.shortcuts import render
from .models import Needs, StatusNeed
import django_tables2 as tables
from django.utils.html import format_html
from .common_need import BazaNeedView
from general.models import Status_akceptacji, Status_procesu
from purchases.models import Purchases
from django.db.models import Exists, OuterRef


class NeedsShortTable(tables.Table):
    link = tables.URLColumn(verbose_name="", accessor="get_link_short", orderable=False)
    id = tables.Column(orderable=False)
    subject = tables.Column(verbose_name="Nazwa", orderable=False)
    data_utworzenia = tables.Column(orderable=False)
    komentarz = tables.Column(orderable=False)
    wymagana_data_realizacji = tables.Column(orderable=False)
    orientacynjy_budzet = tables.Column(orderable=False)
    section = tables.Column(verbose_name="Dział", orderable=False)
    client = tables.Column(verbose_name="Klient", orderable=False)
    osoba_prowadzaca = tables.Column(orderable=False)
    osoba_kontakowa_u_klienta = tables.Column(orderable=False)

    class Meta:
        link = tables.URLColumn(verbose_name="", accessor="get_link", orderable=False)
        model = Needs
        fields = (
            "link",
            "id",
            "subject",
            "data_utworzenia",
            "komentarz",
            "wymagana_data_realizacji",
            "orientacynjy_budzet",
            "section",
            "client",
            "osoba_prowadzaca",
            "osoba_kontakowa_u_klienta",
        )
        template_name = "django_tables2/bootstrap.html"
        per_page = 10

    def render_link(self, value):
        image_url = "/static/general/images/edit.jpg"
        return format_html('<img src="{}" alt="E">', image_url)


class WszystkiePotrzeby(BazaNeedView):
    template_name = "needs_table.html"

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.order_by("-id")


# class PotrzebyBezZakupow(BazaNeedView):
#     template_name = "needs_table.html"

#     def get_queryset(self):
#         queryset = super().get_queryset()
#         return queryset


class PotrzebyBezZakupow(BazaNeedView):
    template_name = "needs_table.html"

    def get_queryset(self):
        # Pobierz domyślny queryset
        queryset = super().get_queryset()
        zaakceptowane_status = Status_akceptacji.objects.get(
            akceptacja="zaakceptowane"
        ).id

        queryset = queryset.filter(status_akceptacji=zaakceptowane_status).exclude(
            purchases__isnull=False  # Wyklucz rekordy, które mają powiązane zakupy
        )

        return queryset


class PotrzebyDoZamkniecia(BazaNeedView):
    template_name = "needs_table.html"

    def get_queryset(self):
        # Pobierz domyślny queryset
        queryset = super().get_queryset()
        zaakceptowane_status = Status_akceptacji.objects.get(
            akceptacja="zaakceptowane"
        ).id
        zakonczony_status = Status_procesu.objects.get(status="zakończony").id
        anulowany_status = Status_procesu.objects.get(status="anulowany").id
        zamknieta_status = StatusNeed.objects.get(status="zamknięta").id
        zrealizowana_status = StatusNeed.objects.get(status="zrealizowana").id

        # Zidentyfikuj potrzeby, które mają powiązane zakupy z innym statusem niż "zakończony" lub "anulowany"
        subquery = Purchases.objects.filter(need_id=OuterRef("pk")).exclude(
            status_procesu__in=[zakonczony_status, anulowany_status]
        )

        # Filtruj potrzeby, które mają status zaakceptowane, które mają powiązane zakupy i które nie są zamknięte ani zrealizowane
        queryset = (
            queryset.filter(
                status_akceptacji=zaakceptowane_status, purchases__isnull=False
            )
            .exclude(status_potrzeby__in=[zamknieta_status, zrealizowana_status])
            .annotate(has_other_status=Exists(subquery))
            .filter(has_other_status=False)
        )

        return queryset
