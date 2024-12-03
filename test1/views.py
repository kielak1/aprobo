from django.shortcuts import render
from general.common_dashboard import common_dashboard
from django.views.decorators.csrf import csrf_protect
from django.shortcuts import redirect


@csrf_protect
def avantic(request):
    if not (
        request.user.groups.filter(name="idea_viewer").exists()
        or request.user.groups.filter(name="contract_viewer").exists()
        or request.user.groups.filter(name="client").exists()
        or request.user.groups.filter(name="advanced").exists()
        or request.user.groups.filter(name="useradmin").exists()
        or request.user.groups.filter(name="superuser").exists()
        or request.user.groups.filter(name="accountant").exists()
        or request.user.groups.filter(name="dataadmin").exists()
    ):
        target_if_no_rights = "/account/login"
        return redirect(target_if_no_rights)
    return common_dashboard("general/index-general.html", request)
