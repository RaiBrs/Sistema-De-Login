from flask import Flask, render_template, request, redirect, url_for, flash, session
# Funções para cadastro e verificação do usuário
from auth import register_user, verify_user
# Validação simples de usuário e senha
from validators import is_valid_username, is_valid_password
from functools import wraps
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)
# item secreto para sessão e flashes
app.secret_key = os.getenv("SECRET_KEY", "chave_padrao")

DOMAIN = "@secureserv"    # Sufixo fixo que será adicionado ao nome de usuário

# Decorator para proteger rotas que exigem login


def login_required(f):
    @wraps(f)
    def wrap(*a, **kw):
        if "user" not in session:  # Verifica se usuário está logado
            flash("Faça login!")
            return redirect(url_for("login"))
        return f(*a, **kw)
    return wrap

# Rota principal, redireciona para login


@app.route("/")
def home():
    return redirect(url_for("login"))

# Rota de login, aceita GET para mostrar formulário e POST para processar dados


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        # Pega o nome do usuário, tira espaços
        user = request.form["user"].strip()
        pw = request.form["pw"]              # Pega a senha

        # Adiciona o sufixo fixo ao usuário
        full_user = f"{user}{DOMAIN}"

        # Validações simples de formato de usuário e senha
        if not is_valid_username(user):
            flash("Usuário inválido! Use letras, números, _ . - (3-20 caracteres).")
            return render_template("login.html")
        if not is_valid_password(pw):
            flash("Senha inválida! Deve ter entre 6 e 50 caracteres.")
            return render_template("login.html")

        # Verifica se o usuário e senha conferem
        if verify_user(full_user, pw):
            session["user"] = full_user      # Guarda o usuário na sessão
            # Redireciona para página de agradecimento
            return redirect(url_for("obrigado"))
        flash("Usuário ou senha inválidos!")
    return render_template("login.html")   # Renderiza o formulário de login

# Rota para registrar novo usuário, aceita GET e POST


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        user = request.form["user"].strip()  # Pega e limpa nome de usuário
        pw = request.form["pw"]              # Pega senha

        full_user = f"{user}{DOMAIN}"        # Adiciona sufixo

        # Validações para formato válido
        if not is_valid_username(user):
            flash("Usuário inválido! Use letras, números, _ . - (3-20 caracteres).")
            return render_template("register.html")
        if not is_valid_password(pw):
            flash("Senha inválida! Deve ter entre 6 e 50 caracteres.")
            return render_template("register.html")

        # Tenta registrar usuário; se já existir, dá erro
        if register_user(full_user, pw):
            flash(f"Cadastro feito para {full_user}! Faça login.")
            return redirect(url_for("login"))
        flash("Usuário já existe!")
    return render_template("register.html")  # Mostra formulário de cadastro

# Página de agradecimento, só acessível se estiver logado


@app.route("/obrigado")
@login_required
def obrigado():
    full_user = session["user"]               # Pega usuário da sessão
    user_id = full_user.replace(DOMAIN, "")  # Remove sufixo para exibir só ID
    # Renderiza página com usuário
    return render_template("obg.html", user=user_id)

# Rota para logout — limpa a sessão e mostra página de saída


@app.route("/logout")
def logout():
    session.clear()
    return render_template("logout.html")


if __name__ == "__main__":
    # Roda a aplicação em modo debug para facilitar desenvolvimento
    app.run(debug=True)
