import json
from werkzeug.security import generate_password_hash, check_password_hash

USERS_FILE = "users.json"  # Arquivo JSON onde os usuários serão armazenados


def load_users():
    """
    Carrega os usuários do arquivo JSON.
    Retorna um dicionário {username: hashed_password}.
    Se o arquivo não existir ou estiver inválido, retorna dicionário vazio.
    """
    try:
        with open(USERS_FILE, "r") as f:
            return json.load(f)  # Lê e converte JSON em dicionário Python
    except (FileNotFoundError, json.JSONDecodeError):
        return {}  # Arquivo não encontrado ou JSON inválido retorna vazio


def save_users(users):
    """
    Salva o dicionário de usuários no arquivo JSON,
    formatado com indentação para facilitar leitura manual.
    """
    with open(USERS_FILE, "w") as f:
        json.dump(users, f, indent=4)


def register_user(username, password):
    """
    Registra um novo usuário:
    - Carrega usuários atuais.
    - Verifica se username já existe; se sim, retorna False.
    - Gera hash seguro da senha usando werkzeug.security.
    - Salva o usuário com senha hasheada no arquivo JSON.
    - Retorna True se sucesso.
    """
    users = load_users()
    if username in users:
        return False
    users[username] = generate_password_hash(password)
    save_users(users)
    return True


def verify_user(username, password):
    """
    Verifica se usuário e senha são válidos:
    - Carrega usuários.
    - Verifica se username existe.
    - Compara senha fornecida com hash salvo usando check_password_hash.
    - Retorna True se senha confere, False caso contrário.
    """
    users = load_users()
    if username not in users:
        return False
    return check_password_hash(users[username], password)
