from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from .views import LogoutView, user_group_table
from .views_user_admin import UserUpdateView, PasswordChangeView, UserListView
from account.new_user import (
    CreateNewUserView,
    verify_user,
    AfterInit,
    AdresZweryfikowany,
    KontoAktywne,
    send_password_reset_link,
    AfterReset
)
from ideas.views_edit_idea import edit_idea_short
from needs.views_edit_need import edit_need_short
from contracts.views_edit_contract import edit_contract_short
from purchases.views_edit_purchase import edit_purchase_short
from django.urls import reverse_lazy
from .views import user_login

urlpatterns = [
    # Authentication and password management
 #   path("login/", auth_views.LoginView.as_view(), name="login"),
    path("login/", user_login, name="login"),
   
    path("logout/", LogoutView.as_view(), name="logout"),
    path("password_change/", PasswordChangeView.as_view(), name="password_change"),
    path(
        "password_change/done/",
        auth_views.PasswordChangeDoneView.as_view(),
        name="password_change_done",
    ),
    path(
        "password_reset/",
        auth_views.PasswordResetView.as_view(
            template_name="password_reset_form.html",
            subject_template_name="registration/password_reset_subject.txt",
            email_template_name="registration/password_reset_email.txt",
            html_email_template_name="registration/password_reset_email.html",
        ),
        name="password_reset",
    ),
    path(
        "password_reset_done/",
        auth_views.PasswordResetDoneView.as_view(
            template_name="password_reset_done.html"
        ),
        name="password_reset_done",
    ),
    path(
        "reset/<uidb64>/<token>/",
        auth_views.PasswordResetConfirmView.as_view(
            template_name="password_reset_confirm.html"
        ),
        name="password_reset_confirm",
    ),
    path(
        "reset/done/",
        auth_views.PasswordResetCompleteView.as_view(
            template_name="password_reset_complete.html"
        ),
        name="password_reset_complete",
    ),
    # Registration and user management
    path("register/", views.register, name="register"),
    path("", views.dashboard, name="dashboard"),
    path("edit/<int:pk>/", UserUpdateView.as_view(), name="edit-user"),
    path("change-password/", PasswordChangeView.as_view(), name="change-password"),
    path("users/", UserListView.as_view(), name="user-list"),
    path("user-groups/", user_group_table, name="user_group_table"),
    path("edit_purchase_short/", edit_purchase_short, name="edit_purchase_short"),
    path("edit_contract_short/", edit_contract_short, name="edit_contract_short"),
    path("edit_need_short/", edit_need_short, name="edit_need_short"),
    path("edit_idea_short/", edit_idea_short, name="edit_idea_short"),
    path("nowy/", CreateNewUserView.as_view(), name="create_new_user"),
    path(
        "after_init/<str:imie>/<str:nazwisko>/<str:username>/",
        AfterInit,
        name="after-init",
    ),
    path("verify/<int:user_id>/", verify_user, name="verify_user"),
    path(
        "adres_zweryfikowany/<str:imie>/<str:nazwisko>/<str:username>/",
        AdresZweryfikowany,
        name="adres-zweryfikowany",
    ),
    path(
        "konto_aktywne/<str:imie>/<str:nazwisko>/<str:username>/",
        KontoAktywne,
        name="konto-aktywne",
    ),
    path(
        "send_password_reset/<int:user_id>/",
        send_password_reset_link,
        name="send_password_reset",
    ),    
    path(
        "after_reset<str:imie>/<str:nazwisko>/<str:username>/",
        AfterReset,
        name="after-reset",
    ),
]
