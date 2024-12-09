from celery import shared_task
from django.utils import timezone
from general.models import Status_procesu, Parametry, Note
from django.db.models import Max, F, Q, DateTimeField, Subquery, OuterRef, Count
from django.db.models.functions import Coalesce, Greatest
import logging
from datetime import timedelta
from needs.models import Needs, LogNeed
from ideas.models import Ideas, LogIdea
from purchases.models import EZZ, Purchases
from general.linki import generate_contract_url
from .mail import utworz_mail_do_wyslania, wyslij_mail_do_grupy
from contracts.models import Contracts
from django.contrib.auth.models import User, Group
from general.parametry import get_param_int

logger = logging.getLogger(__name__)


def ensure_kierownictwo_group_exists():
    group_name = "kierownictwo"
    group, created = Group.objects.get_or_create(name=group_name)
    if created:
        print(f"Grupa '{group_name}' została utworzona.")


def get_max_dni_nieaktywnosci():
    """
    Pobierz maksymalną liczbę dni nieaktywności dla zakupów z parametru w bazie danych.
    Jeśli parametr nie istnieje, utwórz go z domyślną wartością 70.

    :return: int: Maksymalna liczba dni nieaktywności
    """
    param = get_param_int("max_dni_nieaktywnosci_zakupu", 100)
    return param


def zakupy_do_podjecia_det():
    """
    Identyfikacja zakupów, które są oznaczone jako niezakończone i co do których przez długi czas nie było żadnej aktywności.
    Wysłanie notyfikacji do właściciela zakupu.
    """
    from general.linki import generate_purchase_url
    from .mail import utworz_mail_do_wyslania

    logger.info("Pobieranie zakupów do podjęcia")

    try:
        max_dni_nieaktywnosci = get_max_dni_nieaktywnosci()

        status_purchases_zakonczony = Status_procesu.objects.get(status="zakończony")
        status_purchases_anulowany = Status_procesu.objects.get(status="anulowany")

        reference_date = timezone.now() - timezone.timedelta(days=max_dni_nieaktywnosci)

        purchases = (
            Purchases.objects.annotate(
                max_log_date=Max("log__data"),
                max_note_date=Max("notes__timestamp"),
                latest_date=Greatest(
                    F("data_utworzenia"),
                    Max("log__data"),
                    Max("notes__timestamp"),
                    output_field=DateTimeField(),
                ),
            )
            .filter(
                ~Q(status_procesu=status_purchases_zakonczony),
                ~Q(status_procesu=status_purchases_anulowany),
                Q(latest_date__lte=reference_date),
            )
            .distinct()
        )

        for purchase in purchases:
            najpozniejszy_log = purchase.log.order_by("-data").first()
            najpozniejsza_notatka = purchase.notes.order_by("-timestamp").first()

            przedmiot_zakupu_skrocony = purchase.przedmiot_zakupu[:40]

            print(
                f"ID: {purchase.id}",
                f"Latest date: {purchase.latest_date}",
                f"Przedmiot zakupu: {przedmiot_zakupu_skrocony}",
                f"Osoba prowadząca: {purchase.osoba_prowadzaca}",
                f"Section: {purchase.section}",
                f"Tresc najpozniejszego logu: {najpozniejszy_log.akcja if najpozniejszy_log else 'Brak logów'}",
                f"Tresc najpozniejszej notatki: {najpozniejsza_notatka.content if najpozniejsza_notatka else 'Brak notatek'}",
                f"Status procesu: {purchase.status_procesu}",
                f"Status akceptacji: {purchase.status_akceptacji}",
            )

            tresc = f"Dzień dobry,\n\
Zakup numer {purchase.id} wymaga Twojej uwagi ponieważ jego status wskazuje na to, że jest niezakończony, a już dawno nie było żadnej zmiany statusu ani notatki\n\n\
Przedmiot zakupu: {purchase.przedmiot_zakupu} \n\n\
Osoba prowadząca: {purchase.osoba_prowadzaca}\n\n\
Dział: {purchase.section}\n\n\
Treść najpóźniejszego logu: {najpozniejszy_log.akcja if najpozniejszy_log else 'Brak logów'}\n\n\
Treść najpóźniejszej notatki: {najpozniejsza_notatka.content if najpozniejsza_notatka else 'Brak notatek'}\n\n\
Status procesu: {purchase.status_procesu}\n\n\
Status akceptacji: {purchase.status_akceptacji}\n\n\n\
Dostosuj status procesu zgodnie z poniższymi regułami:\n\n\
roboczy- przed uzyskaniem akceptacji dyrektora Biura w systemie Aprobo i skierowaniem wniosku w systemie EZZ do procesu akceptacyjnego \n\n\
w EZZ - od uzyskania akceptacji dyrektora Biura i skierowaniu wniosku w systemie EZZ do procesu akceptacyjnego\n\n\
w zakupach (zakup standardowy) - od uzyskania w systemie EZZ statusu: Zarejestrowany w SRM/SAP CP \n\n\
zakup BGNIG - od uzyskania w systemie EZZ statusu: Zarejestrowany w SRM/SAP CP  (status wybierany jedynie w sytuacji kiedy z jakichkolwiek powodów Biuro Zakupów nie zajmuje się procedowaniem przedmiotowego zakupu) \n\n\
w realizacji - od momentu podpisania umowy/zamówienia przez wszystkie strony (jedynie w przypadku zakupu dotyczącego dostawy sprzętu, licencji, wykonania oprogramowania) \n\n\
zakończony - dla zamówień, dla których występuje faza realizacji od momentu odbioru produktów umowy/zamówienia. Dla innych zamówień/umów od momentu podpisania zamówienia/umowy przez wszystkie strony \n\n\
anulowany - w sytuacji, w której zaniechano realizacji Zakupu \n\n\n\
Jeżeli Zakup nie wymaga zmiany statusu pomimo upływu czasu dodaj notatkę opisującą aktualny status Zakupu\n"
            tresc += generate_purchase_url(purchase.id)
            temat = f"Zakup numer {purchase.id} wymaga uwagi"

            utworz_mail_do_wyslania(purchase.osoba_prowadzaca, temat, tresc)

    except Status_procesu.DoesNotExist:
        logger.error("Nie znaleziono statusu: zakończony lub anulowany")
    except Exception as e:
        logger.error(f"Wystąpił błąd podczas przetwarzania zakupów: {e}")


