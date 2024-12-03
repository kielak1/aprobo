from .views_full_search import full_search
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_protect
from general.advanced_search import search_advanced
from general.advanced_search import query_grammar
from django.contrib.auth.decorators import login_required
from general.models import Zapytanie
from general.common_context import common_context
import logging


logger = logging.getLogger("avantic")


@csrf_protect
def search_view(request):
    com_cont = common_context(request)
    if not (com_cont["is_any_viewer"] or com_cont["is_client"]):
        # if not (
        #     request.user.groups.filter(name="idea_viewer").exists()
        #     or request.user.groups.filter(name="contract_viewer").exists()
        #     or
        #     #  request.user.groups.filter(name='client').exists() or
        #     request.user.groups.filter(name="purchase_viewer").exists()
        # ):
        target_if_no_rights = "/account/login"
        return redirect(target_if_no_rights)

    # Inicjalizacja zmiennych dla kontekstu
    contract_list = []
    ideas = []
    need_list = []
    purchase_list = []
    search_word = ""
    query_name = ""
    parsed = ""
    error_query = ""
    saved_queries = Zapytanie.objects.filter(user=request.user)

    if request.method == "POST":
        search_word = request.POST.get("search_word", "")
        query_name = request.POST.get("query_name", "")
        save_query = request.POST.get("save_query")
        selected_query_id = request.POST.get("saved_queries")
        delete_query = request.POST.get("delete_query")

        # Obsługa usunięcia zapytania
        if delete_query and selected_query_id:
            Zapytanie.objects.filter(id=selected_query_id, user=request.user).delete()
            return redirect("full_search")  # Odświeżenie strony po usunięciu zapytania

        # Obsługa zapisu zapytania
        if save_query and search_word and len(query_name) > 1:
            new_query = Zapytanie(
                nazwa=query_name, tresc=search_word, user=request.user
            )
            new_query.save()

        # Obsługa wyboru zapisanego zapytania
        if selected_query_id:
            selected_query = Zapytanie.objects.get(
                id=selected_query_id, user=request.user
            )
            search_word = selected_query.tresc

        # Sprawdzenie pierwszego znaku search_word
        if search_word and search_word[0] == ">":
            search_query = search_word[1:]
            try:
                krotka, parsed = search_advanced(search_query)
                contract_list, ideas, need_list, purchase_list = krotka
            except Exception as e:
                error_query = f"Błąd zapytania: {e} \n\nPisz zapytania zgodnie z gramtyką lub nie używaj trybu zaawansowanego"
        else:
            contract_list, ideas, need_list, purchase_list = full_search(search_word)

    # korekta context jesli client
    is_client = com_cont["is_client"]
    if is_client:
        klienci_rel = com_cont["klienci_rel"]
        contract_list = []
        ideas = [
            idea
            for idea in ideas
            if idea.client and idea.client.short_name in klienci_rel
        ]

        need_list = [
            need
            for need in need_list
            if need.client and need.client.short_name in klienci_rel
        ]

        purchase_list = [
            purchase
            for purchase in purchase_list
            if purchase.client and purchase.client.short_name in klienci_rel
        ]

    context = {
        "contract_list": contract_list,
        "ideas": ideas,
        "need_list": need_list,
        "purchase_list": purchase_list,
        "search_word": search_word,
        "query_grammar": query_grammar,
        "parsed": parsed,
        "error_query": error_query,
        "query_name": query_name,
        "saved_queries": saved_queries,
    }
    context.update(com_cont)

    return render(request, "full_search.html", context)
