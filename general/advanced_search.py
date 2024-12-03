from lark import Lark, Transformer
from general.views_full_search import (
    note_tresc,
    full_search,
    dopelnienie,
    suma,
    przeciecie,
    owner,
)
import logging

# Konfiguracja logowania
logging.basicConfig(level=logging.DEBUG)

stack = []

# Definicja gramatyki
query_grammar = """
    start: zapytanie

    zapytanie:  funkcja argument  
             | NOT zapytanie 
             | AND zapytanie (zapytanie)+
             | OR zapytanie (zapytanie)+
             | "(" zapytanie ")"

    argument: CNAME | CUST_STRING
    CUST_STRING: /[0-9a-zA-ZąćęłńóśźżĄĆĘŁŃÓŚŹŻ!@#$>%^&*\-+=\\'\/\[\]\{\} ]+/
    funkcja: FULL | NOTE_TRESC | OWNER
    FULL: "FULL"
    NOTE_TRESC: "NOTE_TRESC"
    OWNER: "OWNER"
    NOT: "NOT"
    AND: "AND"
    OR: "OR"
    %import common.CNAME
    %import common.WS
    %ignore WS
"""

# Definicja parsera Lark
parser = Lark(query_grammar, start="start", parser="earley", debug=True)


# Transformer do przetwarzania wyników parsowania
class QueryTransformer(Transformer):
    def zapytanie(self, items):
        if items[0] == "OR":
            l_arg = len(items) - 1
            krotka1 = stack.pop()
            krotka2 = stack.pop()
            sum = suma(krotka1, krotka2)
            stack.append(sum)
            l_arg = l_arg - 2
            while l_arg > 0:
                krotka1 = stack.pop()
                krotka2 = stack.pop()
                sum = suma(krotka1, krotka2)
                stack.append(sum)
                l_arg = l_arg - 1
        elif items[0] == "AND":
            l_arg = len(items) - 1
            krotka1 = stack.pop()
            krotka2 = stack.pop()
            prze = przeciecie(krotka1, krotka2)
            stack.append(prze)
            l_arg = l_arg - 2
            while l_arg > 0:
                krotka1 = stack.pop()
                krotka2 = stack.pop()
                prze = przeciecie(krotka1, krotka2)
                stack.append(prze)
                l_arg = l_arg - 1
        elif items[0] == "NOT":
            krotka = stack.pop()
            dop = dopelnienie(krotka)
            stack.append(dop)
        elif items[0] == "FULL":
            krotka = full_search(items[1])
            stack.append(krotka)
        elif items[0] == "NOTE_TRESC":
            krotka = note_tresc(items[1])
            stack.append(krotka)
        elif items[0] == "OWNER":
            krotka = owner(items[1])
            stack.append(krotka)

        else:
            pass
        if len(items) == 1:
            return items[0]
        if len(items) == 2:
            if items[0] == "FULL":
                return f"full({items[1]})"
            elif items[0] == "NOTE_TRESC":
                return f"note_tresc({items[1]})"
            elif items[0] == "OWNER":
                return f"owner({items[1]})"
            elif items[0] == "NOT":
                return f"not({items[1]})"
        elif len(items) == 3:
            if items[0] == "AND":
                return f"and({items[1]}, {items[2]})"
            elif items[0] == "OR":
                return f"or({items[1]}, {items[2]})"
        return items

    def funkcja(self, items):
        return items[0]

    def argument(self, item):
        return str(item[0])

    def NOT(self, items):
        return "NOT"

    def AND(self, items):
        return "AND"

    def OR(self, items):
        return "OR"

    def FULL(self, items):
        return "FULL"

    def NOTE_TRESC(self, items):
        return "NOTE_TRESC"


def search_advanced(query):
    global stack
    stack.clear()  # Clear the stack at the beginning
    try:
        # logging.debug(f"Parsowanie zapytania: {query}")
        parsed = parser.parse(query)
        # print(parsed.pretty())
        result = QueryTransformer().transform(parsed)
        # logging.debug(f"Stack after transformation: {stack}")
        return stack.pop(), parsed.pretty()
    except Exception as e:
        print(f"Błąd podczas parsowania zapytania '{query}': {e}")
