import logging
import unidecode

from django import forms
from django.conf import settings
from django.contrib import admin, messages
from django.contrib.admin import AdminSite
from django.contrib.auth.models import User, Group
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import path, reverse, reverse_lazy
from django.utils.encoding import force_bytes
from django.utils.html import format_html
from django.utils.http import urlsafe_base64_encode
from django.utils.text import slugify
from django.views.generic import FormView

from general.mail import utworz_mail_do_wyslania, wyslij_mail_do_grupy
from general.linki import generate_user_url
from .models import (
    Sections,
    Clients,
    Status_akceptacji,
    Status_procesu,
    Pilnosc,
    Crip,
    Sposob_zakupu,
    Acceptor,
    Sposob_wyceny,
    Zgodnosc_mapy,
    Rodzaj_inicjatywy,
    Priorytet_inicjatywy,
    Rodzaje_uslug,
    Klasyfikacja_zmiany,
    Poziomy_dostepnosci,
    Dostepnosci_rozwiazania,
    MaileDoWyslania,
    Note,
    Parametry,
    zlecenia_kontrolingowe,
    uslugi,
    Planowane_zakupy,
    Stamp,
    Meeting,
    Resolution,
    MeetingStatus,
    Variable,
)

from account.models import Basket
from contracts.models import Contracts
from ideas.models import Ideas
from needs.models import Needs
from purchases.models import Purchases, EZZ

logger = logging.getLogger("avantic")

# Rejestracja modeli w standardowym panelu admina
admin.site.register(Sections)
admin.site.register(Clients)
admin.site.register(Status_procesu)
admin.site.register(Status_akceptacji)
admin.site.register(Pilnosc)
admin.site.register(Crip)
admin.site.register(Sposob_zakupu)
admin.site.register(Acceptor)
admin.site.register(Sposob_wyceny)
admin.site.register(Zgodnosc_mapy)
admin.site.register(Rodzaj_inicjatywy)
admin.site.register(Priorytet_inicjatywy)
admin.site.register(Rodzaje_uslug)
admin.site.register(Klasyfikacja_zmiany)
admin.site.register(Poziomy_dostepnosci)
admin.site.register(Dostepnosci_rozwiazania)
admin.site.register(MaileDoWyslania)
admin.site.register(Note)
admin.site.register(Parametry)
admin.site.register(zlecenia_kontrolingowe)
admin.site.register(uslugi)
admin.site.register(Planowane_zakupy)
admin.site.register(Stamp)
admin.site.register(Meeting)
admin.site.register(Resolution)
admin.site.register(MeetingStatus)
admin.site.register(Variable)


class MyAdminSite(AdminSite):
    site_header = "Aprobo - Panel Administracyjny"
    site_title = "Aprobo - Panel Administracyjny"

    def has_permission(self, request):
        """Zwraca True, jeśli użytkownik jest aktywny i należy do grupy 'superuser'."""
        return request.user.is_active and (
            request.user.groups.filter(name__in=["superuser"]).exists()
            or request.user.groups.filter(name__in=["useradmin"]).exists()
            or request.user.groups.filter(name__in=["dataadmin"]).exists()
        )

    def each_context(self, request):
        context = super().each_context(request)
        context["extra_links"] = [
            {"name": "Pomysły", "url": reverse("index_ideas")},
            {"name": "Potrzeby", "url": reverse("index_needs")},
            {"name": "Zakupy", "url": reverse("index_purchases")},
            {"name": "Umowy", "url": reverse("index_contracts")},
            {"name": "Zarządzanie", "url": reverse("index")},
            {"name": "Autoryzacja", "url": reverse("dashboard")},
        ]
        return context


my_admin_site = MyAdminSite(name="myadmin")


# Mixin for permissions
class CustomAdminMixin:
    def has_add_permission(self, request):
        return True

    def has_change_permission(self, request, obj=None):
        return True

    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser

    def is_superuser_only(self, request):
        return True