@shared_task
def zakupy_do_podjecia():
    """
    Zadanie Celery, które wywołuje funkcję `zakupy_do_podjecia_det` w celu identyfikacji zakupów do podjęcia.
    """
    zakupy_do_podjecia_det()


def potrzeby_do_podjecia_det():
    """
    Identyfikacja potrzeb, które są oznaczone jako realizowane,
    a które nie mają żadnych powiązanych zakupów lub wszystkie powiązane zakupy są zakończone lub anulowane,
    oraz co do których przez długi czas nie było żadnej aktywności.
    """
    from general.linki import generate_need_url
    from .mail import utworz_mail_do_wyslania

    max_days = get_param_int("max_dni_nieaktywnosci_potrzeby", 100)
    cutoff_date = timezone.now() - timedelta(days=max_days)

    last_log_date = (
        LogNeed.objects.filter(needs=OuterRef("pk"))
        .order_by("-data")
        .values("data")[:1]
    )
    last_log_action = (
        LogNeed.objects.filter(needs=OuterRef("pk"))
        .order_by("-data")
        .values("akcja")[:1]
    )
    last_note_date = (
        Note.objects.filter(object_id=OuterRef("pk"), content_type__model="needs")
        .order_by("-timestamp")
        .values("timestamp")[:1]
    )
    last_note_content = (
        Note.objects.filter(object_id=OuterRef("pk"), content_type__model="needs")
        .order_by("-timestamp")
        .values("content")[:1]
    )

    needs_to_be_addressed = (
        Needs.objects.annotate(
            last_log_activity=Subquery(last_log_date),
            last_log_action=Subquery(last_log_action),
            last_note_activity=Subquery(last_note_date),
            last_note_content=Subquery(last_note_content),
            last_activity=Greatest(
                Coalesce(Max("log__data"), timezone.make_aware(timezone.datetime.min)),
                Coalesce(
                    Max("notes__timestamp"), timezone.make_aware(timezone.datetime.min)
                ),
                "data_utworzenia",
            ),
        )
        .filter(last_activity__lt=cutoff_date, status_potrzeby__status="realizowana")
        .filter(
            Q(purchases__isnull=True)
            | Q(purchases__status_procesu__status__in=["zakończony", "anulowany"])
        )
        .distinct()
    )

    for need in needs_to_be_addressed:
        print(
            f"Potrzeba {need.id} wymaga podjęcia działań. "
            f"Ostatni log: {need.last_log_action or 'Brak danych'} (Data: {need.last_log_activity or 'Brak danych'}), "
            f"Ostatnia notatka: {need.last_note_content or 'Brak danych'} (Data: {need.last_note_activity or 'Brak danych'})."
        )

        tresc = f"Dzień dobry,\n\
Potrzeba numer {need.id} wymaga Twojej uwagi ponieważ jej status wskazuje na to, że jest niezakończona, a albo nie ma powiązanego żadnego Zakupu \
albo wszystkie powiązane Zakupy mają status anulowany bądź zakończony.\n\n\
Jeżeli do tej Potrzeby nie będzie już na pewno powiązanych żadnych Zakupów zakończ Potrzebę.\n\n\
Jeżeli będą kolejne Zakupu to albo stwórz teraz powiązany Zakup a jeżeli jest to niemożliwe to wstaw notatkę, w której wyjaśnisz przyczyny trwania w aktualnym stanie.\n\n\
Przedmiot potrzeby: {need.subject} \n\n\
Status Potrzeby: {need.status_potrzeby} \n\n\
Status akceptacji:    {need.status_akceptacji} \n\n\
Dział:    {need.section} \n\n\
Koordynator IT:    {need.osoba_prowadzaca} \n\n"
        tresc += generate_need_url(need.id)
        temat = f"Potrzeba numer {need.id} wymaga uwagi"
        utworz_mail_do_wyslania(need.osoba_prowadzaca, temat, tresc)


