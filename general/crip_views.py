from django.shortcuts import redirect
from general.models import Crip
from django_filters.views import FilterView
from django_tables2.views import SingleTableMixin
import django_filters
import django_tables2 as tables
from django.utils.html import format_html
from django.contrib.auth.mixins import LoginRequiredMixin
from general.common_context import common_context
from django.db.models import Sum, Q
from general.finanse_common import BaseDateRangeFilterSet


class CripsTable(tables.Table):
    link = tables.URLColumn(verbose_name="", accessor="get_link_short", orderable=False)
    suma_budzetu = tables.Column(verbose_name="Suma budżetów", orderable=False)

    class Meta:
        model = Crip
        fields = (
            "link",
            "id",
            "crip_id",
            "nazwa_projektu",
            "jednostka",
            "sekcja",
            "suma_budzetu",
        )
        template_name = "django_tables2/bootstrap.html"
        per_page = 100

    def render_link(self, value):
        image_url = "/static/general/images/edit.jpg"
        return format_html('<img src="{}" alt="E">', image_url)

    def render_suma_budzetu(self, value, record):
        # Pobierz parametry dat z zapytania
        start_date = self.request.GET.get("start_date")
        end_date = self.request.GET.get("end_date")
        # Użyj odwrotnej relacji ManyToMany - record.needs.all()
        needs = record.needs_set.all()
        # Filtrowanie po dacie, jeśli podano
        if start_date:
            needs = needs.filter(wymagana_data_realizacji__gte=start_date)
        if end_date:
            needs = needs.filter(wymagana_data_realizacji__lte=end_date)
        suma_budzetu = sum(need.orientacynjy_budzet for need in needs)
        return format_html(f"{suma_budzetu:,.2f} ")


class CripsFilter(BaseDateRangeFilterSet):
    id = django_filters.CharFilter(lookup_expr="icontains", label="Id")
    nazwa_projektu = django_filters.CharFilter(lookup_expr="icontains", label="Temat")
    sekcja = django_filters.CharFilter(lookup_expr="icontains", label="Dział")
    jednostka = django_filters.CharFilter(lookup_expr="icontains", label="Jednostka")
    crip_id = django_filters.CharFilter(lookup_expr="icontains", label="Crip ID")

    class Meta:
        model = Crip
        fields = []


class BaseCrip(LoginRequiredMixin, SingleTableMixin, FilterView):
    table_class = CripsTable
    model = Crip
    template_name = "crip-list.html"
    filterset_class = CripsFilter
    login_url = "/account/login/"  # URL do przekierowania, jeśli nie zalogowany

    def get_table(self, **kwargs):
        table = super().get_table(**kwargs)
        table.request = self.request  # Przekazanie requestu do tabeli
        return table

    def dispatch(self, request, *args, **kwargs):
        if not request.user.groups.filter(name="accountant").exists():
            return redirect(self.login_url)
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Dodaj parametry GET do kontekstu
        context["parameters"] = self.request.GET
        context.update(common_context(self.request))
        return context


class WszystkieCripy(BaseCrip):
    def get_queryset(self):
        # Pobierz parametry dat z zapytania GET
        start_date = self.request.GET.get("start_date")
        end_date = self.request.GET.get("end_date")

        # Pobierz oryginalne zapytanie
        queryset = super().get_queryset()

        # Filtruj i agreguj budżety na podstawie relacji ManyToMany z modelem Needs
        queryset = queryset.annotate(
            suma_budzetu=Sum(
                "needs__orientacynjy_budzet",  # Odwołanie do pola "orientacynjy_budzet" w modelu Needs
                filter=(
                    (
                        Q(needs__wymagana_data_realizacji__gte=start_date)
                        if start_date
                        else Q()
                    )
                    & (
                        Q(needs__wymagana_data_realizacji__lte=end_date)
                        if end_date
                        else Q()
                    )
                ),
            )
        ).distinct()
        return queryset


class LinkedCrips(BaseCrip):
    def get_queryset(self):
        # Pobierz parametry dat z zapytania GET
        start_date = self.request.GET.get("start_date")
        end_date = self.request.GET.get("end_date")
        # Filtruj Crips, które są powiązane z Needs lub Purchases
        queryset = super().get_queryset()
        linked_crips = queryset.filter(
            Q(needs__isnull=False) | Q(purchases__isnull=False)
        ).distinct()

        # Filtruj i agreguj budżety na podstawie relacji ManyToMany z modelem Needs
        queryset = linked_crips.annotate(
            suma_budzetu=Sum(
                "needs__orientacynjy_budzet",  # Odwołanie do pola "orientacynjy_budzet" w modelu Needs
                filter=(
                    (
                        Q(needs__wymagana_data_realizacji__gte=start_date)
                        if start_date
                        else Q()
                    )
                    & (
                        Q(needs__wymagana_data_realizacji__lte=end_date)
                        if end_date
                        else Q()
                    )
                ),
            )
        ).distinct()
        return queryset


class AloneCrips(BaseCrip):
    def get_queryset(self):
        # Pobierz parametry dat z zapytania GET
        start_date = self.request.GET.get("start_date")
        end_date = self.request.GET.get("end_date")
        # Filtruj Crips, które nie są powiązane z Needs ani z Purchases
        queryset = super().get_queryset()
        alone_crips = queryset.filter(
            needs__isnull=True, purchases__isnull=True
        ).distinct()
        # Filtruj i agreguj budżety na podstawie relacji ManyToMany z modelem Needs
        queryset = alone_crips.annotate(
            suma_budzetu=Sum(
                "needs__orientacynjy_budzet",  # Odwołanie do pola "orientacynjy_budzet" w modelu Needs
                filter=(
                    (
                        Q(needs__wymagana_data_realizacji__gte=start_date)
                        if start_date
                        else Q()
                    )
                    & (
                        Q(needs__wymagana_data_realizacji__lte=end_date)
                        if end_date
                        else Q()
                    )
                ),
            )
        ).distinct()
        return queryset
