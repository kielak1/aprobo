from .common_contract import BazaContractView


class WszystkieUmowy(BazaContractView):
    template_name = "wszystkie_umowy.html"

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter().order_by("-id")