@shared_task
def potrzeby_do_podjecia():
    """
    Zadanie Celery, które wywołuje funkcję `potrzeby_do_podjecia_det` w celu identyfikacji potrzeb do podjęcia.
    """
    potrzeby_do_podjecia_det()


def pomysly_do_podjecia_det():
    """
    Identyfikacja pomysłów, które są oznaczone jako realizowane,
    a które nie mają żadnych powiązanych potrzeb lub wszystkie powiązane potrzeby są zakończone lub anulowane,
    oraz co do których przez długi czas nie było żadnej aktywności.
    Wysłanie notyfikacji do właściciela.
    """
    from general.linki import generate_idea_url
    from .mail import utworz_mail_do_wyslania

    max_days = get_param_int("max_dni_nieaktywnosci_pomyslu", 100)
    cutoff_date = timezone.now() - timedelta(days=max_days)

    last_log_date = (
        LogIdea.objects.filter(ideas=OuterRef("pk"))
        .order_by("-data")
        .values("data")[:1]
    )
    last_log_action = (
        LogIdea.objects.filter(ideas=OuterRef("pk"))
        .order_by("-data")
        .values("akcja")[:1]
    )
    last_note_date = (
        Note.objects.filter(object_id=OuterRef("pk"), content_type__model="ideas")
        .order_by("-timestamp")
        .values("timestamp")[:1]
    )
    last_note_content = (
        Note.objects.filter(object_id=OuterRef("pk"), content_type__model="ideas")
        .order_by("-timestamp")
        .values("content")[:1]
    )

    ideas_to_be_addressed = (
        Ideas.objects.annotate(
            last_log_activity=Subquery(last_log_date),
            last_log_action=Subquery(last_log_action),
            last_note_activity=Subquery(last_note_date),
            last_note_content=Subquery(last_note_content),
            last_activity=Greatest(
                Coalesce(Max("log__data"), timezone.make_aware(timezone.datetime.min)),
                Coalesce(
                    Max("notes__timestamp"), timezone.make_aware(timezone.datetime.min)
                ),
                "data_utworzenia",
            ),
        )
        .filter(last_activity__lt=cutoff_date, status_idei__status="realizowana")
        .filter(
            Q(needs__isnull=True)
            | Q(needs__status_potrzeby__status__in=["zrealizowana", "zamknięta"])
        )
        .distinct()
    )

    for idea in ideas_to_be_addressed:
        print(
            f"Pomysł {idea.id} wymaga podjęcia działań. "
            f"Ostatni log: {idea.last_log_action or 'Brak danych'} (Data: {idea.last_log_activity or 'Brak danych'}), "
            f"Ostatnia notatka: {idea.last_note_content or 'Brak danych'} (Data: {idea.last_note_activity or 'Brak danych'})."
        )

        tresc = f"Dzień dobry,\n\
Pomysł numer {idea.id} wymaga Twojej uwagi ponieważ jego status wskazuje na to, że jest niezakończony, a albo nie ma powiązanej żadnej Potrzeby \
albo wszystkie powiązane Potrzeby mają status anulowany bądź zakończony.\n\n\
Jeżeli do tego Pomysłu nie będzie już na pewno powiązanych żadnych Potrzeb zakończ Pomysł.\n\n\
Jeżeli będą kolejne Potrzeby to albo stwórz teraz powiązaną Potrzebę a jeżeli jest to niemożliwe to wstaw notatkę, w której wyjaśnisz przyczyny trwania w aktualnym stanie.\n\n\
Przedmiot pomysłu: {idea.subject} \n\n\
Status Pomysłu: {idea.status_idei} \n\n\
Status akceptacji:    {idea.status_akceptacji} \n\n\
Dział:    {idea.section} \n\n\
Koordynator IT:    {idea.osoba_prowadzaca} \n\n"
        tresc += generate_idea_url(idea.id)
        temat = f"Pomysł numer {idea.id} wymaga uwagi"
        utworz_mail_do_wyslania(idea.osoba_prowadzaca, temat, tresc)


