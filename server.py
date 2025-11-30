"""
server.py
----------
Aplicação Flask principal que atua como o backend e interface web do sistema Representa.

Este arquivo é responsável por:
1.  Configurar a aplicação Flask e suas extensões.
2.  Definir as rotas (URLs) acessíveis pelos usuários.
3.  Gerenciar a autenticação e sessão dos usuários.
4.  Interagir com a camada de serviço (`RepresentanteService`) para processar dados.
5.  Renderizar os templates HTML para o frontend.

Arquitetura:
- **Padrão MVC (Model-View-Controller)**: Embora simplificado, este arquivo atua principalmente como o 'Controller', recebendo requisições, chamando a lógica de negócios (Service) e retornando a visualização (Templates).
- **Autenticação**: Utiliza sessões baseadas em cookies assinados do Flask. É uma abordagem simples e eficaz para aplicações menores, mas em produção deve ser reforçada com HTTPS e flags de segurança nos cookies.
- **Persistência**: Delega a persistência de dados para o `RepresentanteService`, mantendo o código da rota limpo e focado no fluxo HTTP.

Segurança:
- As rotas protegidas são decoradas com `@login_required` para garantir que apenas usuários autenticados tenham acesso.
- Senhas são armazenadas como hashes SHA-256 (nota: para produção, recomenda-se algoritmos mais robustos como bcrypt ou Argon2).
"""

from flask import Flask, render_template, request, redirect, url_for, flash, session
from dotenv import load_dotenv
from models.usuario import Usuario, Representante, Aluno
from services.controle_representates import service
import hashlib
import os
from functools import wraps

# Carrega variáveis de ambiente do arquivo .env (ex: chaves secretas, configurações de email)
load_dotenv()

app = Flask(__name__)

# Configuração da chave secreta para assinar cookies de sessão.
# Em produção, isso DEVE ser uma string aleatória longa e mantida em segredo.
app.secret_key = os.getenv('FLASK_SECRET_KEY', 'dev-secret')

# Configurações de Sessão
app.config['PERMANENT_SESSION_LIFETIME'] = 3600  # Sessão expira em 1 hora de inatividade
app.config['SESSION_COOKIE_HTTPONLY'] = True     # Previne acesso ao cookie via JavaScript (proteção XSS)

