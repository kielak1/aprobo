# new_user.py
import unidecode
from django import forms
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse, reverse_lazy
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.utils.text import slugify
from django.views.generic import FormView
from django.core.mail import send_mail

from general.mail import utworz_mail_do_wyslania, wyslij_mail_do_grupy
from general.linki import generate_user_url
from general.common_context import common_context


class NewUserForm(forms.Form):
    imie = forms.CharField(max_length=30, label="Imię")
    nazwisko = forms.CharField(max_length=30, label="Nazwisko")
    email = forms.EmailField(label="Email")


class CreateNewUserView(FormView):
    template_name = "new_user_form.html"
    form_class = NewUserForm
    success_url = reverse_lazy("after-init")  # Lub inny widok docelowy

    def form_valid(self, form):
        imie = form.cleaned_data["imie"].upper()
        nazwisko = form.cleaned_data["nazwisko"].upper()
        # Generowanie loginu
        base_username = (
            unidecode.unidecode(f"{imie[0]}{nazwisko}").replace(" ", "").lower()
        )
        username = base_username
        counter = 1
        while User.objects.filter(username=username).exists():
            username = f"{base_username}{counter}"
            counter += 1

        # Utworzenie użytkownika
        user = User.objects.create_user(
            username=username,
            first_name=imie,
            last_name=nazwisko,
            email=form.cleaned_data["email"],
            password=User.objects.make_random_password(),
        )
        user.is_active = False
        user.save()

        # Generowanie linku weryfikacyjnego
        verification_link = self.request.build_absolute_uri(
            reverse_lazy("verify_user", args=[user.pk])
        )

        # Wysłanie e-maila
        subject = "Potwierdzenie rejestracji"
        body = f"Witaj {imie} {nazwisko}, kliknij link aby zweryfikować swoje konto: {verification_link}"
        utworz_mail_do_wyslania(user=user, subject=subject, body=body)

        # Redirect to after_init with user info
        return redirect("after-init", imie=imie, nazwisko=nazwisko, username=username)


def verify_user(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    imie = user.first_name
    nazwisko = user.last_name
    username = user.username
    if not user.is_active:
        # Tworzenie linku do edycji użytkownika
        edit_user_url = generate_user_url(user_id)
        # Przygotowanie tematu i treści wiadomości
        subject = f"Prośba o aktywację konta użytkownika: {user.get_full_name()}"
        body = (
            f"Użytkownik {user.get_full_name()} (email: {user.email}) zweryfikował swój adres e-mail.\n\n"
            f"Prosimy o zakończenie procesu aktywacji konta lub jego usunięcie.\n"
            f"Link do edycji użytkownika: {edit_user_url}"
        )

        # Wysyłanie wiadomości do grupy "useradmin"
        wyslij_mail_do_grupy("useradmin", subject, body)

        # Wyświetlenie informacji zwrotnej dla użytkownika
        return redirect(
            "adres-zweryfikowany", imie=imie, nazwisko=nazwisko, username=username
        )
    else:
        return redirect(
            "konto-aktywne", imie=imie, nazwisko=nazwisko, username=username
        )


def AfterInit(request, imie, nazwisko, username):
    context = {
        "imie": imie,
        "nazwisko": nazwisko,
        "username": username,
    }
    return render(request, "account/after_init.html", context)


def AdresZweryfikowany(request, imie, nazwisko, username):
    context = {
        "imie": imie,
        "nazwisko": nazwisko,
        "username": username,
    }
    context.update(common_context(request))
    return render(request, "account/adres_zweryfikowany.html", context)


def KontoAktywne(request, imie, nazwisko, username):
    context = {
        "imie": imie,
        "nazwisko": nazwisko,
        "username": username,
    }
    context.update(common_context(request))
    return render(request, "account/konto_aktywne.html", context)


def AfterReset(request, imie, nazwisko, username):
    context = {
        "imie": imie,
        "nazwisko": nazwisko,
        "username": username,
    }
    context.update(common_context(request))
    return render(request, "account/after_reset.html", context)


def send_password_reset_link(request, user_id):
    # Pobranie użytkownika lub zgłoszenie błędu 404
    user = get_object_or_404(User, pk=user_id)

    # Generowanie unikalnego identyfikatora i tokenu
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    token = default_token_generator.make_token(user)

    # Generowanie pełnego linku resetu hasła
    reset_url = f"{settings.DEFAULT_DOMAIN}{reverse('password_reset_confirm', kwargs={'uidb64': uid, 'token': token})}"

    # Wiadomość e-mail
    subject = f"Reset hasła na Twoim koncie {user.username}"
    message = f"Cześć {user.username},\n\nKliknij poniższy link, aby zresetować swoje hasło:\n{reset_url}\n\nJeśli nie prosiłeś o reset hasła, zignoruj tę wiadomość."

    # Wysyłanie wiadomości e-mail
    send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [user.email])

    # Komunikat potwierdzający dla administratora
    message = (
        f"Szanowny administratorze,\n\n"
        f"Link resetujący hasło dla użytkownika {user.username} został wysłany na adres {user.email}.\n\n"
        f"Dziękujemy!"
    )
    subject = f"Potwierdzenie wysłania reset hasła do {user.username}"

    # Wysyłanie wiadomości e-mail do aktualnie zalogowanego użytkownika
    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        [request.user.email],  # E-mail bieżącego, zalogowanego użytkownika
    )
    # Tworzenie context i przekierowanie do 'after-reset' z parametrami
    imie = user.first_name
    nazwisko = user.last_name
    username = user.username

    return redirect(
        reverse(
            "after-reset",
            kwargs={"imie": imie, "nazwisko": nazwisko, "username": username},
        )
    )
