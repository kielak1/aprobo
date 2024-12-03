from django.shortcuts import render, redirect
from django.db.models import Count
from .models import EZZ, Purchases
from django.views.decorators.csrf import csrf_protect
from general.common_context import common_context


@csrf_protect
def unlinked_ezz(request):
    # Znajdź wszystkie EZZ, które nie mają powiązań z Purchases
    if not request.user.groups.filter(name="purchase_viewer").exists():
        target_if_no_rights = f"/account/login"
        return redirect(target_if_no_rights)
    ezz_list = EZZ.objects.annotate(num_purchases=Count("purchases")).filter(
        num_purchases=0
    )

    context = {"ezz_list": ezz_list}
    context.update(common_context(request))
    return render(request, "purchases/unlinked_ezz_list.html", context)
