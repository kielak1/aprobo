from django.core.exceptions import ObjectDoesNotExist
from general.models import Parametry


def get_param_int(param_name, default_value=0):
    """
    Zwraca wartość numeryczną parametru o podanej nazwie.
    Jeśli parametr nie istnieje, tworzy go z domyślną wartością.

    :param param_name: Nazwa parametru
    :type param_name: str
    :param default_value: Domyślna wartość w przypadku braku parametru
    :type default_value: int
    :return: Wartość numeryczna parametru
    :rtype: int
    """
    param, created = Parametry.objects.get_or_create(
        nazwa=param_name, defaults={"num": default_value}
    )
    return param.num


def get_param_str(param_name, default_value="0"):
    """
    Zwraca wartość tekstową parametru o podanej nazwie.
    Jeśli parametr nie istnieje, tworzy go z domyślną wartością.

    :param param_name: Nazwa parametru
    :type param_name: str
    :param default_value: Domyślna wartość w przypadku braku parametru
    :type default_value: str
    :return: Wartość tekstowa parametru
    :rtype: str
    """
    param, created = Parametry.objects.get_or_create(
        nazwa=param_name, defaults={"str": default_value}
    )
    return param.str
