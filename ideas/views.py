from django.shortcuts import redirect
from general.common_dashboard import common_dashboard


from django.views.decorators.csrf import csrf_protect


@csrf_protect
def index(request):
    if not (
        request.user.groups.filter(name="idea_viewer").exists()
        or request.user.groups.filter(name="client").exists()
    ):
        target_if_no_rights = "/account/login"
        return redirect(target_if_no_rights)
    return common_dashboard("ideas/index.html", request)
