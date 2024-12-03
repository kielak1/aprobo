from .common_contract import BazaContractView
from django.db.models import Q


class CzyObslugiwaneUmowy(BazaContractView):
    template_name = "wszystkie_umowy.html"

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter((Q(obslugiwana__isnull=True)) & Q(section__isnull=False))
