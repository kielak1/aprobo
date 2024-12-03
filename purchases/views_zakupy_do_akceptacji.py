from .common_purchase import BazaPurchaseView


class ZakupyDoAkceptacji(BazaPurchaseView):
    template_name = "purchases_table.html"

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(status_akceptacji__akceptacja="do akceptacji")
        return queryset.filter()
