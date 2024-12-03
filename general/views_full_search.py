from django.db.models import Q
from contracts.models import Contracts, LogContract
from ideas.models import Ideas, LogIdea
from needs.models import Needs, LogNeed
from purchases.models import Purchases, Postepowania, LogPurchase
from general.models import Note

from django.contrib.contenttypes.models import ContentType


def full_search(slowo):
    slowo = slowo.strip()
    # Utworzenie zapytań Q dla poszukiwanego słowa w tekstowych polach każdego modelu
    if len(slowo) < 3:
        return [], [], [], []

    try:
        id_slowo = int(slowo)
    except ValueError:
        id_slowo = None

    text_fields_contracts = (
        Q(subject__icontains=slowo)
        | Q(kontrahent__icontains=slowo)
        | Q(numer_umowy__icontains=slowo)
        | Q(zakres__icontains=slowo)
        | Q(przedmiot_kolejnej_umowy__icontains=slowo)
        | Q(komentarz__icontains=slowo)
        | Q(koordynator__username__icontains=slowo)
        | Q(nr_ezz__icontains=slowo)
        | Q(section__short_name__icontains=slowo)
    )

    if id_slowo is not None:
        text_fields_contracts |= Q(id=id_slowo)

    text_fields_ideas = (
        Q(subject__icontains=slowo)
        | Q(opis__icontains=slowo)
        | Q(uzasadnienie__icontains=slowo)
        | Q(produkty__icontains=slowo)
        | Q(komentarz_akceptujacego__icontains=slowo)
        | Q(komentarz__icontains=slowo)
        | Q(section__short_name__icontains=slowo)
        | Q(osoba_prowadzaca__username__icontains=slowo)
    )

    if id_slowo is not None:
        text_fields_ideas |= Q(id=id_slowo)

    text_fields_needs = (
        Q(subject__icontains=slowo)
        | Q(opis__icontains=slowo)
        | Q(uzasadnienie__icontains=slowo)
        | Q(komentarz_akceptujacego__icontains=slowo)
        | Q(komentarz__icontains=slowo)
        | Q(komentarz_infrastrukturalny__icontains=slowo)
        | Q(komentarz_sieciowy__icontains=slowo)
        | Q(komentarz_uslugowy__icontains=slowo)
        | Q(komentarz_finansowy__icontains=slowo)
        | Q(section__short_name__icontains=slowo)
        | Q(osoba_prowadzaca__username__icontains=slowo)
    )

    if id_slowo is not None:
        text_fields_needs |= Q(id=id_slowo)

    text_fields_purchases = (
        Q(przedmiot_zakupu__icontains=slowo)
        | Q(uzasadnienie_zakupu__icontains=slowo)
        | Q(zakres_zakupu__icontains=slowo)
        | Q(cel_i_produkty__icontains=slowo)
        | Q(komentarz__icontains=slowo)
        | Q(komentarz_akceptujacego__icontains=slowo)
        | Q(id_sap__icontains=slowo)
        | Q(osoba_prowadzaca__username__icontains=slowo)
        | Q(section__short_name__icontains=slowo)
    )

    if id_slowo is not None:
        text_fields_purchases |= Q(id=id_slowo)

    # Pobranie list wynikowych na podstawie zapytań
    contract_list = list(Contracts.objects.filter(text_fields_contracts))
    ideas = list(Ideas.objects.filter(text_fields_ideas))
    need_list = list(Needs.objects.filter(text_fields_needs))
    purchase_list = list(Purchases.objects.filter(text_fields_purchases))

    # dolozenie logow
    query = (
        Q(log__akcja__icontains=slowo)
        | Q(log__user__username__icontains=slowo)
        | Q(log__user__first_name__icontains=slowo)
        | Q(log__user__last_name__icontains=slowo)
        | Q(log__user__email__icontains=slowo)
    )

    contract_log_list = Contracts.objects.filter(query).distinct()
    contract_list.extend(contract_log_list)

    idea_log_list = Ideas.objects.filter(query).distinct()
    ideas.extend(idea_log_list)

    need_log_list = Needs.objects.filter(query).distinct()
    need_list.extend(need_log_list)

    purchase_log_list = Purchases.objects.filter(query).distinct()
    purchase_list.extend(purchase_log_list)

    # dolozenie EZZ

    query = (
        Q(ezz__EZZ_number__icontains=slowo)
        | Q(ezz__ordering_person__icontains=slowo)
        | Q(ezz__subject__icontains=slowo)
        | Q(ezz__status__icontains=slowo)
        | Q(ezz__suplier__icontains=slowo)
        | Q(ezz__source_of_financing__icontains=slowo)
        | Q(ezz__final_receiver__icontains=slowo)
        | Q(ezz__current_acceptor__icontains=slowo)
    )

    purchase_log_list = Purchases.objects.filter(query).distinct()
    purchase_list.extend(purchase_log_list)

    # dolozenie postepowan

    postepowania_query = (
        Q(numer_SRM_SAP__icontains=slowo)
        | Q(numer_ZZ__icontains=slowo)
        | Q(opis_zapotrzebowania__icontains=slowo)
        | Q(priorytet__icontains=slowo)
        | Q(status_SRM__icontains=slowo)
        | Q(zlecajacy__icontains=slowo)
        | Q(kupiec__icontains=slowo)
        | Q(status_biura__icontains=slowo)
    )

    matched_postepowania = Postepowania.objects.filter(postepowania_query)

    numer_zz_list = matched_postepowania.values_list("numer_ZZ", flat=True)

    # Zapytanie do modelu Purchases, które filtruje na podstawie numeru ZZ z EZZ, odpowiadającego numerowi ZZ z postępowań
    purchase_log_list = Purchases.objects.filter(
        ezz__EZZ_number__in=numer_zz_list
    ).distinct()

    purchase_list.extend(purchase_log_list)

    # Pobranie wszystkich notatek zawierających slowo w polu content
    notes_with_slowo = Note.objects.filter(content__icontains=slowo)

    # Pobranie ContentType dla każdego z modeli
    purchase_content_type = ContentType.objects.get_for_model(Purchases)
    contract_content_type = ContentType.objects.get_for_model(Contracts)
    idea_content_type = ContentType.objects.get_for_model(Ideas)
    need_content_type = ContentType.objects.get_for_model(Needs)

    # Pobranie listy obiektów powiązanych z notatkami
    purchase_note_list = Purchases.objects.filter(
        id__in=notes_with_slowo.filter(content_type=purchase_content_type).values_list(
            "object_id", flat=True
        )
    )

    contracts_note_list = Contracts.objects.filter(
        id__in=notes_with_slowo.filter(content_type=contract_content_type).values_list(
            "object_id", flat=True
        )
    )

    idea_note_list = Ideas.objects.filter(
        id__in=notes_with_slowo.filter(content_type=idea_content_type).values_list(
            "object_id", flat=True
        )
    )

    need_note_list = Needs.objects.filter(
        id__in=notes_with_slowo.filter(content_type=need_content_type).values_list(
            "object_id", flat=True
        )
    )

    purchase_list.extend(purchase_note_list)
    contract_list.extend(contracts_note_list)
    need_list.extend(need_note_list)
    ideas.extend(idea_note_list)

    # wyczyszczenie duplikatow
    contract_list = list(set(contract_list))
    ideas = list(set(ideas))
    need_list = list(set(need_list))
    purchase_list = list(set(purchase_list))

    return contract_list, ideas, need_list, purchase_list


