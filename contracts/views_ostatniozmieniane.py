from .models import Contracts
from .common_contract import BazaContractView
from django.db.models import Max


class OstatnioZmienianeUmowy(BazaContractView):
    template_name = "wszystkie_umowy.html"

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.annotate(latest_log_date=Max("log__data")).filter(
            latest_log_date__isnull=False
        )
        queryset = queryset.order_by("-latest_log_date")
        return queryset[:20]
