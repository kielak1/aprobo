# general/models/__init__.py

from .models import (
    Parametry,
    Note,
    Sections,
    Clients,
    Status_procesu,
    Status_akceptacji,
    Pilnosc,
    Crip,
    Sposob_zakupu,
    Acceptor,
    Sposob_wyceny,
    Zgodnosc_mapy,
    Rodzaj_inicjatywy,
    Priorytet_inicjatywy,
    Rodzaje_uslug,
    Klasyfikacja_zmiany,
    Poziomy_dostepnosci,
    Dostepnosci_rozwiazania,
    MaileDoWyslania,
)

from .zapytania import (
    Zapytanie,
)

from .services import (
    zlecenia_kontrolingowe,
    uslugi,
)

from .raporty import (
    Planowane_zakupy,
)

from .performance import (
    Stamp,
)

from .rada import (
    Meeting,
    Resolution,
    MeetingStatus,
)

from .proces import (
    Variable,
)

