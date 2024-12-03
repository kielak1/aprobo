from django.conf import settings
from django.views.decorators.csrf import csrf_protect


@csrf_protect
def environment(request):
    host = request.get_host()
    if "avantic.gas.pgnig.pl" in host:
        return {"ENVIRONMENT": "prod"}
    else:
        return {"ENVIRONMENT": "nonprod"}
