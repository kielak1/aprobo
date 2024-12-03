from .common_contract import BazaContractView
from django.db.models import Q


class NieprzypisaneUmowy(BazaContractView):
    template_name = "wszystkie_umowy.html"

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(
            (Q(obslugiwana__isnull=True) | Q(obslugiwana=True))
            & Q(section__isnull=True)
        )