class ContractsAdmin(CustomAdminMixin, admin.ModelAdmin):
    list_display = ("subject", "numer_umowy", "section", "koordynator")
    search_fields = [
        "subject",
        "numer_umowy",
        "section__short_name",
        "koordynator__username",
    ]
    fields = ("section", "koordynator")


class IdeasAdmin(CustomAdminMixin, admin.ModelAdmin):
    list_display = (
        "subject",
        "status_idei",
        "status_akceptacji",
        "section",
        "client",
        "osoba_prowadzaca",
    )
    search_fields = ["subject", "id", "id__icontains"]
    fields = (
        "status_idei",
        "status_akceptacji",
        "section",
        "client",
        "osoba_prowadzaca",
    )


class NeedsAdmin(CustomAdminMixin, admin.ModelAdmin):
    list_display = (
        "subject",
        "status_potrzeby",
        "status_akceptacji",
        "section",
        "client",
        "osoba_prowadzaca",
    )
    search_fields = ["subject", "id", "id__icontains"]
    fields = (
        "status_potrzeby",
        "status_akceptacji",
        "section",
        "client",
        "osoba_prowadzaca",
        "zlecenia_kontrolingowe",
        "uslugi",
        "status_akceptacji_infrastruktury",
        "status_akceptacji_sieci",
        "status_akceptacji_finansow",
        "status_akceptacji_uslug",
    )
    filter_horizontal = ("zlecenia_kontrolingowe", "uslugi")  # lub filter_vertical


class PurchasesAdmin(CustomAdminMixin, admin.ModelAdmin):
    list_display = (
        "przedmiot_zakupu",
        "status_procesu",
        "status_akceptacji",
        "section",
        "client",
        "osoba_prowadzaca",
    )
    search_fields = ["przedmiot_zakupu"]
    fields = (
        "status_procesu",
        "status_akceptacji",
        "section",
        "client",
        "osoba_prowadzaca",
    )


class ClientsAdmin(CustomAdminMixin, admin.ModelAdmin):
    list_display = ("name", "short_name")
    search_fields = ["name", "short_name"]
    filter_horizontal = ["users"]


class PilnoscAdmin(CustomAdminMixin, admin.ModelAdmin):
    list_display = ("pilnosc",)
    search_fields = ["pilnosc"]


class SposobWycenyAdmin(CustomAdminMixin, admin.ModelAdmin):
    list_display = ("sposob_wyceny",)
    search_fields = ["sposob_wyceny"]


class RodzajInicjatywyAdmin(CustomAdminMixin, admin.ModelAdmin):
    list_display = ("rodzaj_inicjatywy",)
    search_fields = ["rodzaj_inicjatywy"]


class PriorytetInicjatywyAdmin(CustomAdminMixin, admin.ModelAdmin):
    list_display = ("priorytet_inicjatywy",)
    search_fields = ["priorytet_inicjatywy"]


class RodzajeUslugAdmin(CustomAdminMixin, admin.ModelAdmin):
    list_display = ("usluga",)
    search_fields = ["usluga"]


class KlasyfikacjaZmianyAdmin(CustomAdminMixin, admin.ModelAdmin):
    list_display = ("zmiana",)
    search_fields = ["zmiana"]


class PoziomyDostepnosciAdmin(CustomAdminMixin, admin.ModelAdmin):
    list_display = ("poziom",)
    search_fields = ["poziom"]


class DostepnosciRozwiazaniaAdmin(CustomAdminMixin, admin.ModelAdmin):
    list_display = ("poziom",)
    search_fields = ["poziom"]


class ParametryAdmin(CustomAdminMixin, admin.ModelAdmin):
    list_display = ("nazwa", "opis", "num", "str")
    search_fields = ["nazwa"]


