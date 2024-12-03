from .common_purchase import BazaPurchaseView


class ZakupyRoboczy(BazaPurchaseView):
    template_name = "purchases_table.html"

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(status_procesu__status="roboczy")
        return queryset.filter()


class ZakupyEzz(BazaPurchaseView):
    template_name = "purchases_table.html"

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(status_procesu__status="w EZZ")
        return queryset.filter()


class ZakupyZakupy(BazaPurchaseView):
    template_name = "purchases_table.html"

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(status_procesu__status="w zakupach")
        return queryset.filter()


class ZakupyBGNIG(BazaPurchaseView):
    template_name = "purchases_table.html"

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(status_procesu__status="zakup BGNIG")
        return queryset.filter()


class ZakupyRealizacja(BazaPurchaseView):
    template_name = "purchases_table.html"

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(status_procesu__status="w realizacji")
        return queryset.filter()
