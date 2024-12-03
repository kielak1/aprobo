from django.shortcuts import render, redirect
from .models import Purchases
from ideas.models import Ideas
from needs.models import Needs

from django_filters.views import FilterView
from django_tables2.views import SingleTableMixin
import django_filters
import django_tables2 as tables
from django.utils.html import format_html
from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.safestring import mark_safe
from general.models import Clients
from general.common_context import common_context


class PurchasesTable(tables.Table):
    link = tables.URLColumn(verbose_name="", accessor="get_link_short", orderable=False)
    powiazane = tables.Column(
        accessor="get_powiazane", verbose_name="Pomysły|Potrzeby", orderable=False
    )
    pilnosc = tables.Column(verbose_name="Pilność")
    budzet_capex_netto = tables.Column(verbose_name="Capex netto")
    budzet_opex_netto = tables.Column(verbose_name="Opex netto")
    osoba_prowadzaca = tables.Column(verbose_name="Osoba prowadząca")
    section = tables.Column(verbose_name="Dział")

    class Meta:
        link = tables.URLColumn(verbose_name="", accessor="get_link", orderable=False)
        model = Purchases
        fields = (
            "link",
            "id",
            "przedmiot_zakupu",
            "ezz",
            "status_procesu",
            #         'status_akceptacji',
            "pilnosc",
            "budzet_capex_netto",
            "budzet_opex_netto",
            "waluta",
            "osoba_prowadzaca",
            "section",
            "client",
            "powiazane",
        )
        template_name = "django_tables2/bootstrap.html"
        per_page = 100

    def render_link(self, value):
        image_url = "/static/general/images/edit.jpg"
        return format_html('<img src="{}" alt="E">', image_url)

    def render_powiazane(self, value, record):
        need_instance = record.need
        if need_instance is None:
            return "---"

        needs = [need_instance]

        ideas = Ideas.objects.filter(needs=need_instance).distinct()

        #      return "----"
        potrzeby = ", ".join(
            [
                f'<a href="/needs/wszystkiepotrzeby/edit_need_short/?need_id={need.id}">{need.id}</a>'
                for need in needs
            ]
        )
        pomysly = ", ".join(
            [
                f'<a href="/ideas/wszystkiepomysly/edit_idea_short/?idea_id={idea.id}">{idea.id}</a>'
                for idea in ideas
            ]
        )

        return mark_safe(f"{pomysly} | {potrzeby}")

    def render_id(self, value, record):
        return mark_safe(
            f'<a href="/purchases/wszystkiezakupy/edit_purchase_short/?purchase_id={record.id}">{record.id}</a>'
        )


class PurchasesFilter(django_filters.FilterSet):
    BOOL_CHOICES = (
        (True, "Tak"),
        (False, "Nie"),
    )

    id = django_filters.CharFilter(lookup_expr="icontains", label="Id")
    przedmiot_zakupu = django_filters.CharFilter(lookup_expr="icontains", label="Temat")
    section__short_name = django_filters.CharFilter(
        lookup_expr="icontains", label="Dział"
    )
    osoba_prowadzaca__username = django_filters.CharFilter(
        lookup_expr="icontains", label="Osoba prowadząca"
    )
    status_procesu__status = django_filters.CharFilter(
        lookup_expr="exact", label="Status zakupu"
    )
    #   status_akceptacji__akceptacja = django_filters.CharFilter(lookup_expr='exact', label='Status akceptacji')
    pilnosc__pilnosc = django_filters.CharFilter(
        lookup_expr="icontains", label="Pilność"
    )
    client__name = django_filters.CharFilter(lookup_expr="exact", label="Klient")

    class Meta:
        model = Purchases
        fields = {}


class BazaPurchaseView(LoginRequiredMixin, SingleTableMixin, FilterView):
    table_class = PurchasesTable
    model = Purchases
    filterset_class = PurchasesFilter
    login_url = "/account/login/"  # URL do przekierowania, jeśli nie zalogowany

    def dispatch(self, request, *args, **kwargs):
        if not request.user.groups.filter(name="purchase_viewer").exists():
            return redirect(self.login_url)

        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Dodaj parametry GET do kontekstu
        context["parameters"] = self.request.GET
        context["klienci"] = Clients.objects.all()  # Pobierz wszystkich klientów
        context.update(common_context(self.request))
        return context
