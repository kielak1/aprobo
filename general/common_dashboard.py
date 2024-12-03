from django.shortcuts import render  # , redirect
from contracts.models import Contracts

from general.models import Sections, Clients
from needs.models import Needs, LogNeed
from ideas.models import Ideas, LogIdea
from contracts.models import LogContract
from purchases.models import Purchases, LogPurchase
from needs.views_wszystkiepotrzeby import NeedsShortTable
from ideas.views_wszystkiepomysly import IdeasShortTable
from contracts.views_wszystkieumowyaktywne import ContractsShortTable
from purchases.views_wszystkiezakupy import PurchasesShortTable
from django_tables2 import RequestConfig
from django.db.models import Q
from contracts.views_statystyka import przygotuj_dane_do_szablonu

from django.db.models import Max
from django.contrib.auth.models import User
from general.parametry import get_param_int
from general.common_context import common_context

import logging

logger = logging.getLogger("avantic")


def get_last_activity(user):
    # Pobranie ostatniego logu z każdego modelu
    last_contract = LogContract.objects.filter(user=user).aggregate(
        last_activity=Max("data")
    )["last_activity"]
    last_idea = LogIdea.objects.filter(user=user).aggregate(last_activity=Max("data"))[
        "last_activity"
    ]
    last_need = LogNeed.objects.filter(user=user).aggregate(last_activity=Max("data"))[
        "last_activity"
    ]
    last_purchase = LogPurchase.objects.filter(user=user).aggregate(
        last_activity=Max("data")
    )["last_activity"]

    # Lista zawierająca wszystkie daty aktywności (filtrowanie wartości None)
    activity_dates = list(
        filter(None, [last_contract, last_idea, last_need, last_purchase])
    )

    # Sprawdzamy, czy lista nie jest pusta przed wywołaniem max()
    if activity_dates:
        return max(activity_dates)
    else:
        return None  # Brak aktywności


def activity_list(request):
    users = User.objects.all()
    activity_data = []

    for user in users:
        last_activity = get_last_activity(user)
        if last_activity:  # Dodajemy tylko użytkowników, którzy mają jakąś aktywność
            activity_data.append(
                {
                    "username": user.username,  # Używamy 'username' zamiast obiektu 'user'
                    "last_activity": last_activity,  # Zwracamy 'last_activity' jako pole w słowniku
                }
            )

    # Sortowanie użytkowników po czasie ostatniej aktywności
    activity_data.sort(key=lambda x: x["last_activity"], reverse=True)

    # Kontekst do przekazania do szablonu
    context = {"activity_data": activity_data}

    return context


