from django.shortcuts import render, redirect

from django_filters.views import FilterView
from django_tables2.views import SingleTableMixin
import django_filters
import django_tables2 as tables
from django.contrib.auth.mixins import LoginRequiredMixin
from purchases.models import Postepowania
from general.common_context import common_context


class PostepowaniaTable(tables.Table):
    class Meta:
        model = Postepowania
        fields = (
            "numer_SRM_SAP",
            "numer_ZZ",
            "opis_zapotrzebowania",
            "priorytet",
            "status_SRM",
            "zlecajacy",
            "kupiec",
            "status_biura",
            "data_wprowadzenia",
        )

        template_name = (
            "django_tables2/bootstrap.html"  # Wybierz szablon wyświetlania tabeli
        )
        per_page = 50


class PostepowaniaFilter(django_filters.FilterSet):
    BOOL_CHOICES = (
        (True, "Tak"),
        (False, "Nie"),
    )

    id = django_filters.CharFilter(lookup_expr="icontains", label="Id")
    opis_zapotrzebowania = django_filters.CharFilter(
        lookup_expr="icontains", label="Nazwa"
    )
    numer_ZZ = django_filters.CharFilter(lookup_expr="icontains", label="numer EZZ")

    class Meta:
        model = Postepowania
        fields = {}


class FilteredPostepowaniaListView(LoginRequiredMixin, SingleTableMixin, FilterView):
    table_class = PostepowaniaTable
    model = Postepowania
    template_name = (
        "postepowania-list.html"  # Wprowadź ścieżkę do swojego własnego szablonu
    )
    filterset_class = PostepowaniaFilter
    login_url = "/account/login/"  # URL do przekierowania, jeśli nie zalogowany

    def dispatch(self, request, *args, **kwargs):
        if not request.user.groups.filter(name="purchase_viewer").exists():
            return redirect(self.login_url)
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(common_context(self.request))
        return context
