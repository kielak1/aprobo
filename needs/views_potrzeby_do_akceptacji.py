from .common_need import BazaNeedView
from django.db.models import Q


class PotrzebyDoAkceptacji(BazaNeedView):
    template_name = "needs_table.html"

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(
            Q(status_akceptacji__akceptacja="do akceptacji")
            & Q(status_potrzeby__status="realizowana")
        )
        return queryset.filter()


class PotrzebyDoAkceptacjiInfra(BazaNeedView):
    template_name = "needs_table.html"

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(
            Q(status_akceptacji_infrastruktury__akceptacja="do akceptacji")
            & Q(status_potrzeby__status="realizowana")
        )
        return queryset.filter()


class PotrzebyDoAkceptacjiUslugi(BazaNeedView):
    template_name = "needs_table.html"

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(
            Q(status_akceptacji_uslug__akceptacja="do akceptacji")
            & Q(status_potrzeby__status="realizowana")
        )
        return queryset


class PotrzebyDoAkceptacjiSiec(BazaNeedView):
    template_name = "needs_table.html"

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(
            Q(status_akceptacji_sieci__akceptacja="do akceptacji")
            & Q(status_potrzeby__status="realizowana")
        )
        return queryset.filter()


class PotrzebyDoAkceptacjiFinanse(BazaNeedView):
    template_name = "needs_table.html"

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(
            Q(status_akceptacji_finansow__akceptacja="do akceptacji")
            & Q(status_potrzeby__status="realizowana")
        )
        return queryset.filter()


class PotrzebyDoAkceptacjiOpoznione(BazaNeedView):
    template_name = "needs_table.html"

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(
            Q(status_akceptacji__akceptacja="zaakceptowane")
            & (
                Q(status_akceptacji_uslug__akceptacja="do akceptacji")
                | Q(status_akceptacji_sieci__akceptacja="do akceptacji")
                | Q(status_akceptacji_infrastruktury__akceptacja="do akceptacji")
                | Q(status_akceptacji_finansow__akceptacja="do akceptacji")
            )
        )
        return queryset.filter()
