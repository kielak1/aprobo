def w_EZZ(status_EZZ):
    akceptowane_statusy = {
        "Akceptacja CIO",
        "Akceptacja Dyrektora Biura",
        "Akceptacja merytoryczna",
        "Akceptacja Przełożonego",
        "Opiniowanie dla Przełożonego",
        "Cofnięty do Dyrektora",
        "Cofnięty do Zlecającego",
        "Kontrola finansowa",
        "Weryfikacja Vendor Managera",
        "Rejestracja w SRM/SAP CP",
    }
    return status_EZZ in akceptowane_statusy


def auto_status_zakupu(status_zakupu, status_EZZ):
    if w_EZZ(status_EZZ):
        return "w EZZ"
    match status_zakupu:
        case "w realizacji":
            return status_zakupu
        case "zakończony":
            return status_zakupu
        case "w zakupach":
            if status_EZZ == "Odrzucony" or status_EZZ == "Anulowany":
                return "anulowany"
            else:
                return status_zakupu
        case "zakup BGNIG":
            return status_zakupu
        case "anulowany":
            return status_zakupu
        case "roboczy":
            if status_EZZ == "Odrzucony" or status_EZZ == "Anulowany":
                return "anulowany"
            elif status_EZZ == "Zarejestrowany w SRM/SAP CP":
                return "w zakupach"
            else:
                return status_zakupu

        case "w akceptacji":
            return status_zakupu
        case "w EZZ":
            match status_EZZ:
                case "Odrzucony":
                    return "anulowany"
                case "Roboczy":
                    return "roboczy"
                case "Zarejestrowany w SRM/SAP CP":
                    return "w zakupach"
                case "Anulowany":
                    return "anulowany"
                case _:
                    return status_zakupu
        case _:
            return status_zakupu
