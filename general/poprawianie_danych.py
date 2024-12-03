from celery import shared_task
from django.utils import timezone
import logging

logger = logging.getLogger("avantic")


def logujideas(idea_instance, dzialanie):
    from ideas.models import LogIdea
    from django.contrib.auth.models import User

    try:
        system_user = User.objects.get(username="system")
    except User.DoesNotExist:
        print("Użytkownik 'system' nie istnieje.")
        return

    wpis_do_logu = LogIdea(user=system_user, akcja=dzialanie)
    wpis_do_logu.save()

    idea_instance.log.add(wpis_do_logu)
    idea_instance.save()


def logujneeds(need_instance, dzialanie):
    from needs.models import LogNeed
    from django.contrib.auth.models import User

    try:
        system_user = User.objects.get(username="system")
    except User.DoesNotExist:
        print("Użytkownik 'system' nie istnieje.")
        return

    wpis_do_logu = LogNeed(user=system_user, akcja=dzialanie)
    wpis_do_logu.save()

    need_instance.log.add(wpis_do_logu)
    need_instance.save()


def logujcontracts(contract_instance, dzialanie):
    from contracts.models import LogContract
    from django.contrib.auth.models import User

    try:
        system_user = User.objects.get(username="system")
    except User.DoesNotExist:
        print("Użytkownik 'system' nie istnieje.")
        return

    wpis_do_logu = LogContract(user=system_user, akcja=dzialanie)
    wpis_do_logu.save()

    contract_instance.log.add(wpis_do_logu)
    contract_instance.save()


def logujpurchases(purchase_instance, dzialanie):
    from purchases.models import LogPurchase
    from django.contrib.auth.models import User

    try:
        system_user = User.objects.get(username="system")
    except User.DoesNotExist:
        print("Użytkownik 'system' nie istnieje.")
        return

    wpis_do_logu = LogPurchase(user=system_user, akcja=dzialanie)
    wpis_do_logu.save()

    purchase_instance.log.add(wpis_do_logu)
    purchase_instance.save()


def odwies_zawieszone():
    from ideas.models import Ideas, StatusIdei
    from .mail import utworz_mail_do_wyslania
    from general.linki import generate_idea_url
    from django.db import transaction

    logger = logging.getLogger(__name__)

    try:
        status_zawieszona = StatusIdei.objects.get(status="zawieszona")
        status_nowa = StatusIdei.objects.get(status="nowa")
    except StatusIdei.DoesNotExist:
        logger.error("Nie znaleziono odpowiednich statusów.")
        return

    current_date = timezone.now().date()
    logger.info(f"Current date: {current_date}")

    zawieszone_idee = Ideas.objects.filter(
        status_idei=status_zawieszona, do_kiedy_zawieszona__lte=current_date
    )

    for idea in zawieszone_idee:

        with transaction.atomic():
            try:
                idea.status_idei = status_nowa
                logujideas(idea, "Odwieś")
                idea.save()
                logger.info(
                    f"Odwieszono ideę: ID={idea.id}, subject={idea.subject}, data zawieszenia={idea.do_kiedy_zawieszona}"
                )

                tresc = (
                    f"\n\nDzień dobry,\n\nw związku z tym, że osiągnięta została określona data do kiedy Pomysł {idea.id} "
                    f"miał być zawieszony ({idea.do_kiedy_zawieszona}) został on odwieszony\n\n"
                )
                tresc += generate_idea_url(idea.id)
                tresc += "\n\nFormularz edycji przedmiotowego pomysłu znajduje się pod powyższym linkiem."

                utworz_mail_do_wyslania(
                    idea.osoba_prowadzaca,
                    f"System odwiesił Pomysł numer {idea.id}",
                    tresc,
                )
            except Exception as e:
                logger.error(f"Failed to update idea ID={idea.id}. Error: {e}")
                transaction.set_rollback(True)


@shared_task
def odwies_zawieszone_pomysly():
    odwies_zawieszone()


def popraw_status_idei_det():
    from ideas.models import Ideas, StatusIdei
    from needs.models import StatusNeed
    from .mail import utworz_mail_do_wyslania
    from general.linki import generate_idea_url

    try:
        status_realizowana = StatusIdei.objects.get(status="realizowana")
        status_need_realizowana = StatusNeed.objects.get(status="realizowana")
    except (StatusIdei.DoesNotExist, StatusNeed.DoesNotExist):
        print("Nie znaleziono odpowiednich statusów.")
        return

    ideas_to_update = Ideas.objects.exclude(status_idei=status_realizowana)

    for idea in ideas_to_update:
        if idea.needs.filter(status_potrzeby=status_need_realizowana).exists():
            idea.status_idei = status_realizowana
            logujideas(idea, "realizowana")
            idea.save()
            print(f"Zaktualizowano ideę: ID={idea.id}, subject={idea.subject}")
            tresc = f'\nDzień dobry,\n\nStatus Pomysłu {idea.id} został ustawiony na "realizowana" w związku z tym, że istnieją powiązane i niezakończone Zakupy\n\n'
            tresc += generate_idea_url(idea.id)
            tresc += "\n\nFormularz edycji przedmiotowego Pomysłu znajduje się pod powyższym linkiem."
            utworz_mail_do_wyslania(
                idea.osoba_prowadzaca,
                f"System przywrócił właściwy status dla Pomysłu numer {idea.id}",
                tresc,
            )