# Register models in custom admin
my_admin_site.register(Clients, ClientsAdmin)
my_admin_site.register(Pilnosc, PilnoscAdmin)
my_admin_site.register(Sposob_wyceny, SposobWycenyAdmin)
my_admin_site.register(Rodzaj_inicjatywy, RodzajInicjatywyAdmin)
my_admin_site.register(Priorytet_inicjatywy, PriorytetInicjatywyAdmin)
my_admin_site.register(Rodzaje_uslug, RodzajeUslugAdmin)
my_admin_site.register(Klasyfikacja_zmiany, KlasyfikacjaZmianyAdmin)
my_admin_site.register(Poziomy_dostepnosci, PoziomyDostepnosciAdmin)
my_admin_site.register(Dostepnosci_rozwiazania, DostepnosciRozwiazaniaAdmin)
my_admin_site.register(Parametry, ParametryAdmin)
my_admin_site.register(Contracts, ContractsAdmin)
my_admin_site.register(Needs, NeedsAdmin)
my_admin_site.register(Ideas, IdeasAdmin)
my_admin_site.register(Purchases, PurchasesAdmin)


# Register Basket model from account
def register_basket_in_myadmin():
    from account.admin import BasketAdmin

    my_admin_site.register(Basket, BasketAdmin)


register_basket_in_myadmin()


# Unregister default User model if already registered
try:
    my_admin_site.unregister(User)
except admin.sites.NotRegistered:
    pass


# User form with baskets and sections
class UserBasketForm(forms.ModelForm):
    baskets = forms.ModelMultipleChoiceField(
        queryset=Basket.objects.all(),
        required=False,
        widget=admin.widgets.FilteredSelectMultiple("Baskets", is_stacked=False),
    )

    sections = forms.ModelMultipleChoiceField(
        queryset=Sections.objects.all(),
        required=False,
        widget=admin.widgets.FilteredSelectMultiple("Sections", is_stacked=False),
        label="Sections",
    )

    class Meta:
        model = User
        fields = [
            "username",
            "email",
            "first_name",
            "last_name",
            "is_active",
            "sections",
        ]
        labels = {
            "username": "Nazwa użytkownika",
            "email": "Adres e-mail",
            "first_name": "Imię",
            "last_name": "Nazwisko",
            "sections": "Działy",
            "is_active": "Czy aktywny",
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.pk:
            user_groups = set(self.instance.groups.all())
            valid_baskets = Basket.objects.filter(groups__in=user_groups).distinct()

            final_baskets = []
            for basket in valid_baskets:
                basket_groups = set(basket.groups.all())
                if basket_groups.issubset(user_groups):
                    final_baskets.append(basket)

            def is_covered_by_other_baskets(basket_groups, other_baskets):
                for other_basket in other_baskets:
                    if set(other_basket.groups.all()).issuperset(basket_groups):
                        return True
                return False

            changed = True
            while changed:
                changed = False
                filtered_baskets = []
                for basket in final_baskets:
                    other_baskets = [b for b in final_baskets if b != basket]
                    if not is_covered_by_other_baskets(
                        set(basket.groups.all()), other_baskets
                    ):
                        filtered_baskets.append(basket)
                    else:
                        changed = True
                final_baskets = filtered_baskets

            self.fields["baskets"].initial = final_baskets
            self.fields["sections"].initial = self.instance.custom_models.all()

    def save(self, commit=True):
        user = super().save(commit=commit)
        if commit:
            self.save_m2m()

        selected_baskets = self.cleaned_data.get("baskets", [])
        new_groups = set()
        for basket in selected_baskets:
            new_groups.update(basket.groups.all())

        user.groups.set(new_groups)

        selected_sections = self.cleaned_data.get("sections", [])
        user.custom_models.set(selected_sections)

        return user


def send_password_reset_email(modeladmin, request, queryset):
    for user in queryset:
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = default_token_generator.make_token(user)
        reset_url = request.build_absolute_uri(
            reverse("password_reset_confirm", kwargs={"uidb64": uid, "token": token})
        )

        subject = "Reset hasła na Twoim koncie"
        message = f"Kliknij poniższy link, aby zresetować swoje hasło:\n{reset_url}"
        send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [user.email])


send_password_reset_email.short_description = "Wyślij link resetujący hasło"


