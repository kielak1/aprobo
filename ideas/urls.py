from django.urls import path
from .views_wszystkiepomysly import WszystkiePomysly, PomyslyKlienta
from .views_pomysly_do_akceptacji import PomyslyDoAkceptacji
from . import views
from .views_edit_idea import edit_idea_short
from needs.views_edit_need import edit_need_short
from contracts.views_edit_contract import edit_contract_short
from purchases.views_edit_purchase import edit_purchase_short
from ideas.raport_pomyslow import export_pomysly_to_excel, export_all_pomysly_to_excel

urlpatterns = [
    path("edit_purchase_short/", edit_purchase_short, name="edit_purchase_short"),
    path("edit_contract_short/", edit_contract_short, name="edit_contract_short"),
    path("edit_need_short/", edit_need_short, name="edit_need_short"),
    path("edit_idea_short/", edit_idea_short, name="edit_idea_short"),
    path(
        "pomyslydoakceptacji/edit_idea_short/", edit_idea_short, name="edit_idea_short"
    ),
    path("wszystkiepomysly/edit_idea_short/", edit_idea_short, name="edit_idea_short"),
    path(
        "wszystkiepomysly/",
        WszystkiePomysly.as_view(),
        name="ideas-list-wszystkiepomysly",
    ),
    path("pomyslyklienta/", PomyslyKlienta.as_view(), name="ideas-list-pomyslyklienta"),
    path("pomyslyklienta/edit_idea_short/", edit_idea_short, name="edit_idea_short"),
    path(
        "pomyslydoakceptacji/",
        PomyslyDoAkceptacji.as_view(),
        name="ideas-list-pomyslydoakceptacji",
    ),
    path("", views.index, name="index_ideas"),
    path("excell", export_pomysly_to_excel, name="export_pomysly_to_excel"),
    path("excell_all", export_all_pomysly_to_excel, name="export_all_pomysly_to_excel"),
]
