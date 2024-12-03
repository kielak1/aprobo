from .models import Ideas
import django_tables2 as tables
from django.utils.html import format_html
from .common_idea import BazaIdeaView
from general.models import Clients
from django.shortcuts import redirect
import logging

logger = logging.getLogger("avantic")


class IdeasShortTable(tables.Table):
    link = tables.URLColumn(verbose_name="", accessor="get_link_short", orderable=False)
    id = tables.Column(orderable=False)
    status_idei = tables.Column(verbose_name="Status pomysłu", orderable=False)
    status_akceptacji = tables.Column(orderable=False)
    subject = tables.Column(verbose_name="Nazwa", orderable=False)
    data_utworzenia = tables.Column(orderable=False)
    orientacynjy_budzet = tables.Column(orderable=False)
    section = tables.Column(verbose_name="Dział", orderable=False)
    client = tables.Column(verbose_name="Klient", orderable=False)
    osoba_prowadzaca = tables.Column(orderable=False)

    class Meta:
        link = tables.URLColumn(verbose_name="", accessor="get_link", orderable=False)
        model = Ideas
        fields = (
            "link",
            "id",
            "status_idei",
            "status_akceptacji",
            "subject",
            "data_utworzenia",
            "orientacynjy_budzet",
            "section",
            "client",
            "osoba_prowadzaca",
        )
        template_name = "django_tables2/bootstrap.html"
        per_page = 6

    def render_link(self, value):
        image_url = "/static/general/images/edit.jpg"
        return format_html('<img src="{}" alt="E">', image_url)


class WszystkiePomysly(BazaIdeaView):
    template_name = "ideas_table.html"

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.prefetch_related("needs", "needs__purchases")
        return queryset.order_by("-id")

    def dispatch(self, request, *args, **kwargs):
        if not request.user.groups.filter(name="idea_viewer").exists():
            return redirect(self.login_url)
        return super().dispatch(request, *args, **kwargs)


class PomyslyKlienta(BazaIdeaView):
    template_name = "ideas_table.html"

    def get_queryset(self):
        current_user = self.request.user
        clients = Clients.objects.filter(users=current_user)
        queryset = super().get_queryset()
        return queryset.filter(client__in=clients).order_by("-id")

    def dispatch(self, request, *args, **kwargs):
        if not request.user.groups.filter(name="client").exists():
            return redirect(self.login_url)
        return super().dispatch(request, *args, **kwargs)