class UserBasketAdmin(admin.ModelAdmin):
    actions = [send_password_reset_email]
    form = UserBasketForm
    list_display = (
        "username",
        "email",
        "first_name",
        "last_name",
        "is_active",
        "send_reset_password_link",
        "change_password_link",
    )
    search_fields = ("username", "email")
    filter_horizontal = ["groups"]

    def change_password_link(self, obj):
        url = reverse("admin:auth_user_password_change", args=[obj.id])
        return format_html(f'<a href="{url}">Zmień hasło</a>')

    change_password_link.short_description = "Zmień hasło"

    def has_add_permission(self, request):
        return False
        # return request.user.groups.filter(name="useradmin").exists()

    def send_reset_password_link(self, obj):
        url = f"/account/{obj.pk}/send_password_reset/"
        return format_html(
            f'<a class="button" href="{url}">Wyślij link resetujący hasło</a>'
        )

    send_reset_password_link.short_description = "Wyślij link resetujący hasło"

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path(
                "<int:user_id>/send_password_reset/",
                self.admin_site.admin_view(self.send_password_reset),
                name="user_send_password_reset",  # Aktualizacja nazwy ścieżki
            ),
        ]
        return custom_urls + urls

    def send_password_reset(self, request, user_id, *args, **kwargs):
        user = get_object_or_404(User, pk=user_id)
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = default_token_generator.make_token(user)
        reset_url = f"{settings.DEFAULT_DOMAIN}{reverse('password_reset_confirm', kwargs={'uidb64': uid, 'token': token})}"

        subject = "Reset hasła na Twoim koncie"
        message = f"Kliknij poniższy link, aby zresetować swoje hasło:\n{reset_url}"
        send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [user.email])

        self.message_user(
            request, f"Link resetujący hasło został wysłany do {user.email}."
        )
        return redirect("admin:auth_user_change", user_id)

    def send_reset_password_link(self, obj):
        # Korzystanie z nowej ścieżki 'account:send_password_reset'
        url = reverse("send_password_reset", args=[obj.pk])
        return format_html(
            f'<a class="button" href="{url}">Wyślij link resetujący hasło</a>'
        )


# Group form with user management
class GroupAdminForm(forms.ModelForm):
    users = forms.ModelMultipleChoiceField(
        queryset=User.objects.all(),
        required=False,
        widget=admin.widgets.FilteredSelectMultiple("Users", is_stacked=False),
    )

    class Meta:
        model = Group
        fields = ["users"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.pk:
            self.fields["users"].initial = self.instance.user_set.all()

    def save(self, commit=True):
        group = super().save(commit=commit)
        if commit:
            group.user_set.set(self.cleaned_data["users"])
        return group


# Admin for Group model
class GroupAdmin(admin.ModelAdmin):
    form = GroupAdminForm
    list_display = ("name",)
    filter_horizontal = ["permissions"]

    def has_add_permission(self, request):
        return False


my_admin_site.register(User, UserBasketAdmin)
my_admin_site.register(Group, GroupAdmin)


# Admin for Sections model
class SectionsAdmin(CustomAdminMixin, admin.ModelAdmin):
    list_display = ("name", "short_name", "kierownik_display")
    search_fields = ["name", "short_name", "kierownik__username"]
    filter_horizontal = ["users"]
    fields = ("name", "short_name", "kierownik", "users")

    def kierownik_display(self, obj):
        """Wyświetla pełne imię i nazwisko kierownika, jeśli przypisany"""
        if obj.kierownik:
            return obj.kierownik.get_full_name()
        return "-"

    kierownik_display.short_description = "Kierownik"


my_admin_site.register(Sections, SectionsAdmin)


class EZZAdmin(admin.ModelAdmin):
    search_fields = ("EZZ_number", "subject")
    list_display = ("EZZ_number", "subject", "ordering_person", "creation_date")

    def has_add_permission(self, request):
        return False


my_admin_site.register(EZZ, EZZAdmin)
