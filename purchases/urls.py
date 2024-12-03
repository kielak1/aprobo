from django.urls import path
from . import views

from .views_import_postepowan import import_postepowan
from .views_crip_import import crip_import
from .views_postepowania import FilteredPostepowaniaListView
from purchases.views_zakupy_do_akceptacji import ZakupyDoAkceptacji
from purchases.views_wszystkiezakupy import WszystkieZakupy
from .views_edit_purchase import edit_purchase_short
from contracts.views_edit_contract import edit_contract_short
from needs.views_edit_need import edit_need_short
from .views import EZZListView, EZZListIllegalView
from ideas.views_edit_idea import edit_idea_short
from .views_zakupy_fazy import (
    ZakupyRoboczy,
    ZakupyEzz,
    ZakupyZakupy,
    ZakupyBGNIG,
    ZakupyRealizacja,
)
from .views_ezz import unlinked_ezz

urlpatterns = [
    path("edit_purchase_short/", edit_purchase_short, name="edit_purchase_short"),
    path("edit_contract_short/", edit_contract_short, name="edit_contract_short"),
    path("edit_need_short/", edit_need_short, name="edit_need_short"),
    path("edit_idea_short/", edit_idea_short, name="edit_idea_short"),
    path("", views.index, name="index_purchases"),
    path(
        "zakupydoakceptacji/edit_purchase_short/",
        edit_purchase_short,
        name="edit_purchase_short",
    ),
    path(
        "wszystkiezakupy/edit_purchase_short/",
        edit_purchase_short,
        name="edit_purchase_short",
    ),
    path(
        "zakupy_roboczy/edit_purchase_short/",
        edit_purchase_short,
        name="edit_purchase_short",
    ),
    path(
        "zakupy_ezz/edit_purchase_short/",
        edit_purchase_short,
        name="edit_purchase_short",
    ),
    path(
        "zakupy_zakupy/edit_purchase_short/",
        edit_purchase_short,
        name="edit_purchase_short",
    ),
    path(
        "zakupy_bgnig/edit_purchase_short/",
        edit_purchase_short,
        name="edit_purchase_short",
    ),
    path(
        "zakupy_realizacja/edit_purchase_short/",
        edit_purchase_short,
        name="edit_purchase_short",
    ),
    path(
        "wszystkiezakupy/",
        WszystkieZakupy.as_view(),
        name="purchases-list-wszystkiezakupy",
    ),
    path(
        "zakupydoakceptacji/",
        ZakupyDoAkceptacji.as_view(),
        name="purchases-list-zakupydoakceptacji",
    ),
    path("ezz/import", views.ezz_import, name="ezz_import"),
    path("ezz/import_postepowan", import_postepowan, name="import_postepowan"),
    path("ezz/", EZZListView.as_view(), name="ezz"),
    path("ezz-illegal/", EZZListIllegalView.as_view(), name="ezz"),
    path("postepowania_list/", FilteredPostepowaniaListView.as_view(), name="cbu-list"),
    path("crip_import/", crip_import, name="crip_import"),
    path("zakupy_roboczy/", ZakupyRoboczy.as_view(), name="zakupy_roboczy"),
    path("zakupy_ezz/", ZakupyEzz.as_view(), name="zakupy_ezz"),
    path("zakupy_zakupy/", ZakupyZakupy.as_view(), name="zakupy_zakupy"),
    path("zakupy_bgnig/", ZakupyBGNIG.as_view(), name="zakupy_bgnig"),
    path("zakupy_realizacja/", ZakupyRealizacja.as_view(), name="zakupy_realizacja"),
]


urlpatterns += [
    path("unlinked_ezz/", unlinked_ezz, name="unlinked_ezz_list"),
]

from general.raporty_zakupowe import (
    export_planowane_zakupy_to_excel,
    export_trwajace_zakupy_to_excel,
)

urlpatterns += [
    path("planowane/", export_planowane_zakupy_to_excel, name="planowane_zakupy"),
    path("trwajace/", export_trwajace_zakupy_to_excel, name="trwajace_zakupy"),
]
