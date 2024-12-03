from .models import Contracts
from general.models import Sections


from django.db.models import Count, Q


def przygotuj_dane_do_szablonu():
    # Liczba rekordów Contracts, w których wartość obslugiwana jest równa None
    liczba_obslugiwanych_none = Contracts.objects.filter(
        obslugiwana__isnull=True
    ).count()
    # Liczba rekordów Contracts, w których wartość section jest nieustawiona
    liczba_section_none = Contracts.objects.filter(
        section__isnull=True, obslugiwana=True
    ).count()

    # Dla rekordów Contracts, dla których wartość section jest ustawiona,
    # podaj liczby rekordów, dla których nie jest ustawiona wartość pola czy_wymagana_kontynuacja
    # w podziale na wszystkie wartości section.
    rekordy_bez_kontynuacji_po_sekcji = (
        Contracts.objects.filter(
            obslugiwana=True,
            section__isnull=False,
            czy_wymagana_kontynuacja__isnull=True,
        )
        .values("section__name")
        .annotate(liczba=Count("id"))
    )

    # Dla rekordów Contracts, dla których wartość section jest ustawiona oraz
    # wartość czy_wymagana_kontynuacja jest True, podaj liczby rekordów,
    # dla których nie jest ustawiona wartość pola wymagana_data_zawarcia_kolejnej_umowy
    # w podziale na wszystkie wartości section.
    rekordy_bez_daty_umowy_po_sekcji = (
        Contracts.objects.filter(
            obslugiwana=True,
            section__isnull=False,
            czy_wymagana_kontynuacja=True,
            wymagana_data_zawarcia_kolejnej_umowy__isnull=True,
        )
        .values("section__name")
        .annotate(liczba=Count("id"))
    )

    # Dla rekordów Contracts, dla których wartość section jest ustawiona oraz
    # wartość czy_wymagana_kontynuacja jest True, podaj liczby rekordów,
    # dla których brak jest powiązania z jakimkolwiek rekordem poprzez pole ideas
    # w podziale na wszystkie wartości section.
    rekordy_bez_ideas_po_sekcji = (
        Contracts.objects.filter(
            obslugiwana=True, section__isnull=False, czy_wymagana_kontynuacja=True
        )
        .annotate(liczba_ideas=Count("ideas"))
        .filter(liczba_ideas=0)
        .values("section__name")
        .annotate(liczba=Count("id"))
    )

    return {
        "liczba_obslugiwanych_none": liczba_obslugiwanych_none,
        "liczba_section_none": liczba_section_none,
        "rekordy_bez_kontynuacji_po_sekcji": rekordy_bez_kontynuacji_po_sekcji,
        "rekordy_bez_daty_umowy_po_sekcji": rekordy_bez_daty_umowy_po_sekcji,
        "rekordy_bez_ideas_po_sekcji": rekordy_bez_ideas_po_sekcji,
    }