@shared_task
def pomysly_do_podjecia():
    """
    Zadanie Celery, które wywołuje funkcję `pomysly_do_podjecia_det` w celu identyfikacji pomysłów do podjęcia.
    """
    pomysly_do_podjecia_det()


def umowy_bez_statusu_det():
    """
    Identyfikacja umów, które nie mają ustawionego pola `czy_obsługiwana`.
    Wysłanie notyfikacji do właściciela.
    """
    try:
        contracts = Contracts.objects.filter(
            koordynator__isnull=False, obslugiwana__isnull=True
        ).distinct()

        for contract in contracts:
            koordynator = contract.koordynator
            if isinstance(koordynator, User):
                print(
                    f"Umowa {contract.id} wymaga podjęcia działań. "
                    f"Koordynator: {koordynator}, "
                    f"Przedmiot: {contract.subject}, "
                    f"Numer umowy: {contract.numer_umowy}"
                )

                tresc = f"Dzień dobry,\n\
Umowa numer {contract.id} wymaga Twojej uwagi ponieważ jej pole `czy umowa jest obsługiwana` nie jest ustawione.\n\n\
Przedmiot umowy: {contract.subject} \n\n\
Numer umowy: {contract.numer_umowy} \n\n\
Koordynator: {koordynator.get_full_name()} \n\n\
Sekcja: {contract.section} \n\n\
Zakres: {contract.zakres} \n\n\
Wartość: {contract.wartosc} {contract.waluta} \n\n\
Komentarz: {contract.komentarz} \n\n\n\
Należy wybrać Tak jeżeli zachodzi co najmniej jedna z poniższych przesłanek:\n\n\
- zamówienie dotyczy realizacji usług, które jeszcze nie zostały zakończone\n\n\
- zamówienie dotyczy realizacji usług zakończonych ale istnieje potrzeba ich kontynuacji a jeszcze nie został stworzony nowy Pomysł, który zaadresuje wymaganie kontunuacji.\n\n\
- zamówienie dotyczy zakupu środków trwałych lub WNIP, co do których świadczona jest aktualnie usługa gwarancji/wsparcia\n\n\
- zamówienie dotyczy zakupu środków trwałych lub WNIP, dla których należy teraz lub w przyszłości zakupić usługę gwarancji/wsparcia (lub dokonać zakupu odtworzeniowego), a jeszcze nie został stworzony nowy Pomysł\n\n\n"

                tresc += generate_contract_url(contract.id)
                temat = f"Umowa numer {contract.id} wymaga uwagi"
                utworz_mail_do_wyslania(koordynator, temat, tresc)
            else:
                logger.error(
                    f"Koordynator for contract {contract.id} is not a User instance."
                )

    except Exception as e:
        logger.error(f"Wystąpił błąd podczas przetwarzania umów: {e}")


@shared_task
def umowy_bez_statusu():
    """
    Zadanie Celery, które wywołuje funkcję `umowy_bez_statusu_det` w celu identyfikacji umów bez statusu.
    """
    umowy_bez_statusu_det()