def login_required(f):
    """
    Decorator personalizado para proteger rotas que exigem autenticação.
    
    Verifica se a chave 'user_email' está presente na sessão. Se não estiver,
    redireciona o usuário para a página de login com uma mensagem de aviso.
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_email' not in session:
            flash('Você precisa estar logado para acessar essa página.', 'warning')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function


def get_usuario_ativo():
    """
    Helper para recuperar o objeto Representante completo do usuário logado atualmente.
    
    Retorna:
        Representante: Objeto com todos os dados do usuário (alunos, mensagens, etc).
        None: Se não houver usuário logado.
    """
    if 'user_email' in session:
        return service.retornar_representante(session['user_email'])
    return None

@app.route('/')
def home():
    """
    Rota da Página Inicial (Landing Page).
    
    Acessível publicamente. Serve como ponto de entrada para novos usuários ou
    para quem não está logado.
    """
    return render_template('home.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    """
    Rota de Login.
    
    GET: Renderiza o formulário de login.
    POST: Processa as credenciais enviadas.
          - Busca o usuário pelo email.
          - Compara o hash da senha fornecida com o hash armazenado.
          - Se sucesso, cria a sessão e redireciona para o dashboard.
    """
    if request.method == 'POST':
        email = request.form.get('email')
        dados_user = service.buscar_representante_por_email(email)
        
        if dados_user is None:
            flash('Usuário não encontrado')
            return redirect(url_for('login'))
            
        senha = request.form.get('password')
        # Hash da senha para comparação segura
        senha_hash = hashlib.sha256(senha.encode()).hexdigest()
        
        if dados_user.get('senha') != senha_hash:
            flash('Senha incorreta')
            return redirect(url_for('login'))
            
        # Login bem-sucedido: Armazena identificadores na sessão
        session['user_email'] = email
        session['user_name'] = dados_user.get('name')
        session.permanent = True  # Ativa a expiração da sessão configurada anteriormente
        
        return redirect(url_for('dashboard'))
        
    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    """
    Rota de Cadastro de Novos Representantes.
    
    Permite que novos representantes criem uma conta no sistema.
    """
    if request.method == 'POST':
        nome = request.form.get('nome')
        email = request.form.get('email')
        telefone = request.form.get('telefone')
        senha = request.form.get('password')
        
        # Hash da senha antes de salvar no banco de dados
        senha_hash = hashlib.sha256(senha.encode()).hexdigest()
        
        try:
            service.adicionar_representante(nome, email, telefone, senha_hash)
            flash('Representante cadastrado com sucesso. Faça login.')
            return redirect(url_for('login'))
        except Exception as e:
            flash(f'Erro ao cadastrar representante: {e}', 'danger')
            return redirect(url_for('signup'))
            
    return render_template('signup.html')

@app.route('/logout')
def logout():
    """
    Rota de Logout.
    
    Limpa a sessão do usuário, efetivamente desconectando-o, e redireciona para o login.
    """
    session.clear()
    flash('Você foi desconectado com sucesso.', 'info')
    return redirect(url_for('login'))

@app.route('/dashboard')
@login_required
def dashboard():
    """
    Rota do Painel Principal (Dashboard).
    
    Exibe a visão geral para o representante logado, incluindo:
    - Estatísticas (total de alunos, mensagens).
    - Gráficos de desempenho.
    - Ações rápidas.
    
    Esta rota agrega dados de várias fontes (Service, ChartService) para passar
    um contexto rico para o template renderizar.
    """
    usuarioAtivo = get_usuario_ativo()
    if usuarioAtivo:
        print(f"Renderizando dashboard para: {usuarioAtivo.nome}")
        
        # --- Agregação de Dados para Gráficos ---
        # Chama o serviço especializado em gráficos para processar os dados brutos
        # e transformá-los em formatos consumíveis pelo Chart.js (listas de labels e valores).
        from services.chart_service import get_dashboard_chart_data
        chart_data = get_dashboard_chart_data(usuarioAtivo)

        return render_template('dashboard.html', 
                               usuarioAtivo=usuarioAtivo,
                               msg_chart_labels=chart_data['msg_chart_labels'],
                               msg_chart_values=chart_data['msg_chart_values'],
                               student_chart_labels=chart_data['student_chart_labels'],
                               student_chart_values=chart_data['student_chart_values'],
                               new_students_last_7_days=chart_data['new_students_last_7_days'])
    
    # Fallback caso algo estranho aconteça e não haja usuário ativo (embora o decorator previna)
    return render_template('dashboard.html', usuarioAtivo=usuarioAtivo)

@app.route('/enviar-mensagem', methods=['POST'])
@login_required
def enviar_mensagem():
    """
    Rota para Envio de Mensagens (Anúncios).
    
    Recebe os dados do formulário de envio de mensagem e delega para o serviço
    de email realizar o disparo real.
    """
    usuarioAtivo = get_usuario_ativo()
    assunto = request.form.get('subject')
    corpo = request.form.get('message-content')
    
    try:
        if usuarioAtivo and service.enviar_mensagem(usuarioAtivo, assunto, corpo):
            flash('Mensagem enviada com sucesso')
        else:
            flash('Falha ao enviar mensagem')
    except Exception as e:
        flash(f"Erro ao enviar mensagem: {e}")
        
    return redirect(url_for('dashboard'))

@app.route('/adicionar-representado', methods=['POST'])
@login_required
def adicionar_representado():
    """
    Rota para Adicionar Manualmente um Representado (Aluno).
    
    Permite que o representante cadastre um aluno diretamente pelo dashboard.
    """
    usuarioAtivo = get_usuario_ativo()
    
    if not usuarioAtivo:
        flash('Nenhum representante ativo', 'danger')
        return redirect(url_for('dashboard'))

    nome = request.form.get('full-name')
    email = request.form.get('contact-email')
    telefone = request.form.get('phone-number')

    try:
        service.adicionar_aluno(usuarioAtivo.email, nome, email, telefone)
        flash('Representado adicionado com sucesso', 'success')
    except Exception as e:
        flash(f'Erro ao adicionar representado: {e}', 'danger')
        
    return redirect(url_for('dashboard'))

@app.route('/representado/edit', methods=['POST'])
@login_required
def editar_representado():
    """
    Rota para Editar Dados de um Representado.
    
    Atualiza informações (nome, email, telefone) de um aluno existente.
    """
    usuarioAtivo = get_usuario_ativo()
    if not usuarioAtivo:
        flash('Nenhum representante ativo', 'danger')
        return redirect(url_for('dashboard'))

    aluno_id = request.form.get('aluno_id')
    nome = request.form.get('edit-nome')
    email = request.form.get('edit-email')
    telefone = request.form.get('edit-telefone')

    # Constrói dicionário apenas com os campos que foram preenchidos
    updates = {}
    if nome:
        updates['nome'] = nome
    if email:
        updates['email'] = email
    if telefone:
        updates['telefone'] = telefone

    try:
        service.atualizar_aluno(usuarioAtivo.email, aluno_id, updates)
        flash('Representado atualizado com sucesso', 'success')
    except Exception as e:
        flash(f'Erro ao atualizar representado: {e}', 'danger')
        
    return redirect(url_for('dashboard'))


@app.route('/representado/delete', methods=['POST'])
@login_required
def deletar_representado():
    """
    Rota para Remover um Representado.
    
    Exclui permanentemente um aluno da lista do representante.
    """
    usuarioAtivo = get_usuario_ativo()
    if not usuarioAtivo:
        flash('Nenhum representante ativo', 'danger')
        return redirect(url_for('dashboard'))

    aluno_id = request.form.get('aluno_id')
    try:
        removed = service.remover_aluno(usuarioAtivo.email, aluno_id)
        if removed:
            flash('Representado removido com sucesso', 'success')
        else:
            flash('Representado não encontrado', 'warning')
    except Exception as e:
        flash(f'Erro ao remover representado: {e}', 'danger')
        
    return redirect(url_for('dashboard'))


@app.route('/registrar', methods=['GET', 'POST'])
def registrar_aluno():
    """
    Rota Pública de Auto-Cadastro de Alunos.
    
    Permite que alunos se cadastrem sozinhos, escolhendo seu representante
    a partir de uma lista. Útil para divulgar um link e captar contatos.
    """
    if request.method == 'POST':
        nome = request.form.get('nome')
        email = request.form.get('email')
        telefone = request.form.get('telefone')
        representante_email = request.form.get('representante_email')

        try:
            service.adicionar_aluno(representante_email, nome, email, telefone)
            flash('Cadastro realizado com sucesso! Aguarde contato do seu representante.', 'success')
        except Exception as e:
            flash(f'Erro ao realizar cadastro: {e}', 'danger')
        return redirect(url_for('registrar_aluno'))
    
    # GET request: Renderiza o formulário público com a lista de representantes disponíveis
    representantes = service.listar_representantes()
    return render_template('public_form.html', representantes=representantes)


if __name__ == '__main__':
    # Inicia o servidor de desenvolvimento do Flask
    # debug=True permite reload automático em alterações de código e mensagens de erro detalhadas
    app.run(debug=True)
