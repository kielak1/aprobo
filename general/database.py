from django.shortcuts import render, redirect
from django.core.exceptions import ValidationError
from zipfile import BadZipFile
from ideas.models import StatusIdei
from needs.models import StatusNeed
from general.models import MeetingStatus
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.models import Group
from general.common_context import common_context
from account.models import Basket
from django.db.models import Count


@csrf_protect
def odtworz_stale(request):
    if (
        not request.user.is_authenticated
        or not request.user.groups.filter(name="dataadmin").exists()
    ):
        return redirect("/account/login")

    target_rada_statuses = [
        "nowe",
        "otwarte",
        "zamknięte",
    ]

    lista_dodanych_rada = []
    # Pobierz aktualne statusy z bazy danych
    current_rada_statuses = MeetingStatus.objects.values_list("status", flat=True)

    # Dodaj brakujące statusy
    for status in target_rada_statuses:
        if status not in current_rada_statuses:
            MeetingStatus.objects.create(status=status)
            lista_dodanych_rada.append(status)

    # Usuń nadmiarowe statusy
    MeetingStatus.objects.filter(
        status__in=set(current_rada_statuses) - set(target_rada_statuses)
    ).delete()

    target_statuses = [
        "rada architektury",
        "zrealizowana",
        "zamknięta",
        "realizowana",
        "zawieszona",
        "nowa",
        "analiza",
        "wstrzymane",
    ]

    lista_dodanych = []
    # Pobierz aktualne statusy z bazy danych
    current_statuses = StatusIdei.objects.values_list("status", flat=True)

    # Dodaj brakujące statusy
    for status in target_statuses:
        if status not in current_statuses:
            StatusIdei.objects.create(status=status)
            lista_dodanych.append(status)

    # Usuń nadmiarowe statusy
    StatusIdei.objects.filter(
        status__in=set(current_statuses) - set(target_statuses)
    ).delete()

    target_need_statuses = [
        "rada architektury",
        "zrealizowana",
        "zamknięta",
        "realizowana",
        "nowa",
        "analiza",
        "wstrzymane",
    ]

    lista_dodanych_need = []
    # Pobierz aktualne statusy z bazy danych
    current_need_statuses = StatusNeed.objects.values_list("status", flat=True)

    # Dodaj brakujące statusy

    for status in target_need_statuses:
        if status not in current_need_statuses:
            StatusNeed.objects.create(status=status)
            lista_dodanych_need.append(status)

    # Usuń nadmiarowe statusy
    StatusNeed.objects.filter(
        status__in=set(current_need_statuses) - set(target_need_statuses)
    ).delete()

    # Definicja docelowych grup
    target_groups = [
        "accountant",
        "advanced",
        "client",
        "contract_allocator",
        "contract_editor",
        "contract_viewer",
        "idea_acceptor",
        "idea_allocator",
        "idea_editor",
        "idea_recommender",
        "idea_viewer",
        "kierownictwo",
        "lead_maker",
        "need_acceptor",
        "need_allocator",
        "need_editor",
        "need_finanse_acceptor",
        "need_infra_acceptor",
        "need_maker",
        "need_net_acceptor",
        "need_recommender",
        "need_service_acceptor",
        "need_viewer",
        "purchase_acceptor",
        "purchase_allocator",
        "purchase_editor",
        "purchase_recommender",
        "purchase_viewer",
        "superuser",
        "useradmin",
        "dataadmin",
    ]

    lista_dodanych_grup = []
    # Pobierz aktualne grupy z bazy danych
    current_groups = Group.objects.values_list("name", flat=True)

    # Dodaj brakujące grupy
    for group in target_groups:
        if group not in current_groups:
            Group.objects.create(name=group)
            lista_dodanych_grup.append(group)

    # Usuń nadmiarowe grupy
    Group.objects.filter(name__in=set(current_groups) - set(target_groups)).delete()

    # stworzenie brakujacych koszykow jednoelementowych
    single_group_baskets = Basket.objects.annotate(group_count=Count("groups")).filter(
        group_count=1
    )

    for group in Group.objects.all():
        # Sprawdzamy, czy którykolwiek z koszyków jednoelementowych zawiera tę grupę
        basket_for_group = single_group_baskets.filter(groups=group).first()

        if not basket_for_group:
            # Jeśli nie istnieje koszyk jednoelementowy dla tej grupy, tworzymy nowy
            basket = Basket.objects.create(name=f"{group.name}")
            basket.groups.add(group)

    context = {
        "lista_dodanych": lista_dodanych,
        "lista_dodanych_need": lista_dodanych_need,
        "lista_dodanych_grup": lista_dodanych_grup,
        "lista_dodanych_rada": lista_dodanych_rada,
    }
    context.update(common_context(request))
    return render(request, "general/odtworz_stale.html", context)
