import socket


def generate_need_url(id_potrzeby):
    hostname = socket.gethostname()
    base_url = f"https://{hostname}/needs/wszystkiepotrzeby/edit_need_short/"
    need_url = f"{base_url}?need_id={id_potrzeby}"
    return need_url


def generate_purchase_url(id_zakupu):
    hostname = socket.gethostname()
    base_url = f"https://{hostname}/purchases/wszystkiezakupy/edit_purchase_short/"
    need_url = f"{base_url}?purchase_id={id_zakupu}"
    return need_url


def generate_contract_url(id_umowy):
    hostname = socket.gethostname()
    base_url = f"https://{hostname}/contracts/wszystkieumowy/edit_contract_short/"
    need_url = f"{base_url}?contract_id={id_umowy}"
    return need_url


def generate_idea_url(id_pomyslu):
    hostname = socket.gethostname()
    base_url = f"https://{hostname}/ideas/wszystkiepomysly/edit_idea_short/"
    need_url = f"{base_url}?idea_id={id_pomyslu}"
    return need_url


def generate_user_url(id_user):
    hostname = socket.gethostname()
    user_url = f"https://{hostname}/general/myadmin/auth/user/{id_user}/change/"
    return user_url
