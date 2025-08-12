import re  # Biblioteca para expressões regulares


def is_valid_username(username):
    """
    Verifica se o nome de usuário é válido:
    - Deve conter apenas letras (maiúsculas ou minúsculas), números,
      e os caracteres _ . -
    - Deve ter entre 3 e 20 caracteres.
    """
    pattern = r'^[a-zA-Z0-9_.-]{3,20}$'
    # Retorna True se combinar com o padrão
    return re.match(pattern, username) is not None


def is_valid_password(password):
    """
    Verifica se a senha é válida:
    - Deve ter comprimento entre 6 e 50 caracteres.
    """
    return 6 <= len(password) <= 50
