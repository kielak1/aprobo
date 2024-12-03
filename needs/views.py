from general.common_dashboard import common_dashboard
from django.shortcuts import redirect
from django.views.decorators.csrf import csrf_protect


@csrf_protect
def index(request):
    if not request.user.groups.filter(name="need_viewer").exists():
        target_if_no_rights = f"/account/login"
        return redirect(target_if_no_rights)
    return common_dashboard("needs/index.html", request)
