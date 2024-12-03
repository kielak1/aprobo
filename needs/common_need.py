from django.shortcuts import render, redirect
from .models import Needs
from ideas.models import Ideas
import django_filters
import django_tables2 as tables
from django.utils.html import format_html
from django_filters.views import FilterView
from django_tables2.views import SingleTableMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.safestring import mark_safe
from general.models import Clients
from general.common_context import common_context


class NeedsTable(tables.Table):
    link = tables.URLColumn(verbose_name="", accessor="get_link_short", orderable=False)
    subject = tables.Column(verbose_name="Nazwa")
    section = tables.Column(verbose_name="Dział")
    client = tables.Column(verbose_name="Klient")
    #    czy_dotyczy_architektury = tables.Column(verbose_name='Architektura' )
    powiazane = tables.Column(
        accessor="get_powiazane", verbose_name="Pomysły|Zakupy", orderable=False
    )
    orientacynjy_budzet = tables.Column(verbose_name="Orientacyjny budżet")
    osoba_prowadzaca = tables.Column(verbose_name="Osoba prowadząca")

    class Meta:
        link = tables.URLColumn(verbose_name="", accessor="get_link", orderable=False)
        model = Needs
        fields = (
            "link",
            "id",
            "status_potrzeby",
            "status_akceptacji",
            "subject",
            "data_utworzenia",
            #               'czy_dotyczy_architektury',
            "wymagana_data_realizacji",
            "orientacynjy_budzet",
            "section",
            "client",
            "osoba_prowadzaca",
            "powiazane",
        )
        template_name = "django_tables2/bootstrap.html"
        per_page = 100

    def render_link(self, value):
        image_url = "/static/general/images/edit.jpg"
        return format_html('<img src="{}" alt="E">', image_url)

    def render_powiazane(self, value, record):
        ideas = Ideas.objects.filter(needs=record).exclude(needs=None)
        # Generowanie hiperlinków dla pomyslow
        pomysly = ", ".join(
            [
                f'<a href="/ideas/wszystkiepomysly/edit_idea_short/?idea_id={idea.id}">{idea.id}</a>'
                for idea in ideas
            ]
        )
        purchase_list = record.purchases.all()
        # Generowanie hiperlinków dla zakupów
        zakupy = ", ".join(
            [
                f'<a href="/purchases/wszystkiezakupy/edit_purchase_short/?purchase_id={purchase.id}">{purchase.id}</a>'
                for purchase in purchase_list
            ]
        )
        return mark_safe(f"{pomysly} | {zakupy}")

    def render_id(self, value, record):
        return mark_safe(
            f'<a href="/needs/wszystkiepotrzeby/edit_need_short/?need_id={record.id}">{record.id}</a>'
        )


class NeedsFilter(django_filters.FilterSet):
    BOOL_CHOICES = (
        (True, "Tak"),
        (False, "Nie"),
    )

    # czy_dotyczy_architektury = django_filters.ChoiceFilter(
    #     choices=BOOL_CHOICES,
    #     label='Czy dotyczy architektury'
    # )

    subject = django_filters.CharFilter(lookup_expr="icontains", label="Nazwa")
    id = django_filters.CharFilter(lookup_expr="icontains", label="Id")
    section__short_name = django_filters.CharFilter(
        lookup_expr="icontains", label="Dział"
    )
    status_potrzeby__status = django_filters.CharFilter(
        lookup_expr="exact", label="Status potrzeby"
    )
    osoba_prowadzaca__username = django_filters.CharFilter(
        lookup_expr="icontains", label="Osoba prowadząca"
    )
    status_akceptacji__akceptacja = django_filters.CharFilter(
        lookup_expr="exact", label="Status akceptacji"
    )
    client__name = django_filters.CharFilter(lookup_expr="exact", label="Klient")

    class Meta:
        model = Needs

        fields = [
            "subject",
            "id",
            "section__short_name",
            "osoba_prowadzaca__username",
            "status_potrzeby__status",  #                 'czy_dotyczy_architektury',\
            "status_akceptacji__akceptacja",
        ]


class BazaNeedView(LoginRequiredMixin, SingleTableMixin, FilterView):
    table_class = NeedsTable
    model = Needs
    filterset_class = NeedsFilter
    login_url = "/account/login/"  # URL do przekierowania, jeśli nie zalogowany

    def dispatch(self, request, *args, **kwargs):
        if not request.user.groups.filter(name="need_viewer").exists():
            return redirect(self.login_url)
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Dodaj parametry GET do kontekstu
        context["parameters"] = self.request.GET
        context["klienci"] = Clients.objects.all()  # Pobierz wszystkich klientów
        context.update(common_context(self.request))
        return context