def common_dashboard(adres_url, request):
    liczba_elementow = get_param_int("liczba_obiektow_na_dashboard", 6)
    liczba_elementow_klient = get_param_int("liczba_obiektow_na_dashboard_klient", 20)
    user = request.user
    dzialy = []
    grupy = []
    is_lead_maker = False
    is_recommender = False
    com_cont = common_context(request)

    if user.is_authenticated:
        if request.user.groups.filter(name="lead_maker").exists():
            is_lead_maker = True
        if request.user.groups.filter(name="idea_recommender").exists():
            is_recommender = True
        if request.user.groups.filter(name="need_recommender").exists():
            is_recommender = True
        if request.user.groups.filter(name="purchase_recommender").exists():
            is_recommender = True

        sections = Sections.objects.filter(users=user)
        dzialy = [dzial.short_name for dzial in sections]

        klienci_rel = com_cont["klienci_rel"]

        grupy = [group.name for group in user.groups.all()]
        if "need_viewer" in grupy:
            excluded_statuses = ["zamknięta", "zrealizowana"]
            needs_queryset = Needs.objects.filter(
                section__short_name__in=dzialy
            ).exclude(status_potrzeby__status__in=excluded_statuses)

            needs_queryset = needs_queryset.annotate(
                latest_log_date=Max("log__data")
            ).filter(latest_log_date__isnull=False)
            needs_queryset = needs_queryset.order_by("-latest_log_date")
            needs_queryset = needs_queryset[:liczba_elementow]

        else:
            needs_queryset = Needs.objects.none()  # Nie pokazuj żadnych rekordów
        is_client = request.user.groups.filter(name="client").exists()
        if "idea_viewer" in grupy:
            excluded_statuses = ["zamknięta", "zrealizowana"]
            ideas_queryset = Ideas.objects.filter(
                section__short_name__in=dzialy
            ).exclude(status_idei__status__in=excluded_statuses)

            ideas_queryset = ideas_queryset.annotate(
                latest_log_date=Max("log__data")
            ).filter(latest_log_date__isnull=False)
            ideas_queryset = ideas_queryset.order_by("-latest_log_date")
            ideas_queryset = ideas_queryset[:liczba_elementow]
        else:
            if is_client:
                excluded_statuses = ["zamknięta", "zrealizowana"]
                ideas_queryset = Ideas.objects.filter(
                    client__short_name__in=klienci_rel
                ).exclude(status_idei__status__in=excluded_statuses)

                ideas_queryset = ideas_queryset.annotate(
                    latest_log_date=Max("log__data")
                ).filter(latest_log_date__isnull=False)
                ideas_queryset = ideas_queryset.order_by("-latest_log_date")
                ideas_queryset = ideas_queryset[:liczba_elementow_klient]
            else:
                ideas_queryset = Ideas.objects.none()  # Nie pokazuj żadnych rekordów

        if "purchase_viewer" in grupy:
            excluded_statuses = ["anulowany", "zakończony"]
            purchases_queryset = Purchases.objects.filter(
                section__short_name__in=dzialy
            ).exclude(status_procesu__status__in=excluded_statuses)

            purchases_queryset = purchases_queryset.annotate(
                latest_log_date=Max("log__data")
            ).filter(latest_log_date__isnull=False)
            purchases_queryset = purchases_queryset.order_by("-latest_log_date")
            purchases_queryset = purchases_queryset[:liczba_elementow]

        else:
            purchases_queryset = (
                Purchases.objects.none()
            )  # Nie pokazuj żadnych rekordów

        if "contract_viewer" in grupy:
            contracts_queryset = Contracts.objects.filter(
                Q(section__short_name__in=dzialy) & Q(obslugiwana=True)
            )
            contracts_queryset = contracts_queryset.annotate(
                latest_log_date=Max("log__data")
            ).filter(latest_log_date__isnull=False)
            contracts_queryset = contracts_queryset.order_by("-latest_log_date")
            contracts_queryset = contracts_queryset[:liczba_elementow]
        else:
            contracts_queryset = (
                Contracts.objects.none()
            )  # Nie pokazuj żadnych rekordów

    else:
        needs_queryset = Needs.objects.none()  # Nie pokazuj żadnych rekordów
        ideas_queryset = Ideas.objects.none()  # Nie pokazuj żadnych rekordów
        purchases_queryset = Purchases.objects.none()  # Nie pokazuj żadnych rekordów
        contracts_queryset = Contracts.objects.none()  # Nie pokazuj żadnych rekordów

    table_needs = NeedsShortTable(needs_queryset)
    table_ideas = IdeasShortTable(ideas_queryset)
    table_purchases = PurchasesShortTable(purchases_queryset)
    table_contracts = ContractsShortTable(contracts_queryset)

    RequestConfig(request).configure(table_needs)
    RequestConfig(request).configure(table_ideas)
    RequestConfig(request).configure(table_purchases)
    RequestConfig(request).configure(table_contracts)
    ideas_do_akceptacji = Ideas.objects.filter(
        status_akceptacji__akceptacja="do akceptacji"
    ).count()
    needs_do_akceptacji = Needs.objects.filter(
        status_akceptacji__akceptacja="do akceptacji"
    ).count()
    purchases_do_akceptacji = Purchases.objects.filter(
        status_akceptacji__akceptacja="do akceptacji"
    ).count()
    needs_do_akceptacji_infra = Needs.objects.filter(
        Q(status_akceptacji_infrastruktury__akceptacja="do akceptacji")
        & Q(status_potrzeby__status="realizowana")
        & ~Q(status_akceptacji__akceptacja="zaakceptowane")
    ).count()
    needs_do_akceptacji_siec = Needs.objects.filter(
        Q(status_akceptacji_sieci__akceptacja="do akceptacji")
        & Q(status_potrzeby__status="realizowana")
        & ~Q(status_akceptacji__akceptacja="zaakceptowane")
    ).count()
    needs_do_akceptacji_finanse = Needs.objects.filter(
        Q(status_akceptacji_finansow__akceptacja="do akceptacji")
        & Q(status_potrzeby__status="realizowana")
        & ~Q(status_akceptacji__akceptacja="zaakceptowane")
    ).count()
    needs_do_akceptacji_uslugi = Needs.objects.filter(
        Q(status_akceptacji_uslug__akceptacja="do akceptacji")
        & Q(status_potrzeby__status="realizowana")
        & ~Q(status_akceptacji__akceptacja="zaakceptowane")
    ).count()
    needs_late_accept = Needs.objects.filter(
        Q(status_akceptacji__akceptacja="zaakceptowane")
        & (  # Główna akceptacja musi być zaakceptowana
            Q(status_akceptacji_uslug__akceptacja="do akceptacji")
            | Q(status_akceptacji_sieci__akceptacja="do akceptacji")
            | Q(status_akceptacji_infrastruktury__akceptacja="do akceptacji")
            | Q(status_akceptacji_finansow__akceptacja="do akceptacji")
        )
    ).count()

    ideas_do_decyzji_rady = Ideas.objects.filter(
        Q(status_idei__status="rada architektury") & Q(czy_dotyczy_architektury=True)
    ).count()
    needs_do_decyzji_rady = Needs.objects.filter(
        Q(status_potrzeby__status="rada architektury")
        & Q(czy_dotyczy_architektury=True)
    ).count()

    ideas_do_analizy = Ideas.objects.filter(Q(status_idei__status="analiza")).count()
    needs_do_analizy = Needs.objects.filter(
        Q(status_potrzeby__status="analiza")
    ).count()

    ideas_wstrzymane = Ideas.objects.filter(Q(status_idei__status="wstrzymane")).count()
    needs_wstrzymane = Needs.objects.filter(
        Q(status_potrzeby__status="wstrzymane")
    ).count()

    dane_do_szablonu = przygotuj_dane_do_szablonu()
    context = {
        "userx": user.username,
        "dzialy": dzialy,
        "grupy": grupy,
        "table_needs": table_needs,
        "table_ideas": table_ideas,
        "table_purchases": table_purchases,
        "table_contracts": table_contracts,
        "is_lead_maker": is_lead_maker,
        "ideas_do_akceptacji": ideas_do_akceptacji,
        "needs_do_akceptacji": needs_do_akceptacji,
        "purchases_do_akceptacji": purchases_do_akceptacji,
        "needs_do_akceptacji_infra": needs_do_akceptacji_infra,
        "needs_do_akceptacji_siec": needs_do_akceptacji_siec,
        "needs_do_akceptacji_finanse": needs_do_akceptacji_finanse,
        "needs_do_akceptacji_uslugi": needs_do_akceptacji_uslugi,
        "ideas_do_decyzji_rady": ideas_do_decyzji_rady,
        "needs_do_decyzji_rady": needs_do_decyzji_rady,
        "ideas_do_analizy": ideas_do_analizy,
        "needs_do_analizy": needs_do_analizy,
        "ideas_wstrzymane": ideas_wstrzymane,
        "needs_wstrzymane": needs_wstrzymane,
        "needs_late_accept": needs_late_accept,
        # "klienci": klienci,
        # "klienci_rel": klienci_rel,
    }

    context.update(dane_do_szablonu)

    kto_byl_aktywny = activity_list(request)

    if kto_byl_aktywny:
        context.update(kto_byl_aktywny)

    context.update(com_cont)

    return render(request, adres_url, context)
