from django.shortcuts import redirect
from general.models import Meeting
from django_filters.views import FilterView
from django_tables2.views import SingleTableMixin
import django_filters
import django_tables2 as tables
from django.utils.html import format_html
from django.contrib.auth.mixins import LoginRequiredMixin
from general.common_context import common_context
from django.utils.safestring import mark_safe
import logging

logger = logging.getLogger("avantic")


class RadyTable(tables.Table):
    class Meta:
        model = Meeting
        fields = (
            "id",
            "meeting_date",
            "meeting_status",
        )
        template_name = "django_tables2/bootstrap.html"
        per_page = 100

    def render_id(self, record):
        return mark_safe(f'<a href="/general/edit_rada/{record.id}">{record.id}</a>')


class RadyFilter(django_filters.FilterSet):
    id = django_filters.CharFilter(lookup_expr="icontains", label="Id")
    meeting_date = django_filters.CharFilter(
        lookup_expr="icontains", label="meeting_date"
    )

    class Meta:
        model = Meeting
        fields = {}


class WszystkieRady(LoginRequiredMixin, SingleTableMixin, FilterView):
    table_class = RadyTable
    model = Meeting
    template_name = "rady-list.html"
    filterset_class = RadyFilter
    login_url = "/account/login/"  # URL do przekierowania, jeśli nie zalogowany

    def dispatch(self, request, *args, **kwargs):
        context = common_context(self.request)
        rada_viewer = context["rada_viewer"]
        # Sprawdź uprawnienia na podstawie zmiennej 'rada_viewer'
        if not rada_viewer:
            return redirect(self.login_url)
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.order_by("-meeting_date")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Dodaj parametry GET do kontekstu
        context["parameters"] = self.request.GET
        context.update(common_context(self.request))
        return context