def umowy_czy_kontynuowac_det():
    """
    Identyfikacja umów, które nie mają ustawionego pola `czy_kontynuować`.
    Wysłanie notyfikacji do właściciela.
    """
    try:
        contracts = Contracts.objects.filter(
            koordynator__isnull=False,
            obslugiwana__isnull=False,
            czy_wymagana_kontynuacja__isnull=True,
            obslugiwana=True,
        ).distinct()

        for contract in contracts:
            koordynator = contract.koordynator
            if isinstance(koordynator, User):
                print(
                    f"Umowa {contract.id} wymaga podjęcia działań. "
                    f"Koordynator: {koordynator}, "
                    f"Przedmiot: {contract.subject}, "
                    f"Numer umowy: {contract.numer_umowy}"
                )

                tresc = f"Dzień dobry,\n\
Umowa numer {contract.id} wymaga Twojej uwagi ponieważ jej pole `czy umowa wymaga kontynuacji` nie jest ustawione.\n\n\
Przedmiot umowy: {contract.subject} \n\n\
Numer umowy: {contract.numer_umowy} \n\n\
Koordynator: {koordynator.get_full_name()} \n\n\
Sekcja: {contract.section} \n\n\
Zakres: {contract.zakres} \n\n\
Wartość: {contract.wartosc} {contract.waluta} \n\n\
Komentarz: {contract.komentarz} \n\n\n\
Umowa wymaga kontynuacji jeżeli po zakończeniu usługi świadczonej w ramach umowu/zamówienia niezbędne będzie zamówienie usługi/subskrypcji lub zakupienie nowego sprzętu lub licencji.\n\n\
Status umowy, która została sklasyfikowana jako wymagająca kontynuacji można zmienić na niewymaga kontynuacji jeżeli został stworzony i zrealzowany Pomysł(y) na kontynuację (np. usług).\n\n"

                tresc += generate_contract_url(contract.id)
                temat = f"Umowa numer {contract.id} wymaga uwagi"
                utworz_mail_do_wyslania(koordynator, temat, tresc)
            else:
                logger.error(
                    f"Koordynator for contract {contract.id} is not a User instance."
                )

    except Exception as e:
        logger.error(f"Wystąpił błąd podczas przetwarzania umów: {e}")


@shared_task
def umowy_czy_kontynuowac():
    """
    Zadanie Celery, które wywołuje funkcję `umowy_czy_kontynuowac_det` w celu identyfikacji umów, które wymagają decyzji o kontynuacji.
    """
    umowy_czy_kontynuowac_det()


def umowy_brak_wlasciciela_det():
    """
    Identyfikacja umów, które nie mają ustawionego właściciela.
    Wysłanie notyfikacji do kierownictwa (allocators).
    """
    try:
        contracts = Contracts.objects.filter(
            section__isnull=True,
        ).distinct()

        for contract in contracts:
            tresc = f"Dzień dobry,\n\
Umowa numer {contract.id} wymaga Twojej uwagi ponieważ nie jest przypisana do żadnego działu.\n\n\
Przedmiot umowy: {contract.subject} \n\n\
Numer umowy: {contract.numer_umowy} \n\n\
Zakres: {contract.zakres} \n\n\
Wartość: {contract.wartosc} {contract.waluta} \n\n\
Komentarz: {contract.komentarz} \n\n\n\
Przypisz umowę do właściwego działu.\n\n"

            tresc += generate_contract_url(contract.id)
            temat = f"Umowa numer {contract.id} wymaga uwagi"
            wyslij_mail_do_grupy("contract_allocator", temat, tresc)

    except Exception as e:
        logger.error(f"Wystąpił błąd podczas przetwarzania umów: {e}")


@shared_task
def umowy_brak_wlasciciela():
    """
    Zadanie Celery, które wywołuje funkcję `umowy_brak_wlasciciela_det` w celu identyfikacji umów bez właściciela.
    """
    umowy_brak_wlasciciela_det()


def umowy_jak_kontynuowac_det():
    """
    Identyfikacja umów, które powinny mieć zdefiniowane pomysły, a ich nie mają.
    Wysłanie notyfikacji do właściciela.
    """
    try:
        contracts = (
            Contracts.objects.filter(
                koordynator__isnull=False,
                obslugiwana__isnull=False,
                czy_wymagana_kontynuacja__isnull=False,
                wymagana_data_zawarcia_kolejnej_umowy__isnull=False,
                czy_wymagana_kontynuacja=True,
                obslugiwana=True,
            )
            .annotate(ideas_count=Count("ideas"))
            .filter(ideas_count=0)
            .distinct()
        )

        for contract in contracts:
            koordynator = contract.koordynator
            if isinstance(koordynator, User):
                print(
                    f"Umowa {contract.id} wymaga podjęcia działań. "
                    f"Koordynator: {koordynator}, "
                    f"Przedmiot: {contract.subject}, "
                    f"Numer umowy: {contract.numer_umowy}"
                )

                tresc = f"Dzień dobry,\n\
Umowa numer {contract.id} wymaga Twojej uwagi ponieważ nie posiada zdefiniowanych pomysłów na kontynuację przedmiotu umowy.\n\n\
Przedmiot umowy: {contract.subject} \n\n\
Numer umowy: {contract.numer_umowy} \n\n\
Koordynator: {koordynator.get_full_name()} \n\n\
Sekcja: {contract.section} \n\n\
Zakres: {contract.zakres} \n\n\
Wartość: {contract.wartosc} {contract.waluta} \n\n\
Komentarz: {contract.komentarz} \n\n\n\
Zdefiniuj pomysł na kontynuację zakresu umowy.\n\n"

                tresc += generate_contract_url(contract.id)
                tresc += "\n\n\nPrzedmiotem pomysłów definiowane w ramach tej umowy musi być produkt, któryu zapewni ciągłość usług po upływie terminu trwania umowy\n"
                temat = f"Umowa numer {contract.id} wymaga uwagi"
                utworz_mail_do_wyslania(koordynator, temat, tresc)
            else:
                logger.error(
                    f"Koordynator for contract {contract.id} is not a User instance."
                )

    except Exception as e:
        logger.error(f"Wystąpił błąd podczas przetwarzania umów: {e}")


