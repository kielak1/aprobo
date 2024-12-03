from django.urls import path
from .views_wszystkiepotrzeby import (
    WszystkiePotrzeby,
    PotrzebyBezZakupow,
    PotrzebyDoZamkniecia,
)
from .views_edit_need import edit_need_short
from ideas.views_edit_idea import edit_idea_short
from purchases.views_edit_purchase import edit_purchase_short
from contracts.views_edit_contract import edit_contract_short
from . import views
from needs.views_potrzeby_do_akceptacji import (
    PotrzebyDoAkceptacji,
    PotrzebyDoAkceptacjiInfra,
    PotrzebyDoAkceptacjiUslugi,
    PotrzebyDoAkceptacjiSiec,
    PotrzebyDoAkceptacjiFinanse,
    PotrzebyDoAkceptacjiOpoznione,
)
from needs.test_need import testauto, testautodynamic

urlpatterns = [
    path(
        "potrzebydoakceptacjilate/edit_need_short/",
        edit_need_short,
        name="edit_need_short",
    ),
    path(
        "potrzebydoakceptacjilate/",
        PotrzebyDoAkceptacjiOpoznione.as_view(),
        name="need-list-potrzebydoakceptacji-late",
    ),
    path(
        "potrzebydoakceptacjiinfra/edit_need_short/",
        edit_need_short,
        name="edit_need_short",
    ),
    path(
        "potrzebydoakceptacjiinfra/",
        PotrzebyDoAkceptacjiInfra.as_view(),
        name="need-list-potrzebydoakceptacji-infra",
    ),
    path(
        "potrzebydoakceptacjiuslugi/edit_need_short/",
        edit_need_short,
        name="edit_need_short",
    ),
    path(
        "potrzebydoakceptacjiuslugi/",
        PotrzebyDoAkceptacjiUslugi.as_view(),
        name="need-list-potrzebydoakceptacji-uslugi",
    ),
    path(
        "potrzebydoakceptacjisiec/edit_need_short/",
        edit_need_short,
        name="edit_need_short",
    ),
    path(
        "potrzebydoakceptacjisiec/",
        PotrzebyDoAkceptacjiSiec.as_view(),
        name="need-list-potrzebydoakceptacji-siec",
    ),
    path(
        "potrzebydoakceptacjifinanse/edit_need_short/",
        edit_need_short,
        name="edit_need_short",
    ),
    path(
        "potrzebydoakceptacjifinanse/",
        PotrzebyDoAkceptacjiFinanse.as_view(),
        name="need-list-potrzebydoakceptacji-finanse",
    ),
    path(
        "potrzebydoakceptacji/edit_need_short/", edit_need_short, name="edit_need_short"
    ),
    path(
        "potrzebydoakceptacji/",
        PotrzebyDoAkceptacji.as_view(),
        name="need-list-potrzebydoakceptacji",
    ),
    path("edit_purchase_short/", edit_purchase_short, name="edit_purchase_short"),
    path("edit_contract_short/", edit_contract_short, name="edit_contract_short"),
    path("edit_need_short/", edit_need_short, name="edit_need_short"),
    path("edit_idea_short/", edit_idea_short, name="edit_idea_short"),
    path("wszystkiepotrzeby/edit_need_short/", edit_need_short, name="edit_need_short"),
    path(
        "potrzebybezzakupow/edit_need_short/", edit_need_short, name="edit_need_short"
    ),
    path(
        "wszystkiepotrzeby/",
        WszystkiePotrzeby.as_view(),
        name="needs-list-wszystkiepotrzeby",
    ),
    path(
        "potrzebybezzakupow/", PotrzebyBezZakupow.as_view(), name="potrzebybezzakupow"
    ),
    path(
        "potrzebydozamkniecia/",
        PotrzebyDoZamkniecia.as_view(),
        name="potrzebydozamkniecia",
    ),
    path(
        "potrzebydozamkniecia/edit_need_short/", edit_need_short, name="edit_need_short"
    ),
    path("", views.index, name="index_needs"),
    path("testauto", testauto, name="testauto"),
    path("testautodynamic", testautodynamic, name="testautodynamic"),
]
