"""
server.py
----------
Aplicação Flask mínima usada como interface web para gerenciar representantes
e seus representados (alunos). Este arquivo expõe rotas de login, logout,
dashboard e ações simples (enviar mensagem, adicionar representado).

Comentários neste arquivo seguem estilo de desenvolvedor sênior: explicam
decisões arquiteturais, pontos de extensão e riscos de segurança.

Observações importantes:
- A autenticação aqui é mínima e serve apenas como scaffold; para produção
  substitua pela validação contra um banco de dados e adicione proteção contra
  força bruta / CSRF.
- Sessões são armazenadas usando o mecanismo de sessão do Flask (cookies
  assinados). A chave secreta (`FLASK_SECRET_KEY`) deve ser forte em
  produção e não comitada no repositório.
"""

from flask import Flask, render_template, request, redirect, url_for, flash, session
from dotenv import load_dotenv
from models.usuario import Usuario, Representante, Aluno
from controle_representantes import adicionar_representante, buscar_representante_por_email
import os
from functools import wraps

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('FLASK_SECRET_KEY', 'dev-secret')
app.config['PERMANENT_SESSION_LIFETIME'] = 3600  # 1 hora
app.config['SESSION_COOKIE_HTTPONLY'] = True

def login_required(f):
    """Decorator para verificar se o usuário está logado."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_email' not in session:
            flash('Você precisa estar logado para acessar essa página.', 'warning')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function


def get_usuario_ativo():
    """Recupera o usuário ativo da session."""
    if 'user_email' in session:
        return buscar_representante_por_email(session['user_email'])
    return None

@app.route('/')
def home():
    """Página inicial pública.

    Simplesmente renderiza um template `home.html`. Em aplicações maiores
    pode conter uma landing page ou redirecionar para `/login`.
    """
    return render_template('home.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        usuarioAtivo = buscar_representante_por_email(email)
        if usuarioAtivo is None:
            flash('Usuário não encontrado')
            return redirect(url_for('login'))
        
        # Armazenar na session (em vez de variável global)
        session['user_email'] = email
        session['user_name'] = usuarioAtivo.nome
        session.permanent = True  # Mantém logado enquanto o navegador está aberto
        
        return redirect(url_for('dashboard'))
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    flash('Você foi desconectado com sucesso.', 'info')
    return redirect(url_for('login'))

@app.route('/dashboard')
@login_required
def dashboard():
    usuarioAtivo = get_usuario_ativo()
    if usuarioAtivo:
        usuarioAtivo.atualizar_alunos()
        print(f"Renderizando dashboard para: {usuarioAtivo.nome}")
    return render_template('dashboard.html', usuarioAtivo=usuarioAtivo)

@app.route('/enviar-mensagem', methods=['POST'])
@login_required
def enviar_mensagem():
    usuarioAtivo = get_usuario_ativo()
    assunto = request.form.get('subject')
    corpo = request.form.get('message-content')
    try:
        if usuarioAtivo and usuarioAtivo.enviar_email(assunto, corpo):
            flash('Mensagem enviada com sucesso')
        else:
            flash('Falha ao enviar mensagem')
    except Exception as e:
        flash(f"Erro ao enviar mensagem: {e}")
    return redirect(url_for('dashboard'))

@app.route('/adicionar-representado', methods=['POST'])
@login_required
def adicionar_representado():
    usuarioAtivo = get_usuario_ativo()
    aluno = Aluno(nome=request.form.get('full-name'),
                  email=request.form.get('contact-email'),
                  telefone=request.form.get('phone-number'),
                  representante=usuarioAtivo.nome if usuarioAtivo else None)
    print(f"Adicionando representado: {aluno}")
    if aluno.nome is not None and usuarioAtivo:
        usuarioAtivo.adicionar_aluno(aluno)
    # validações e lógica de salvamento deverão ser implementadas
    flash('Representado adicionado (placeholder)')
    return redirect(url_for('dashboard'))


if __name__ == '__main__':
    app.run(debug=True)