@shared_task
def umowy_jak_kontynuowac():
    """
    Zadanie Celery, które wywołuje funkcję `umowy_jak_kontynuowac_det` w celu identyfikacji umów, które powinny mieć zdefiniowane pomysły.
    """
    umowy_jak_kontynuowac_det()


def umowy_kiedy_kontynuowac_det():
    """
    Identyfikacja umów, które powinny mieć zdefinowana datę kontynuacji
    Wysłanie notyfikacji do właściciela.
    """
    try:
        contracts = Contracts.objects.filter(
            koordynator__isnull=False,
            obslugiwana__isnull=False,
            czy_wymagana_kontynuacja__isnull=False,
            wymagana_data_zawarcia_kolejnej_umowy__isnull=True,
            czy_wymagana_kontynuacja=True,
            obslugiwana=True,
        ).distinct()

        for contract in contracts:
            koordynator = contract.koordynator
            if isinstance(koordynator, User):
                print(
                    f"Umowa {contract.id} wymaga podjęcia działań. "
                    f"Koordynator: {koordynator}, "
                    f"Przedmiot: {contract.subject}, "
                    f"Numer umowy: {contract.numer_umowy}"
                )

                tresc = f"Dzień dobry,\n\
Umowa numer {contract.id} wymaga Twojej uwagi ponieważ nie posiada określonej daty zawarcia umowy na kontunuację przedmiotu umowy.\n\n\
Przedmiot umowy: {contract.subject} \n\n\
Numer umowy: {contract.numer_umowy} \n\n\
Koordynator: {koordynator.get_full_name()} \n\n\
Sekcja: {contract.section} \n\n\
Zakres: {contract.zakres} \n\n\
Wartość: {contract.wartosc} {contract.waluta} \n\n\
Komentarz: {contract.komentarz} \n\n\n\
Wprowadź datę zawarcia kolejnej umowy.\n\n\
Jeżeli umowy dotyczy świadczenia usług wsparcia lub innych to należy wprowadzić datę zakończenia świadczenia takich usług w ramach umowy {contract.id}.\n\n\
W przyadku kiedy umowa dotyczy zakupu urządzeń to należy pamiętać o tym, kiedy kończy się gwarancja lub inne usługi związane ze sprzętem\n\n\
W przypadku usług subskrypcji należy uwzględnić datę zakończenia subskrypcji\n\n\
Jeżeli mamy do czynienia z sytuacją, w której widzimy konieczność zawarcia w przyszłości kilku umów, które będą konsekwencją niniejszej umowy to należy zdefiniować odpowiednią liczbę pomysłów a jako datę kolejnej umowy podac datę najwcześniejszego z nich\n\n"

                tresc += generate_contract_url(contract.id)
                temat = f"Umowa numer {contract.id} wymaga uwagi"
                utworz_mail_do_wyslania(koordynator, temat, tresc)
            else:
                logger.error(
                    f"Koordynator for contract {contract.id} is not a User instance."
                )

    except Exception as e:
        logger.error(f"Wystąpił błąd podczas przetwarzania umów: {e}")


@shared_task
def umowy_kiedy_kontynuowac():
    """
    Zadanie Celery, które wywołuje funkcję `umowy_kiedy_kontynuowac_det` w celu identyfikacji umów, które powinny mieć zdefiniowaną date kontynuacji.
    """
    umowy_kiedy_kontynuowac_det()


def normalize(name):
    """
    Function to normalize names, for example, removing diacritics or converting to lowercase.
    """
    return name.lower()