@shared_task
def popraw_status_idei():
    popraw_status_idei_det()


def popraw_status_needs_det():
    from needs.models import Needs, StatusNeed
    from general.models import Status_procesu
    from .mail import utworz_mail_do_wyslania
    from general.linki import generate_need_url

    try:
        status_need_realizowana = StatusNeed.objects.get(status="realizowana")
        status_purchases_zakonczony = Status_procesu.objects.get(status="zakończony")
        status_purchases_anulowany = Status_procesu.objects.get(status="anulowany")
    except (StatusNeed.DoesNotExist, Status_procesu.DoesNotExist):
        print("Nie znaleziono odpowiednich statusów.")
        return

    needs_to_update = Needs.objects.exclude(status_potrzeby=status_need_realizowana)

    for need in needs_to_update:
        if need.purchases.exclude(
            status_procesu__in=[status_purchases_zakonczony, status_purchases_anulowany]
        ).exists():
            need.status_potrzeby = status_need_realizowana
            logujneeds(need, "realizowana")
            need.save()
            print(f"Zaktualizowano potrzebę: ID={need.id}, subject={need.subject}")
            tresc = f'\nDzień dobry,\n\nStatus Potrzeby {need.id} został ustawiony na "realizowana" w związku z tym, że istnieją powiązane i niezakończone Pomysły\n\n'
            tresc += generate_need_url(need.id)
            tresc += "\n\nFormularz edycji przedmiotowej Potrzeby znajduje się pod powyższym linkiem."
            utworz_mail_do_wyslania(
                need.osoba_prowadzaca,
                f"System przywrócił właściwy status dla Potrzeby numer {need.id}",
                tresc,
            )


@shared_task
def popraw_status_needs():
    popraw_status_needs_det()


def section_form_user(user):
    from general.models import Sections

    sekcja = Sections.objects.filter(users=user).first()
    return sekcja


def user_from_section(sekcja):
    from general.models import Sections

    dzial = Sections.objects.filter(short_name=sekcja).first()
    if dzial:
        koordynator = dzial.kierownik
        return koordynator
    else:
        return None


