from django.core.mail import EmailMessage
from django.http import HttpResponse
from general.models import MaileDoWyslania
from django.contrib.auth.models import User, Group
from celery import shared_task
from .parametry import get_param_int
import logging

logger = logging.getLogger("avantic")


def wyslij_mail(mail: MaileDoWyslania) -> bool:
    """
    Wysyła e-mail na podstawie obiektu MaileDoWyslania i usuwa rekord po pomyślnym wysłaniu.

    Parameters
    ----------
    mail : MaileDoWyslania
        Obiekt zawierający informacje o e-mailu do wysłania.

    Returns
    -------
    bool
        Zwraca True, jeśli e-mail został wysłany pomyślnie, w przeciwnym razie False.
    """
    if get_param_int("send_not") == 1:
        recipients_list = [mail.recipient]
        try:
            email = EmailMessage(
                mail.subject, mail.body, from_email=mail.sender, to=recipients_list
            )
            email.send()
            if mail.id is not None:
                mail.delete()  # Usuwa rekord po pomyślnym wysłaniu e-maila
            return True
        except Exception as e:
            print(f"Failed to send email: {e}")
            if mail.id is not None:
                mail.delete()  # Usuwa rekord po niepomyślnej próbie wysłania e-maila
            return False
    else:
        return False


@shared_task
def wyslij_wszystkie_maile():
    """
    Wysyła wszystkie e-maile z modelu MaileDoWyslania.
    Po pomyślnym wysłaniu, rekordy zostają usunięte z bazy danych.
    """
    wszystkie_maile = MaileDoWyslania.objects.all()
    for mail in wszystkie_maile:
        if wyslij_mail(mail):
            if mail.id is not None:
                mail.delete()
            print(f"E-mail to {mail.recipient} has been sent and deleted.")
        else:
            print(f"Failed to send e-mail to {mail.recipient}.")


def utworz_mail_do_wyslania(user: User, subject: str, body: str, sender: str = None):
    """
    Tworzy obiekt MaileDoWyslania na podstawie przekazanych parametrów.

    Parameters
    ----------
    user : User
        Użytkownik, do którego zostanie wysłany mail.
    subject : str
        Temat maila.
    body : str
        Treść maila.
    sender : str, optional
        Nadawca maila. Jeśli nie podany, użyty zostanie domyślny adres.

    Returns
    -------
    MaileDoWyslania
        Utworzony obiekt MaileDoWyslania.
    """
    if get_param_int("send_not") == 1:
        recipient = user.email
        # Użyj podanego nadawcy lub domyślnego, jeśli nie został podany
        mail = MaileDoWyslania.objects.create(
            subject=subject,
            body=body,
            recipient=recipient,
            sender=sender if sender else "avantic@pgnig.pl",
        )
        return mail


def wyslij_mail_do_grupy(nazwa_grupy: str, subject: str, body: str):
    """
    Wysyła wiadomości e-mail do wszystkich użytkowników należących do danej grupy.

    Parameters
    ----------
    nazwa_grupy : str
        Nazwa grupy użytkowników, do której zostaną wysłane maile.
    subject : str
        Temat maila.
    body : str
        Treść maila.

    Returns
    -------
    None
    """
    if get_param_int("send_not") == 1:
        # Pobierz grupę na podstawie nazwy
        try:
            grupa = Group.objects.get(name=nazwa_grupy)
        except Group.DoesNotExist:
            print(f"Grupa o nazwie {nazwa_grupy} nie istnieje.")
            return

        # Pobierz wszystkich użytkowników należących do grupy
        users = grupa.user_set.all()

        # Dla każdego użytkownika w grupie, utwórz i wyślij mail
        for user in users:
            utworz_mail_do_wyslania(user, subject, body)