def note_tresc(slowo):
    slowo = slowo.strip()
    # Utworzenie zapytań Q dla poszukiwanego słowa w tekstowych polach każdego modelu
    if len(slowo) < 3:
        return [], [], [], []

    # Pobranie wszystkich notatek zawierających slowo w polu content
    notes_with_slowo = Note.objects.filter(content__icontains=slowo)

    # Pobranie ContentType dla każdego z modeli
    purchase_content_type = ContentType.objects.get_for_model(Purchases)
    contract_content_type = ContentType.objects.get_for_model(Contracts)
    idea_content_type = ContentType.objects.get_for_model(Ideas)
    need_content_type = ContentType.objects.get_for_model(Needs)

    # Pobranie listy obiektów powiązanych z notatkami
    purchase_note_list = Purchases.objects.filter(
        id__in=notes_with_slowo.filter(content_type=purchase_content_type).values_list(
            "object_id", flat=True
        )
    )

    contract_note_list = Contracts.objects.filter(
        id__in=notes_with_slowo.filter(content_type=contract_content_type).values_list(
            "object_id", flat=True
        )
    )

    idea_note_list = Ideas.objects.filter(
        id__in=notes_with_slowo.filter(content_type=idea_content_type).values_list(
            "object_id", flat=True
        )
    )

    need_note_list = Needs.objects.filter(
        id__in=notes_with_slowo.filter(content_type=need_content_type).values_list(
            "object_id", flat=True
        )
    )

    return contract_note_list, idea_note_list, need_note_list, purchase_note_list


