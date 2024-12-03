from django.shortcuts import render, redirect
from purchases.auto_status_z_EZZ import auto_status_zakupu
from purchases.models import Purchases, EZZ, LogPurchase
from general.models import Status_procesu
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_protect
from general.common_context import common_context


@csrf_protect
def auto_ezz(request):
    if not request.user.groups.filter(name="contract_editor").exists():
        target_if_no_rights = f"/account/login"
        return redirect(target_if_no_rights)

    # Lista do przechowywania krotek
    results = []

    # Przejrzyj wszystkie rekordy Purchases
    all_purchases = Purchases.objects.all()

    for purchase in all_purchases:
        # Pobierz aktualny status_procesu i status EZZ
        current_status_procesu = purchase.status_procesu.status
        ezz_status = purchase.ezz.status

        # Wywołaj funkcję auto_status_zakupu
        new_status_procesu = auto_status_zakupu(current_status_procesu, ezz_status)

        # Porównaj wynik z aktualnym status_procesu
        if new_status_procesu != current_status_procesu:

            # Stwórz krotkę z wymaganymi informacjami
            result_tuple = (
                purchase.id,
                current_status_procesu,
                purchase.ezz.id if purchase.ezz else None,
                ezz_status,
                new_status_procesu,
                purchase.przedmiot_zakupu,
            )
            # Dodaj krotkę do listy
            results.append(result_tuple)
            purchase.status_procesu = Status_procesu.objects.get(
                status=new_status_procesu
            )
            purchase.save()
            wpis_do_logu = LogPurchase()
            wpis_do_logu.user = User.objects.get(username="system")
            wpis_do_logu.akcja = new_status_procesu
            wpis_do_logu.save()
            purchase.log.add(wpis_do_logu)

    # Przygotuj kontekst
    context = {"results": results}
    context.update(common_context(request))
    return render(request, "general/auto_ezz.html", context)
