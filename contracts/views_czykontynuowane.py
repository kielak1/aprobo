from .common_contract import BazaContractView
from django.db.models import Q


class CzyKontynuowaneUmowy(BazaContractView):
    template_name = "wszystkie_umowy.html"

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(
            (Q(obslugiwana=True)) & Q(czy_wymagana_kontynuacja__isnull=True)
        )
