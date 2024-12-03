"""
URL configuration for test1 project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/

Examples:
    Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  
"""

from django.contrib import admin
from django.urls import path
from django.urls import include, path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from ideas.views_edit_idea import edit_idea_short
from needs.views_edit_need import edit_need_short
from contracts.views_edit_contract import edit_contract_short
from purchases.views_edit_purchase import edit_purchase_short
from account.views import user_login

urlpatterns = [
    path("general/", include("general.urls")),
    path("purchases/", include("purchases.urls")),
    path("contracts/", include("contracts.urls")),
    path("needs/", include("needs.urls")),
    path("ideas/", include("ideas.urls")),
    path("admin/", admin.site.urls),
    path("", views.avantic, name="avantic"),
    path("account/", include("account.urls")),
    path("login/", user_login, name="login"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    path("edit_purchase_short/", edit_purchase_short, name="edit_purchase_short"),
    path("edit_contract_short/", edit_contract_short, name="edit_contract_short"),
    path("edit_need_short/", edit_need_short, name="edit_need_short"),
    path("edit_idea_short/", edit_idea_short, name="edit_idea_short"),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
