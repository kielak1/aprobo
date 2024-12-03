from django.db import models
from django.contrib.auth.models import Group, User
from django.utils.translation import gettext_lazy as _
import logging

logger = logging.getLogger("avantic")


class Basket(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True, null=True)
    groups = models.ManyToManyField(Group, related_name="baskets")

    class Meta:
        verbose_name = _("Koszyk uprawnień")
        verbose_name_plural = _("Koszyki uprawnień")

    def __str__(self):
        return self.name

    def add_user_permissions(self, user: User):
        """
        Dodaje wszystkie uprawnienia z koszyka do podanego użytkownika.

        :param user: Użytkownik, do którego dodawane są uprawnienia
        :type user: User
        """
        for group in self.groups.all():
            user.groups.add(group)  # Dodaj grupę do użytkownika
            logger.info(f"Dodano grupę {group.name} do użytkownika {user.username}")

    def remove_user_permissions(self, user: User):
        """
        Usuwa wszystkie uprawnienia z koszyka od podanego użytkownika.

        :param user: Użytkownik, od którego usuwane są uprawnienia
        :type user: User
        """
        for group in self.groups.all():
            user.groups.remove(group)  # Usuń grupę od użytkownika
            logger.info(f"Usunięto grupę {group.name} od użytkownika {user.username}")


# Zmiana wyświetlanych nazw dla modelu User
User._meta.verbose_name = _("Użytkownik")
User._meta.verbose_name_plural = _("Użytkownicy")

# Zmiana wyświetlanych nazw dla modelu Group
Group._meta.verbose_name = _("Grupa")
Group._meta.verbose_name_plural = _("Grupy")
