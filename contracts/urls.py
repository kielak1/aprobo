from django.urls import path
from . import views
from .views_import_CBU import (
    cbu_import,
)
from .views_import_EZZC import (
    ezzc_import,
)
from .views_edit_contract import edit_contract_short
from .views_auto_contract import auto_contract
from .views_nieprzypisane import NieprzypisaneUmowy
from .views_czyobslugiwane import CzyObslugiwaneUmowy
from .views_czykontynuowane import CzyKontynuowaneUmowy
from .views_kiedykontynuowane import KiedyKontynuowaneUmowy
from .views_jakontynuowane import JakKontynuowaneUmowy
from .views_wszystkieumowy import WszystkieUmowy
from .views_wszystkieumowyaktywne import WszystkieUmowyAktywne
from .views_ostatniozmieniane import OstatnioZmienianeUmowy
from .views_CBU import FilteredCBUListView
from .views_EZZC import FilteredEZZCListView
from purchases.views_edit_purchase import edit_purchase_short
from needs.views_edit_need import edit_need_short
from ideas.views_edit_idea import edit_idea_short

urlpatterns = [
    path("edit_purchase_short/", edit_purchase_short, name="edit_purchase_short"),
    path("edit_contract_short/", edit_contract_short, name="edit_contract_short"),
    path("edit_need_short/", edit_need_short, name="edit_need_short"),
    path("edit_idea_short/", edit_idea_short, name="edit_idea_short"),
    path("", views.index, name="index_contracts"),
    path("cbu_import/", cbu_import, name="cbu_import"),
    path("ezzc_import/", ezzc_import, name="ezzc_import"),
    path(
        "wszystkieumowyaktywne/edit_contract_short/",
        edit_contract_short,
        name="edit_contract_short",
    ),
    path(
        "wszystkieumowyaktywne/",
        WszystkieUmowyAktywne.as_view(),
        name="contracts-list-wszystkieumowyaktywne",
    ),
    path(
        "wszystkieumowy/edit_contract_short/",
        edit_contract_short,
        name="edit_contract_short",
    ),
    path(
        "wszystkieumowy/",
        WszystkieUmowy.as_view(),
        name="contracts-list-wszystkieumowy",
    ),
    path(
        "nieprzypisane/edit_contract_short/",
        edit_contract_short,
        name="edit_contract_short",
    ),
    path(
        "nieprzypisane/",
        NieprzypisaneUmowy.as_view(),
        name="contracts-list-nieprzypisane",
    ),
    path(
        "czyobslugiwane/edit_contract_short/",
        edit_contract_short,
        name="edit_contract_short",
    ),
    path(
        "czyobslugiwane/",
        CzyObslugiwaneUmowy.as_view(),
        name="contracts-list-czyobslugiwane",
    ),
    path(
        "czykontynuowac/edit_contract_short/",
        edit_contract_short,
        name="edit_contract_short",
    ),
    path(
        "czykontynuowac/",
        CzyKontynuowaneUmowy.as_view(),
        name="contracts-list-czykontynuowane",
    ),
    path(
        "kiedykontynuowac/edit_contract_short/",
        edit_contract_short,
        name="edit_contract_short",
    ),
    path(
        "kiedykontynuowac/",
        KiedyKontynuowaneUmowy.as_view(),
        name="contracts-list-kiedykontynuowane",
    ),
    path(
        "jakkontynuowac/edit_contract_short/",
        edit_contract_short,
        name="edit_contract_short",
    ),
    path(
        "jakkontynuowac/",
        JakKontynuowaneUmowy.as_view(),
        name="contracts-list-jakkontynuowane",
    ),
    path("cbu_list/", FilteredCBUListView.as_view(), name="cbu-list"),
    path("ezzc_list/", FilteredEZZCListView.as_view(), name="ezzc-list"),
    path("ezzc_add/", views.ezzc_add, name="ezzc_add"),
    path("auto_contract/", auto_contract, name="auto_contract"),
    path(
        "ostatniozmieniane/edit_contract_short/",
        edit_contract_short,
        name="edit_contract_short",
    ),
    path(
        "ostatniozmieniane/",
        OstatnioZmienianeUmowy.as_view(),
        name="contracts-list-ostatniozmieniane",
    ),
]