def nielegalne_ezz_det(ezz_number=None, ordering_person=None, subject=None):
    """
    Identyfikacja EZZ, które zostały wprowadzone do systemu bez wymaganych zgód wewnątrz Biura.
    Wysłanie notyfikacji do właściciela.
    """
    try:
        #       queryset = EZZ.objects.all()
        queryset = EZZ.objects.filter(nieistotny=False)
        # Filtry wstępne
        if ezz_number:
            queryset = queryset.filter(EZZ_number=ezz_number)
        if ordering_person:
            queryset = queryset.filter(ordering_person=ordering_person)
        if subject:
            queryset = queryset.filter(subject=subject)

        # Wykluczenie rekordów o określonych statusach w polu 'subject'
        excluded_statuses = ["Anulowany", "Roboczy", "Cofnięty do Zlecającego"]
        queryset = queryset.exclude(status__in=excluded_statuses)

        # Sprawdzenie, czy EZZ jest powiązany z zakupami
        queryset = queryset.filter(Q(purchases__isnull=True)).distinct()

        for purchase in queryset:
            ordering_person_name = purchase.ordering_person
            if ordering_person_name:
                print(
                    f"EZZ {purchase.EZZ_number} wymaga podjęcia działań. "
                    f"Zlecający: {ordering_person_name}, "
                    f"Przedmiot: {purchase.subject}, "
                    f"Numer umowy: {purchase.EZZ_number}"
                )

                last_name = ordering_person_name.split(" ")[-1]
                normalized_last_name = normalize(last_name)

                # Wyszukiwanie koordynatora po nazwisku
                matching_users = User.objects.filter(
                    last_name__icontains=normalized_last_name
                )

                if matching_users.exists():
                    koordynator = matching_users.first()
                    print(f"Przypisany koordynator: {koordynator.username}")

                    tresc = f"Dzień dobry,\n\
EZZ numer {purchase.EZZ_number} wymaga Twojej uwagi ponieważ nie został powiązany z żadnym Zakupem (Potrzebą)\n\n\
Przedmiot EZZ: {purchase.subject} \n\n\
Numer EZZ: {purchase.EZZ_number} \n\n\
Zlecający: {ordering_person_name} \n\n\
Dostawca: {purchase.suplier} \n\n\
Źródło finansowania: {purchase.source_of_financing} \n\n\
Odbiorca końcowy: {purchase.final_receiver} \n\n\
Data ostatniej akceptacji: {purchase.date_of_last_acceptance} \n\n\
Status: {purchase.status} \n\n"
                    tresc += "\nUzupełnij w Aprobo właściwe procesy decyzyjne\n"
                    #        print(tresc)
                    temat = f"EZZ numer {purchase.EZZ_number} wymaga uwagi"

                    # Wysłanie maila do koordynatora
                    utworz_mail_do_wyslania(koordynator, temat, tresc)
                else:
                    logger.error(
                        f"No User found with last name {last_name} (normalized: {normalized_last_name}) for EZZ number {purchase.EZZ_number}"
                    )
            else:
                logger.error(
                    f"Ordering person for purchase {purchase.EZZ_number} is not specified."
                )

    except Exception as e:
        logger.error(f"Wystąpił błąd podczas przetwarzania EZZ: {e}")


@shared_task
def nielegalne_ezz():
    """
    Zadanie Celery, które wywołuje funkcję `nielegalne_ezz_det` w celu identyfikacji ezz, które zostały poszczone w  obieg akceptacyjny bez wymaganych zgód wewnątrz Biura.
    """
    nielegalne_ezz_det()


def raport_ciaglosci_serwisow_det(ezz_number=None, ordering_person=None, subject=None):
    """
    Sporządzenie raportu ciągłości serwisów i wysłanie.
    """
    from general.raporty_jakosci import ensure_kierownictwo_group_exists

    max_days = get_param_int("max_dni_na_odnowienie", 100)
    cutoff_date = timezone.now() + timedelta(days=max_days)
    try:
        contracts = Contracts.objects.filter(
            obslugiwana__isnull=False,
            czy_wymagana_kontynuacja__isnull=False,
            wymagana_data_zawarcia_kolejnej_umowy__isnull=False,
            czy_wymagana_kontynuacja=True,
            obslugiwana=True,
            wymagana_data_zawarcia_kolejnej_umowy__lt=cutoff_date,
        ).order_by("wymagana_data_zawarcia_kolejnej_umowy")

        tresc = f"Lista serwisów wygasających w ciągu najbliższych {max_days} dni:\n\n"
        for contract in contracts:
            tresc += f"{contract.wymagana_data_zawarcia_kolejnej_umowy}\t"
            tresc += f"({contract.id})"
            tresc += f" {contract.section} "
            tresc += f" {contract.koordynator} "
            tresc += f" {contract.subject} "
            tresc += generate_contract_url(contract.id)
            ideas_count = contract.ideas.count()
            if ideas_count == 0:
                tresc += f" - Brak Pomysłów !!!\n"
            else:
                tresc += f"\n\tPomysły ({ideas_count}):\n"
                for idea in contract.ideas.all():
                    tresc += f"\t- {idea.id}: {idea.subject}\n"
                    needs_count = idea.needs.count()
                    if needs_count == 0:
                        tresc += f"\t\tBrak Potrzeb !!!\n"
                    else:
                        tresc += f"\t\tPotrzeby ({needs_count}):\n"
                    for need in idea.needs.all():
                        tresc += f"\t\t- {need.id}: {need.subject}\n"

                        purchases_count = need.purchases.count()
                        if purchases_count == 0:
                            tresc += f"\t\t\tBrak Zakupów !!!\n"
                        else:
                            tresc += f"\t\t\tZakupy ({purchases_count}):\n"
                            for purchase in need.purchases.all():
                                tresc += f"\t\t\t- {purchase.id}: {purchase.przedmiot_zakupu}\t"
                                tresc += f"{purchase.status_procesu}\t"
                                tresc += f"{purchase.ezz}\t"

                                tresc += "\n"

            tresc += "\n"

        ensure_kierownictwo_group_exists()
        wyslij_mail_do_grupy("kierownictwo", "raport ciągłości usług", tresc)
    except Exception as e:
        logger.error(f"Wystąpił błąd podczas przetwarzania umów: {e}")