def sections_users_det():
    """
    Próba ustalenia działu na podstawie użytkownika i użytkownika na podstawie działu w Umowach, Pomysłach, Potrzebach i Zakupach.
    Wysłanie notyfikacji do właściciela.
    """
    from contracts.models import Contracts
    from general.models import Sections
    from ideas.models import Ideas
    from needs.models import Needs
    from purchases.models import Purchases

    # Umowy
    try:
        contracts = Contracts.objects.filter(
            section__isnull=False,
            koordynator__isnull=True,
        ).distinct()

        for contract in contracts:
            dzial = Sections.objects.filter(short_name=contract.section).first()
            koordynator = user_from_section(dzial)
            if koordynator:
                contract.koordynator = koordynator
                contract.save()
                logujcontracts(contract, f"user {koordynator}")
                print(
                    f"W umowie {contract.id} ustawiono koordynatora It na {contract.koordynator}"
                )
    except Exception as e:
        logger.error(f"Wystąpił błąd podczas przetwarzania umów: {e}")

    try:
        contracts = Contracts.objects.filter(
            section__isnull=True,
            koordynator__isnull=False,
        ).distinct()
        for contract in contracts:
            sekcja = section_form_user(contract.koordynator)
            if sekcja:
                contract.section = sekcja
                contract.save()
                logujcontracts(contract, f"dział {sekcja}")
                print(f"W umowie {contract.id} ustawiono dział na {contract.section}")
            else:
                print(f"Ustawienie działu w umowie {contract.id} jest niemożliwe")
    except Exception as e:
        logger.error(f"Wystąpił błąd podczas przetwarzania umów: {e}")

    # Pomysły
    try:
        ideas = Ideas.objects.filter(
            section__isnull=False,
            osoba_prowadzaca__isnull=True,
        ).distinct()

        for idea in ideas:
            dzial = Sections.objects.filter(short_name=idea.section).first()
            koordynator = user_from_section(dzial)
            if koordynator:
                idea.osoba_prowadzaca = koordynator
                idea.save()
                logujideas(idea, f"user {koordynator}")
                print(
                    f"W pomyśle {idea.id} ustawiono koordynatora It na {idea.osoba_prowadzaca}"
                )
    except Exception as e:
        logger.error(f"Wystąpił błąd podczas przetwarzania pomysłów: {e}")

    try:
        ideas = Ideas.objects.filter(
            section__isnull=True,
            osoba_prowadzaca__isnull=False,
        ).distinct()
        for idea in ideas:
            sekcja = section_form_user(idea.osoba_prowadzaca)
            if sekcja:
                idea.section = sekcja
                idea.save()
                logujideas(idea, f"dział {idea.section}")
                print(f"W pomyśle {idea.id} ustawiono dział na {idea.section}")
            else:
                print(f"Ustawienie działu w pomyśle {idea.id} jest niemożliwe")
    except Exception as e:
        logger.error(f"Wystąpił błąd podczas przetwarzania pomysłów: {e}")

    # Potrzeby
    try:
        needs = Needs.objects.filter(
            section__isnull=False,
            osoba_prowadzaca__isnull=True,
        ).distinct()

        for need in needs:
            dzial = Sections.objects.filter(short_name=need.section).first()
            koordynator = user_from_section(dzial)
            if koordynator:
                need.osoba_prowadzaca = koordynator
                need.save()
                logujneeds(need, f"user {koordynator}")
                print(
                    f"W potrzebie {need.id} ustawiono koordynatora It na {need.osoba_prowadzaca}"
                )
    except Exception as e:
        logger.error(f"Wystąpił błąd podczas przetwarzania pomysłów: {e}")

    try:
        needs = Needs.objects.filter(
            section__isnull=True,
            osoba_prowadzaca__isnull=False,
        ).distinct()
        for need in needs:
            sekcja = section_form_user(need.osoba_prowadzaca)
            if sekcja:
                need.section = sekcja
                need.save()
                logujneeds(need, f"dział {need.section}")
                print(f"W pomyśle {need.id} ustawiono dział na {need.section}")
            else:
                print(f"Ustawienie działu w potrzebie {need.id} jest niemożliwe")
    except Exception as e:
        logger.error(f"Wystąpił błąd podczas przetwarzania pomysłów: {e}")

    # Zakupy
    try:
        purchases = Purchases.objects.filter(
            section__isnull=False,
            osoba_prowadzaca__isnull=True,
        ).distinct()

        for purchase in purchases:
            dzial = Sections.objects.filter(short_name=purchase.section).first()
            koordynator = user_from_section(dzial)
            if koordynator:
                purchase.osoba_prowadzaca = koordynator
                purchase.save()
                logujpurchases(purchase, f"user {koordynator}")
                print(
                    f"W zakupie {purchase.id} ustawiono koordynatora It na {purchase.osoba_prowadzaca}"
                )
    except Exception as e:
        logger.error(f"Wystąpił błąd podczas przetwarzania pomysłów: {e}")

    try:
        purchases = Purchases.objects.filter(
            section__isnull=True,
            osoba_prowadzaca__isnull=False,
        ).distinct()
        for purchases in purchases:
            sekcja = section_form_user(purchase.osoba_prowadzaca)
            if sekcja:
                purchase.section = sekcja
                purchase.save()
                logujpurchases(purchase, f"dział {[purchase].section}")
                print(f"W zakupie {purchase.id} ustawiono dział na {purchase.section}")
            else:
                print(f"Ustawienie działu w zakupie {purchase.id} jest niemożliwe")
    except Exception as e:
        logger.error(f"Wystąpił błąd podczas przetwarzania pomysłów: {e}")


@shared_task
def sections_users():
    sections_users_det()


def skoryguj_status_zakupow_det():
    """
    Skorygowanie statusu zakupow na podstawie statusu zaimportowanych EZZ
    Wysłanie notyfikacji do właściciela.
    """
    from purchases.auto_status_z_EZZ import auto_status_zakupu
    from purchases.models import Purchases
    from general.models import Status_procesu

    all_purchases = Purchases.objects.all()
    for purchase in all_purchases:
        # Pobierz aktualny status_procesu i status EZZ
        current_status_procesu = purchase.status_procesu.status
        ezz_status = purchase.ezz.status

        # Wywołaj funkcję auto_status_zakupu
        new_status_procesu = auto_status_zakupu(current_status_procesu, ezz_status)

        # Porównaj wynik z aktualnym status_procesu
        if new_status_procesu != current_status_procesu:
            purchase.status_procesu = Status_procesu.objects.get(
                status=new_status_procesu
            )
            purchase.save()
            print(
                f"Zmieniono status Zakupu {purchase.id} z {current_status_procesu} na {new_status_procesu}"
            )
            logujpurchases(
                purchase, f"status {current_status_procesu} -> {new_status_procesu}"
            )


@shared_task
def skoryguj_status_zakupow():
    skoryguj_status_zakupow_det()
