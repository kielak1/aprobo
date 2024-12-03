from .models import Ideas
from django_filters.views import FilterView
from django_tables2.views import SingleTableMixin
import django_filters
import django_tables2 as tables
from django.utils.html import format_html
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from purchases.models import Purchases
import logging
from general.linki import generate_purchase_url, generate_need_url
from general.models import Clients
from django.db.models import Q
from django.utils.safestring import mark_safe
from general.common_context import common_context
logger = logging.getLogger("avantic")

class IdeasTable(tables.Table):
    link = tables.URLColumn(verbose_name="", accessor="get_link_short", orderable=False)
    status_idei = tables.Column(verbose_name="Status pomysłu")
    subject = tables.Column(verbose_name="Nazwa")
    section = tables.Column(verbose_name="Dział")
    client = tables.Column(verbose_name="Klient")
    wymagana_data_realizacji = tables.Column(verbose_name="Data realizacji")
    section = tables.Column(verbose_name="Dział")
    #    czy_dotyczy_architektury = tables.Column(verbose_name='Architektura')
    powiazane = tables.Column(
        accessor="get_powiazane", verbose_name="Potrzeby|Zakupy", orderable=False
    )
    orientacynjy_budzet = tables.Column(verbose_name="Orientacyjny budżet")

    class Meta:
        model = Ideas
        fields = (
            "link",
            "id",
            "status_idei",
            "status_akceptacji",
            #        'czy_dotyczy_architektury',
            "subject",
            "data_utworzenia",
            "wymagana_data_realizacji",
            "orientacynjy_budzet",
            "section",
            "client",
            "osoba_prowadzaca",
            "powiazane",
        )
        per_page = 100

    def render_link(self, value):
        image_url = "/static/general/images/edit.jpg"
        return format_html('<img src="{}" alt="E">', image_url)

    def render_powiazane(self, record):
        is_client = self.context.get("is_client", False) if self.context else False
        # Pobieranie powiązanych potrzeb
        needs = record.needs.filter(~Q(status_potrzeby__status="zamknięta"))
        if is_client:
            potrzeby = ", ".join(
                [
                    f'{need.id}'
                    for need in needs
                ]
            )
        else:
            # Generowanie hiperlinków dla potrzeb
            potrzeby = ", ".join(
                [
                    f'<a href="/needs/wszystkiepotrzeby/edit_need_short/?need_id={need.id}">{need.id}</a>'
                    for need in needs
                ]
            )
         # Pobieranie powiązanych zakupów
        purchase_list = Purchases.objects.filter(need__in=needs)

        if is_client:
            # Generowanie hiperlinków dla zakupów
            zakupy = ", ".join(
                [
                    f'{purchase.id}'
                    for purchase in purchase_list
                ]
            )
        else:
            # Generowanie hiperlinków dla zakupów
            zakupy = ", ".join(
                [
                    f'<a href="/purchases/wszystkiezakupy/edit_purchase_short/?purchase_id={purchase.id}">{purchase.id}</a>'
                    for purchase in purchase_list
                ]
            )
        # Zwracanie bezpiecznego HTML-a z linkami do potrzeb i zakupów
        return mark_safe(f"{potrzeby} | {zakupy}")

    def render_id(self, record):
        return mark_safe(
            f'<a href="/ideas/wszystkiepomysly/edit_idea_short/?idea_id={record.id}">{record.id}</a>'
        )


class IdeasFilter(django_filters.FilterSet):
    BOOL_CHOICES = (
        (True, "Tak"),
        (False, "Nie"),
    )

    id = django_filters.CharFilter(lookup_expr="icontains", label="Id")
    subject = django_filters.CharFilter(lookup_expr="icontains", label="Temat")
    section__short_name = django_filters.CharFilter(
        lookup_expr="icontains", label="Dział"
    )
    osoba_prowadzaca__username = django_filters.CharFilter(
        lookup_expr="icontains", label="Osoba prowadząca"
    )
    status_idei__status = django_filters.CharFilter(
        lookup_expr="exact", label="Status pomysłu"
    )
    status_akceptacji__akceptacja = django_filters.CharFilter(
        lookup_expr="exact", label="Status akceptacji"
    )
    client__name = django_filters.CharFilter(lookup_expr="exact", label="Klient")

    class Meta:
        model = Ideas
        fields = {}


class BazaIdeaView(LoginRequiredMixin, SingleTableMixin, FilterView):
    table_class = IdeasTable
    model = Ideas
    filterset_class = IdeasFilter
    login_url = "/account/login/"  # URL do przekierowania, jeśli nie zalogowany

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Dodaj parametry GET do kontekstu
        context["parameters"] = self.request.GET
        context["klienci"] = Clients.objects.all()  # Pobierz wszystkich klientów
        context.update(common_context(self.request))
        return context

    def get_table(self, **kwargs):
        table = super().get_table(**kwargs)
        # Przekazuj tylko niezbędne dane do tabeli
        table.context = {
            "is_client": self.request.user.groups.filter(name="client").exists()
        }
        return table

