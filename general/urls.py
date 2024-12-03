from django.urls import path, re_path
from . import views
from .admin import my_admin_site
from .crip_views import WszystkieCripy, LinkedCrips, AloneCrips
from .views_edit_crip import edit_crip_short, edit_crip_short_new
from .views_edit_uslugi import edit_uslugi_short, edit_uslugi_short_new
from .views_edit_zlecenia import edit_zlecenia_short, edit_zlecenia_short_new
from .full_search_form_view import search_view
from ideas.views_edit_idea import edit_idea_short
from needs.views_edit_need import edit_need_short
from contracts.views_edit_contract import edit_contract_short
from purchases.views_edit_purchase import edit_purchase_short
from .auto_ezz import auto_ezz
from .contract_list import ContractsView
from .views_uslugi_import import uslugi_import
from .views_zlecenia_import import zlecenia_import
from .views_zlecenia_export import zlecenia_export
from .views_uslugi_export import uslugi_export
from .views_crip_export import crip_export
from .uslugi_views import WszystkieUslugi
from .zlecenia_views import WszystkieZlecenia
from .autocomplete import (
    UslugiAutocomplete,
    ZleceniaAutocomplete,
    InvitationsAutocomplete,
    AttendanceAutocomplete,
    DiscussedIdeasAutocomplete,
    DiscussedNeedsAutocomplete,
    CripsAutocomplete,
    RodzajeUslugAutocomplete,
)
from .database import odtworz_stale
from .rady_views import WszystkieRady
from .views_edit_rada import edit_rada, new_rada
from .doc_view import protokol_rady_architektury
from general.aggregated_stamp_view import aggregated_stamp_view
from general.test_page import test_view

urlpatterns = [
    path("", views.index, name="index"),
    path("myadmin/", my_admin_site.urls),
    path("crip-list/", WszystkieCripy.as_view(), name="crip-list-all"),
    path("crip-linked/", LinkedCrips.as_view(), name="crip-linked"),
    path("crip-alone/", AloneCrips.as_view(), name="crip-alone"),
    path("edit_crip_short/", edit_crip_short, name="edit_crip_short"),
    path("crip-list/edit_crip_short/", edit_crip_short, name="edit_crip_short"),
    path("crip-linked/edit_crip_short/", edit_crip_short, name="edit_crip_short"),
    path("crip-alone/edit_crip_short/", edit_crip_short, name="edit_crip_short"),
    path("edit_crip_short_new/", edit_crip_short_new, name="edit_crip_short_new"),
    path("full_search/", search_view, name="full_search"),
    path("edit_purchase_short/", edit_purchase_short, name="edit_purchase_short"),
    path("edit_contract_short/", edit_contract_short, name="edit_contract_short"),
    path("edit_need_short/", edit_need_short, name="edit_need_short"),
    path("edit_idea_short/", edit_idea_short, name="edit_idea_short"),
    path("auto_ezz/", auto_ezz, name="auto_ezz"),
    path("contracts/", ContractsView.as_view(), name="contracts_list"),
    path("import_uslug/", uslugi_import, name="import_uslug"),
    path("import_zlecen/", zlecenia_import, name="import_zlecen"),
    path("export_zlecen/", zlecenia_export, name="export_zlecen"),
    path("export_uslug/", uslugi_export, name="export_uslug"),
    path("export_crip/", crip_export, name="export_crip"),
    path("uslug-list/", WszystkieUslugi.as_view(), name="uslug-list-all"),
    path("zlecenia-list/", WszystkieZlecenia.as_view(), name="zlecenia-list-all"),
    path("edit_uslugi_short_new/", edit_uslugi_short_new, name="edit_uslugi_short_new"),
    path(
        "edit_zlecenia_short_new/",
        edit_zlecenia_short_new,
        name="edit_zlecenia_short_new",
    ),
    path("edit_uslugi_short/", edit_uslugi_short, name="edit_uslugi_short"),
    path("edit_zlecenia_short/", edit_zlecenia_short, name="edit_zlecenia_short"),
    path("uslug-list/edit_uslugi_short/", edit_uslugi_short, name="edit_uslugi_short"),
    path(
        "zlecenia-list/edit_zlecenia_short/",
        edit_zlecenia_short,
        name="edit_zlecenia_short",
    ),
    path("baza/stale/", odtworz_stale, name="odtworz_stale"),
    path("rady-list/", WszystkieRady.as_view(), name="rady-list-all"),
    path("rady-new/", new_rada, name="new_rada"),
    path("edit_rada/<int:meeting_id>/", edit_rada, name="edit_rada"),
    path(
        "protokol-rady/<int:id_rady>/",
        protokol_rady_architektury,
        name="protokol_rady_architektury",
    ),
    path("stamp/", aggregated_stamp_view, name="aggregated_stamp_view"),
    path("test/", test_view, name="test_page"),
   
    re_path(
        r"^zlecenia-autocomplete/$",
        ZleceniaAutocomplete.as_view(),
        name="zlecenia-autocomplete",
    ),
    re_path(
        r"^uslugi-autocomplete/$",
        UslugiAutocomplete.as_view(),
        name="uslugi-autocomplete",
    ),
    re_path(
        r"^invitations-autocomplete/$",
        InvitationsAutocomplete.as_view(),
        name="invitations-autocomplete",
    ),
    re_path(
        r"^attendance_list-autocomplete/$",
        AttendanceAutocomplete.as_view(),
        name="attendance_list-autocomplete",
    ),
    re_path(
        r"^discussed_ideas-autocomplete/$",
        DiscussedIdeasAutocomplete.as_view(),
        name="discussed_ideas-autocomplete",
    ),
    re_path(
        r"^discussed_needs-autocomplete/$",
        DiscussedNeedsAutocomplete.as_view(),
        name="discussed_needs-autocomplete",
    ),
    re_path(
        r"^crips-autocomplete/$",
        CripsAutocomplete.as_view(),
        name="crips-autocomplete",
    ),
    re_path(
        r"^rodzaje-uslug-autocomplete/$",
        RodzajeUslugAutocomplete.as_view(),
        name="rodzaje-uslug-autocomplete",
    ),
]



#RodzajeUslugAutocomplete