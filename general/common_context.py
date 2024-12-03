import logging
from general.parametry import get_param_int
from general.models import Variable, Clients

logger = logging.getLogger("avantic")


def common_context(request):
    context = {}
    user = request.user

    # Inicjalizacja grup uprawnień w postaci słownika
    permissions = {
        "is_recommender": False,
        "is_user_admin": False,
        "is_lead_maker": False,
        "is_contract_allocator": False,
        "is_contract_editor": False,
        "is_contract_viewer": False,
        "is_client": False,
        "is_idea_allocator": False,
        "is_idea_editor": False,
        "is_idea_viewer": False,
        "is_need_maker": False,
        "is_idea_acceptor": False,
        "is_idea_recommender": False,
        "is_superuser": False,
        "is_need_allocator": False,
        "is_need_editor": False,
        "is_need_viewer": False,
        "is_need_acceptor": False,
        "is_need_recommender": False,
        "is_need_infra_acceptor": False,
        "is_need_net_acceptor": False,
        "is_need_finanse_acceptor": False,
        "is_need_service_acceptor": False,
        "is_purchase_allocator": False,
        "is_purchase_editor": False,
        "is_purchase_viewer": False,
        "is_purchase_acceptor": False,
        "is_purchase_recommender": False,
        "is_advanced": False,
        "is_accountant": False,
        "is_dataadmin": False,
    }

    # Sprawdzanie grup użytkownika
    if user.is_authenticated:
        user_groups = set(user.groups.values_list("name", flat=True))

        # Mapowanie grup użytkownika na uprawnienia
        group_permission_map = {
            "idea_recommender": "is_idea_recommender",
            "need_recommender": "is_need_recommender",
            "useradmin": "is_user_admin",
            "lead_maker": "is_lead_maker",
            "contract_allocator": "is_contract_allocator",
            "contract_editor": "is_contract_editor",
            "contract_viewer": "is_contract_viewer",
            "client": "is_client",
            "idea_allocator": "is_idea_allocator",
            "idea_editor": "is_idea_editor",
            "idea_viewer": "is_idea_viewer",
            "need_maker": "is_need_maker",
            "idea_acceptor": "is_idea_acceptor",
            "superuser": "is_superuser",
            "need_allocator": "is_need_allocator",
            "need_editor": "is_need_editor",
            "need_viewer": "is_need_viewer",
            "need_acceptor": "is_need_acceptor",
            "need_infra_acceptor": "is_need_infra_acceptor",
            "need_net_acceptor": "is_need_net_acceptor",
            "need_finanse_acceptor": "is_need_finanse_acceptor",
            "need_service_acceptor": "is_need_service_acceptor",
            "purchase_allocator": "is_purchase_allocator",
            "purchase_editor": "is_purchase_editor",
            "purchase_viewer": "is_purchase_viewer",
            "purchase_acceptor": "is_purchase_acceptor",
            "purchase_recommender": "is_purchase_recommender",
            "advanced": "is_advanced",
            "accountant": "is_accountant",
            "dataadmin": "is_dataadmin",
        }

        for group, permission in group_permission_map.items():
            if group in user_groups:
                permissions[permission] = True

    # Pochodne uprawnienia
    derived_permissions = [
        ("is_contract_allocator", "is_contract_editor", "is_contract_viewer"),
        (
            #   "is_lead_maker",
            "is_contract_editor",
            "is_contract_viewer",
            "is_idea_editor",
            "is_idea_viewer",
        ),
        ("is_idea_allocator", "is_idea_editor", "is_idea_viewer"),
        ("is_idea_acceptor", "is_idea_editor", "is_idea_viewer"),
        ("is_idea_recommender", "is_idea_editor", "is_idea_viewer", "is_recommender"),
        (
            "is_superuser",
            "is_idea_viewer",
            "is_need_viewer",
            "is_need_editor",
            "is_purchase_viewer",
        ),
        ("is_need_allocator", "is_need_editor", "is_need_viewer"),
        ("is_need_acceptor", "is_need_editor", "is_need_viewer"),
        ("is_need_recommender", "is_need_editor", "is_need_viewer", "is_recommender"),
        ("is_need_infra_acceptor", "is_need_editor", "is_need_viewer"),
        ("is_need_net_acceptor", "is_need_editor", "is_need_viewer"),
        ("is_need_finanse_acceptor", "is_need_editor", "is_need_viewer"),
        ("is_need_service_acceptor", "is_need_editor", "is_need_viewer"),
        ("is_purchase_allocator", "is_purchase_editor", "is_purchase_viewer"),
    ]

    for base, *others in derived_permissions:
        if permissions[base]:
            for perm in others:
                permissions[perm] = True

    # Obsługa rady
    permissions["obsluga_rady"] = (
        get_param_int("obsluga_rady_architektury", 0) == 1
        and permissions["is_recommender"]
    )
    permissions["rada_viewer"] = get_param_int(
        "obsluga_rady_architektury", 0
    ) == 1 and (permissions["is_idea_viewer"] or permissions["is_need_viewer"])
    permissions["is_any_viewer"] = (
        permissions["is_idea_viewer"]
        or permissions["is_need_viewer"]
        or permissions["is_purchase_viewer"]
        or permissions["is_contract_viewer"]
    )

    permissions["finanse_viewer"] = permissions["is_any_viewer"]
    permissions["finanse_editor"] = permissions["is_accountant"]
    permissions["finanse_importer"] = (
        permissions["is_accountant"] and permissions["is_advanced"]
    )

    status_importu_umow = Variable.get("status_importu_umow")
    permissions["dolacz_umowy"] = status_importu_umow == 1
    permissions["ustaw_dane_umowy"] = status_importu_umow == 2

    context.update(permissions)

    parametry = {}
    szerokosc = get_param_int("szerokosc", 1000)
    parametry["szerokosc"] = szerokosc
    polowka = round(szerokosc / 2) - 5
    parametry["polowka"] = polowka
    szeroka_szerokosc = round(szerokosc * 5 / 4)
    parametry["szeroka_szerokosc"] = szeroka_szerokosc
    context.update(parametry)

    # dodatkowe informacje do kontekstu
    if user.is_authenticated:
        klienci = Clients.objects.all()  # Pobierz wszystkich klientów
        clients = Clients.objects.filter(users=user)
        klienci_rel = [klient.short_name for klient in clients]
        dodatkowe = {
            "klienci": klienci,
            "klienci_rel": klienci_rel,
        }
        context.update(dodatkowe)

    wszystkie_pomysly = request.GET.get('wszystkie_pomysly')
    context.update({'wszystkie_pomysly':wszystkie_pomysly})
    return context