@shared_task
def raport_ciaglosci_serwisow():
    """
    Zadanie Celery, które wywołuje funkcję `raport_ciaglosci_serwisow_det` w celu sporządzeni i wysłania raportu ciąglości serwisów.
    """
    raport_ciaglosci_serwisow_det()


def umowy_zabezpieczone_det():
    """
    Identyfikacja umów, które prawdopodobnie zostały już obsłużone w zakresie zapewnienia ciągłości usług
    """
    try:

        included_statuses = ["zamknięta", "zrealizowana"]
        excluded_statuses = ["rada architektury", "realizowana", "zawieszona", "nowa"]

        # Filtracja kontraktów zgodnie z wymaganiami
        contracts = Contracts.objects.filter(
            koordynator__isnull=False,
            obslugiwana__isnull=False,
            czy_wymagana_kontynuacja__isnull=False,
            wymagana_data_zawarcia_kolejnej_umowy__isnull=False,
            czy_wymagana_kontynuacja=True,
            obslugiwana=True,
            ideas__isnull=False,
        ).distinct()

        # Wykluczenie kontraktów z powiązanymi Ideas o niepożądanych statusach
        contracts = contracts.exclude(
            Q(ideas__status_idei__status__in=excluded_statuses)
        ).distinct()

        # Dodatkowa filtracja dla statusów idei
        contracts = contracts.filter(
            Q(ideas__status_idei__status__in=included_statuses)
        ).distinct()

        for contract in contracts:
            koordynator = contract.koordynator
            if isinstance(koordynator, User):
                print(
                    f"Umowa {contract.id} wymaga podjęcia działań. "
                    f"Koordynator: {koordynator}, "
                    f"Przedmiot: {contract.subject}, "
                    f"Numer umowy: {contract.numer_umowy}"
                )

                tresc = f"Dzień dobry,\n\
Umowa numer {contract.id} wymaga Twojej uwagi ponieważ potencjalnie została już obsłużona w zakresie zapewnienia ciągłości usług.\n\n\
Jeżeli Pomysły, Potrzeby i Zakupy, które zostały stworzone aby zapewnic ciągłość tej umowy zostały zakończone i cel zapewnienia ciągłości usług został osiągnięty to zmień kontrolkę 'Czy umowa wymaga kontynuacji z Tak na Nie.\n\n\
W przeciwnym przypadku rozważ stworzenie Pomysłu, którego produketm będzie zapewnienie ciągłości usług\n\n\n\
Wchodząc na stronę https://avantic.gas.pgnig.pl/general/contracts/ możesz zweryfikować dla których umów w najbliższym czasie wymagane jest ich odnowienie\n\n\
Przedmiot umowy: {contract.subject} \n\n"
                tresc += generate_contract_url(contract.id)
                temat = f"Umowa numer {contract.id} wymaga uwagi"
                utworz_mail_do_wyslania(koordynator, temat, tresc)
            else:
                logger.error(
                    f"Koordynator for contract {contract.id} is not a User instance."
                )

    except Exception as e:
        logger.error(f"Wystąpił błąd podczas przetwarzania umów: {e}")


@shared_task
def umowy_zabezpieczone():
    """
    Zadanie Celery, które wywołuje funkcję `umowy_zabezpieczone_det` w celu identyfikacji umów, które prawdopodobnie zostały już obsłużonje w zakresei zapewnienia ciągłoścvi usług .
    """
    umowy_zabezpieczone_det()
