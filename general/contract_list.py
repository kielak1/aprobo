from django.views.generic import ListView
from django.db.models import F
from django.db.models.functions import Coalesce
from contracts.models import Contracts
from datetime import date
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from general.common_context import common_context


class ContractsView(LoginRequiredMixin, ListView):
    model = Contracts
    template_name = "contracts_list.html"
    login_url = "/account/login/"  # URL do przekierowania, jeśli nie zalogowany

    def dispatch(self, request, *args, **kwargs):
        context = common_context(self.request)
        is_any_viewer = context["is_any_viewer"]
        # Sprawdź uprawnienia na podstawie zmiennej 'rada_viewer'
        if not is_any_viewer:
            return redirect(self.login_url)
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        # Filtrujemy kontrakty, które wymagają kontynuacji i są obsługiwane
        # Sortowanie: najpierw te z wymagana_data_zawarcia_kolejnej_umowy jako null, potem reszta po dacie
        queryset = (
            Contracts.objects.filter(czy_wymagana_kontynuacja=True, obslugiwana=True)
            .prefetch_related("ideas__needs__purchases")
            .order_by(
                Coalesce(
                    "wymagana_data_zawarcia_kolejnej_umowy",
                    F("wymagana_data_zawarcia_kolejnej_umowy"),
                ).asc(nulls_first=True)
            )
        )

        section_name = self.request.GET.get("section__short_name")
        if section_name:
            queryset = queryset.filter(section__short_name=section_name)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        contracts = context["object_list"]
        for contract in contracts:
            if contract.wymagana_data_zawarcia_kolejnej_umowy:
                contract.days_until_due = (
                    contract.wymagana_data_zawarcia_kolejnej_umowy - date.today()
                ).days
            else:
                contract.days_until_due = None
        context["parameters"] = self.request.GET
        context.update(common_context(self.request))
        return context