def dopelnienie(krotka):
    contract_list, idea_list, need_list, purchase_list = krotka

    # Przekształcenie listy obiektów w listę identyfikatorów
    contract_ids = [contract.id for contract in contract_list]
    idea_ids = [idea.id for idea in idea_list]
    need_ids = [need.id for need in need_list]
    purchase_ids = [purchase.id for purchase in purchase_list]

    # Uzyskanie listy brakujących elementów dla Contracts
    c1 = Contracts.objects.exclude(id__in=contract_ids)

    # Uzyskanie listy brakujących elementów dla Ideas
    i1 = Ideas.objects.exclude(id__in=idea_ids)

    # Uzyskanie listy brakujących elementów dla Needs
    n1 = Needs.objects.exclude(id__in=need_ids)

    # Uzyskanie listy brakujących elementów dla Purchases
    p1 = Purchases.objects.exclude(id__in=purchase_ids)

    dopelnienie_krotki = (c1, i1, n1, p1)

    return dopelnienie_krotki


def przeciecie(krotka1, krotka2):
    contract_list1, idea_list1, need_list1, purchase_list1 = krotka1
    contract_list2, idea_list2, need_list2, purchase_list2 = krotka2

    # Znajdowanie przecięcia poszczególnych list i przekształcenie na listy
    contract_list_intersection = list(set(contract_list1).intersection(contract_list2))
    idea_list_intersection = list(set(idea_list1).intersection(idea_list2))
    need_list_intersection = list(set(need_list1).intersection(need_list2))
    purchase_list_intersection = list(set(purchase_list1).intersection(purchase_list2))

    return (
        contract_list_intersection,
        idea_list_intersection,
        need_list_intersection,
        purchase_list_intersection,
    )


# def przeciecie(krotka1, krotka2):
#     return tuple(set(a).intersection(b) for a, b in zip(krotka1, krotka2))


def suma(krotka1, krotka2):
    return tuple(a + b for a, b in zip(krotka1, krotka2))


def owner(slowo):
    slowo = slowo.strip()
    # Utworzenie zapytań Q dla poszukiwanego słowa w tekstowych polach każdego modelu
    if len(slowo) < 3:
        return [], [], [], []
    text_fields_contracts = Q(koordynator__username__icontains=slowo) | Q(
        section__short_name__icontains=slowo
    )
    text_fields_ideas = Q(section__short_name__icontains=slowo) | Q(
        osoba_prowadzaca__username__icontains=slowo
    )
    text_fields_needs = Q(section__short_name__icontains=slowo) | Q(
        osoba_prowadzaca__username__icontains=slowo
    )
    text_fields_purchases = Q(osoba_prowadzaca__username__icontains=slowo) | Q(
        section__short_name__icontains=slowo
    )

    # Pobranie list wynikowych na podstawie zapytań
    contract_list = list(Contracts.objects.filter(text_fields_contracts))
    ideas = list(Ideas.objects.filter(text_fields_ideas))
    need_list = list(Needs.objects.filter(text_fields_needs))
    purchase_list = list(Purchases.objects.filter(text_fields_purchases))

    return contract_list, ideas, need_list, purchase_list
