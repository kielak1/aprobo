from django import forms
from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.utils.http import url_has_allowed_host_and_scheme
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User, Group
from django.contrib import messages
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from django.contrib.auth.views import LogoutView as AuthLogoutView

from .forms import LoginForm, UserRegistrationForm
from general.common_dashboard import common_dashboard
from general.common_context import common_context
import logging

logger = logging.getLogger("avantic")

@csrf_protect
@login_required
def dashboard(request):
    return common_dashboard("account/dashboard.html", request)


@csrf_protect
def register(request):
    if not request.user.groups.filter(name="useradmin").exists():
        target_if_no_rights = f"/account/login"
        return redirect(target_if_no_rights)
    if request.method == "POST":
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            # Utworzenie nowego obiektu użytkownika, ale jeszcze nie zapisujemy go w bazie danych.
            new_user = user_form.save(commit=False)
            # Ustawienie wybranego hasła.
            new_user.set_password(user_form.cleaned_data["password"])
            # Zapisanie obiektu User.
            new_user.save()
            return render(request, "account/register_done.html", {"new_user": new_user})
    else:
        user_form = UserRegistrationForm()
    return render(request, "account/register.html", {"user_form": user_form})


class LoginForm(forms.Form):
    username = forms.CharField(
        label="Nazwa użytkownika",
        max_length=100,
        widget=forms.TextInput(attrs={"autocomplete": "off"}),
    )
    password = forms.CharField(
        label="Hasło", widget=forms.PasswordInput(attrs={"autocomplete": "off"})
    )

def user_login(request: HttpRequest) -> HttpResponse:
    next_url = request.GET.get("next") or request.POST.get("next", "avantic")
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(username=cd["username"], password=cd["password"])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    messages.success(
                        request, "Uwierzytelnienie zakończyło się sukcesem."
                    )
                    if url_has_allowed_host_and_scheme(
                        next_url, allowed_hosts={request.get_host()}
                    ):
                        return redirect(next_url)
                    return redirect("avantic")
                else:
                    messages.error(request, "Konto jest zablokowane.")
            else:
                messages.error(request, "Nieprawidłowe dane uwierzytelniające!")
        else:
            messages.error(request, "Nieprawidłowe dane w formularzu!")
    else:
        form = LoginForm()
    return render(request, "account/login.html", {"form": form, "next": next_url})


class LogoutView(AuthLogoutView):
    def dispatch(self, request, *args, **kwargs):
        print("test")
        if request.method == "GET":
            return self.post(request, *args, **kwargs)
        return super().dispatch(request, *args, **kwargs)


def user_in_useradmin_group(request):
    user = request.user
    return user.groups.filter(name="useradmin").exists()  # or user.is_superuser


@login_required
@csrf_exempt
def user_group_table(request):
    if not request.user.groups.filter(name="useradmin").exists():
        target_if_no_rights = f"/account/login"
        return redirect(target_if_no_rights)

    users = User.objects.all().order_by("username")
    groups = Group.objects.all()

    if request.method == "POST":
        user_id = request.POST.get("user_id")
        group_id = request.POST.get("group_id")
        action = request.POST.get("action")
        user = User.objects.get(id=user_id)
        group = Group.objects.get(id=group_id)

        if action == "add":
            if user_in_useradmin_group(request):
                user.groups.add(group)
        elif action == "remove":
            if user_in_useradmin_group(request):
                user.groups.remove(group)
        return redirect("user_group_table")
    context = {"users": users, "groups": groups}
    context.update(common_context(request))
    return render(request, "account/user_group_table.html", context)
