from django.shortcuts import render
from django.db.models import Avg, Max, Min
from django.db.models.functions import TruncHour, TruncDay, TruncWeek, TruncMonth
from general.models import Stamp
from django.utils.timezone import now, timedelta
from django.views.decorators.csrf import csrf_protect
from general.common_context import common_context


def get_time_grouping(period):
    if period == "hour":
        return TruncHour("czas_utworzenia")
    elif period == "day":
        return TruncDay("czas_utworzenia")
    elif period == "week":
        return TruncWeek("czas_utworzenia")
    elif period == "month":
        return TruncMonth("czas_utworzenia")
    return None


@csrf_protect
def aggregated_stamp_view(request):
    # Pobieramy parametr przedziału czasu z zapytania (domyślnie: godzina)
    period = request.GET.get("period", "hour")

    # Grupowanie danych w zależności od wybranego przedziału czasu
    time_grouping = get_time_grouping(period)

    if time_grouping is None:
        # Obsługa nieprawidłowego parametru
        context = {"message": "Nieprawidłowy przedział czasu"}
        context.update(common_context(request))
        return render(request, "error.html", context)

    # Agregowanie danych
    aggregated_data = (
        Stamp.objects.annotate(time_period=time_grouping)
        .values("nazwa", "typ_zdarzenia", "sekwencja", "time_period")
        .annotate(
            min_duration=Min("czas_trwania"),
            max_duration=Max("czas_trwania"),
            avg_duration=Avg("czas_trwania"),
        )
        # Odwracamy sortowanie, aby najnowsze były na górze
        .order_by("-time_period", "nazwa")
    )

    # Przetwarzanie wyników i konwersja czasu do milisekund
    results = {}
    for entry in aggregated_data:
        key = (entry["time_period"], entry["nazwa"])

        # Przeliczenie czasu trwania do milisekund i zaokrąglenie do jednej dziesiątej
        entry["min_duration"] = (
            round(entry["min_duration"].total_seconds() * 1000, 1)
            if entry["min_duration"]
            else None
        )
        entry["max_duration"] = (
            round(entry["max_duration"].total_seconds() * 1000, 1)
            if entry["max_duration"]
            else None
        )
        entry["avg_duration"] = (
            round(entry["avg_duration"].total_seconds() * 1000, 1)
            if entry["avg_duration"]
            else None
        )

        if key not in results:
            results[key] = []
        results[key].append(entry)

    context = {
        "aggregated_data": results,
        "period": period,
    }
    context.update(common_context(request))
    return render(request, "aggregated_stamp_table.html", context)
