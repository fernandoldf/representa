# Estrutura Simplificada - Projeto Representa

## 📁 Estrutura de Diretórios

```
representa/
│
├── server.py                    # [FERNANDO] Servidor Flask + Rotas
│
├── api_googlesheets.py          # [FERNANDO] Lógica Google Sheets API
├── api_twilio.py                # [FERNANDO] Lógica Twilio API
│
├── victor/
│   ├── __init__.py
│   ├── enviar_email.py          # Função para enviar email
│   ├── enviar_whatsapp.py       # Função para enviar WhatsApp
│   └── aluno.py                 # Classe/estrutura de dados do Aluno
│
├── alan/
│   ├── __init__.py
│   ├── style.css                # CSS principal do projeto
│   ├── login.html               # Template da tela de login
│   ├── adicionar_aluno.html     # Template para adicionar aluno
│   └── enviar_mensagem.html     # Template para enviar mensagens
│
├── andrielli/
│   ├── __init__.py
│   ├── validacao.py             # Funções de validação de dados
│   └── README.md                # Documentação do projeto
│
├── static/
│   ├── css/
│   │   └── style.css            # → Symlink ou cópia do alan/style.css
│   └── img/
│       └── logo.png
│
├── templates/
│   ├── login.html               # → Symlink ou cópia do alan/login.html
│   ├── adicionar_aluno.html     # → Symlink ou cópia do alan/adicionar_aluno.html
│   └── enviar_mensagem.html     # → Symlink ou cópia do alan/enviar_mensagem.html
│
├── .env                         # Variáveis de ambiente (NÃO COMMITAR)
├── .gitignore
├── requirements.txt
└── credentials.json             # Credenciais Google (NÃO COMMITAR)
```

---

## 👥 Divisão Clara de Responsabilidades

### 🔧 **Fernando** (Líder Técnico - Infraestrutura)

**Arquivos de Responsabilidade:**
- `server.py` - Servidor Flask + todas as rotas
- `api_googlesheets.py` - Integração com Google Sheets
- `api_twilio.py` - Configuração da API Twilio
- `.env`, `requirements.txt`, `.gitignore`

**Tarefas:**
1. Configurar o servidor Flask
2. Criar as rotas (`/login`, `/adicionar-aluno`, `/enviar-mensagem`)
3. Integrar o trabalho de Victor, Alan e Andrielli
4. Conectar as APIs do Google Sheets e Twilio

---

### 🎨 **Alan** (Interface e Design)

**Pasta de Trabalho:** `alan/`

**Arquivos de Responsabilidade:**
- `alan/style.css` - Todo o CSS do projeto
- `alan/login.html` - Página de login
- `alan/adicionar_aluno.html` - Formulário adicionar aluno
- `alan/enviar_mensagem.html` - Interface enviar mensagens

**Tarefas:**
1. ✅ Criar o design visual (cores, fontes, layout)
2. ✅ Desenvolver os 3 templates HTML
3. ✅ Garantir que os formulários tenham os campos corretos
4. 🔗 Trabalhar com Andrielli na estrutura dos formulários

**O que Alan NÃO precisa saber:**
- Como o Flask funciona
- Como os dados são salvos
- Lógica de Python

**Alan trabalha apenas na pasta `alan/`** - Fernando copia os arquivos prontos para `templates/` e `static/`

---

### 💻 **Victor** (Lógica de Comunicação)

**Pasta de Trabalho:** `victor/`

**Arquivos de Responsabilidade:**
- `victor/enviar_email.py` - Função para enviar email
- `victor/enviar_whatsapp.py` - Função para enviar WhatsApp via Twilio
- `victor/aluno.py` - Estrutura de dados do Aluno (classe ou dicionário)

**Tarefas:**
1. ✅ Criar função `enviar_email(destinatario, assunto, mensagem)`
2. ✅ Criar função `enviar_whatsapp(telefone, mensagem)` usando Twilio
3. ✅ Definir como um "Aluno" é representado no código (classe com nome, email, telefone)

**Estrutura esperada dos arquivos:**

```python
# victor/enviar_email.py
def enviar_email(destinatario, assunto, mensagem):
    # Victor implementa aqui
    pass

# victor/enviar_whatsapp.py
def enviar_whatsapp(telefone, mensagem):
    # Victor implementa aqui usando API Twilio
    pass

# victor/aluno.py
class Aluno:
    def __init__(self, nome, email, telefone):
        # Victor define a estrutura
        pass
```

**Victor trabalha apenas na pasta `victor/`** - Fernando importa as funções no `server.py`

---

### ✅ **Andrielli** (Apoio e Qualidade)

**Pasta de Trabalho:** `andrielli/`

**Arquivos de Responsabilidade:**
- `andrielli/validacao.py` - Funções de validação
- `andrielli/README.md` - Documentação do projeto

**Tarefas:**
1. ✅ Criar funções de validação:
   - `validar_email(email)` - verifica se tem "@"
   - `validar_nome(nome)` - verifica se não está vazio
   - `validar_telefone(telefone)` - verifica formato básico
2. 🔗 Ajudar Alan com a estrutura HTML dos formulários
3. ✅ Manter o README.md atualizado

**Estrutura esperada:**

```python
# andrielli/validacao.py

def validar_email(email):
    """Verifica se o email tem @"""
    if "@" in email and "." in email:
        return True
    return False

def validar_nome(nome):
    """Verifica se o nome não está vazio"""
    if nome and len(nome) > 0:
        return True
    return False

def validar_telefone(telefone):
    """Verifica formato básico do telefone"""
    # Andrielli implementa aqui
    pass
```

**Andrielli trabalha apenas na pasta `andrielli/`** - Fernando importa as validações no `server.py`

---

## 📋 Template do `server.py` (Fernando)

```python
# server.py - Arquivo principal do Fernando

from flask import Flask, render_template, request, redirect, url_for, flash
from dotenv import load_dotenv
import os

# Importa o trabalho dos colegas
from victor.enviar_email import enviar_email
from victor.enviar_whatsapp import enviar_whatsapp
from victor.aluno import Aluno
from andrielli.validacao import validar_email, validar_nome, validar_telefone
import api_googlesheets
import api_twilio

load_dotenv()
app = Flask(__name__)
app.secret_key = os.getenv('FLASK_SECRET_KEY')

# ===== ROTAS =====

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Lógica de login
        pass
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@app.route('/adicionar-aluno', methods=['GET', 'POST'])
def adicionar_aluno():
    if request.method == 'POST':
        nome = request.form.get('nome')
        email = request.form.get('email')
        telefone = request.form.get('telefone')
        
        # Usa as validações da Andrielli
        if not validar_nome(nome):
            flash('Nome inválido!')
            return redirect(url_for('adicionar_aluno'))
        
        if not validar_email(email):
            flash('Email inválido!')
            return redirect(url_for('adicionar_aluno'))
        
        # Cria aluno usando classe do Victor
        novo_aluno = Aluno(nome, email, telefone)
        
        # Salva no Google Sheets
        api_googlesheets.adicionar_aluno(novo_aluno)
        
        flash('Aluno adicionado com sucesso!')
    
    return render_template('adicionar_aluno.html')

@app.route('/enviar-mensagem', methods=['GET', 'POST'])
def enviar_mensagem():
    if request.method == 'POST':
        assunto = request.form.get('assunto')
        mensagem = request.form.get('mensagem')
        tipo = request.form.get('tipo')  # 'email' ou 'whatsapp'
        
        # Busca alunos do Google Sheets
        alunos = api_googlesheets.buscar_alunos()
        
        if tipo == 'email':
            for aluno in alunos:
                # Usa função do Victor
                enviar_email(aluno.email, assunto, mensagem)
        
        elif tipo == 'whatsapp':
            for aluno in alunos:
                # Usa função do Victor
                enviar_whatsapp(aluno.telefone, mensagem)
        
        flash('Mensagens enviadas!')
    
    return render_template('enviar_mensagem.html')

if __name__ == '__main__':
    app.run(debug=True)
```

---

## 🔄 Fluxo de Trabalho no GitHub

### 1. **Cada pessoa trabalha na SUA pasta**

```bash
# Alan modifica apenas alan/
git add alan/
git commit -m "Alan: Atualiza CSS e templates"
git push

# Victor modifica apenas victor/
git add victor/
git commit -m "Victor: Implementa envio de email"
git push

# Andrielli modifica apenas andrielli/
git add andrielli/
git commit -m "Andrielli: Adiciona validação de telefone"
git push
```

### 2. **Sem conflitos!**
Como cada um trabalha em pastas diferentes, **não há conflitos no Git** 🎉

### 3. **Fernando integra tudo**
```bash
# Fernando copia os arquivos prontos para os lugares corretos
cp alan/style.css static/css/
cp alan/*.html templates/

# E importa as funções no server.py
```

---

## ✅ Checklist de Tarefas por Pessoa

### Fernando
- [ ] Criar `server.py` com as rotas
- [ ] Criar `api_googlesheets.py`
- [ ] Criar `api_twilio.py`
- [ ] Integrar o trabalho de todos
- [ ] Configurar `.env` e `requirements.txt`

### Alan
- [ ] Criar `alan/style.css` com o design
- [ ] Criar `alan/login.html`
- [ ] Criar `alan/adicionar_aluno.html`
- [ ] Criar `alan/enviar_mensagem.html`
- [ ] Trabalhar com Andrielli nos formulários

### Victor
- [ ] Criar `victor/enviar_email.py`
- [ ] Criar `victor/enviar_whatsapp.py`
- [ ] Criar `victor/aluno.py`

### Andrielli
- [ ] Criar `andrielli/validacao.py` com 3 funções
- [ ] Ajudar Alan com HTML dos formulários
- [ ] Criar `andrielli/README.md`

---

## 📝 Template do README.md (Andrielli)

```markdown
# Representa - Sistema para Representantes de Turma

## Como Rodar o Projeto

1. Clone o repositório:
   ```bash
   git clone https://github.com/seu-usuario/representa.git
   cd representa
   ```

2. Crie um ambiente virtual:
   ```bash
   python -m venv venv
   ```

3. Ative o ambiente virtual:
   - Windows: `venv\Scripts\activate`
   - Linux/Mac: `source venv/bin/activate`

4. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```

5. Configure o arquivo `.env` com suas credenciais

6. Rode a aplicação:
   ```bash
   python server.py
   ```

7. Acesse no navegador: `http://localhost:5000`

## Equipe

- **Fernando**: Infraestrutura e Integração
- **Alan**: Design e Interface
- **Victor**: Lógica de Comunicação
- **Andrielli**: Validação e Documentação
```

---

## 🎯 Vantagens desta Estrutura

✅ **Zero conflitos no Git** - cada um tem sua pasta
✅ **Fácil de entender** - cada pessoa sabe exatamente onde trabalhar
✅ **Independência** - Victor não precisa esperar Alan terminar
✅ **Baixa curva de aprendizado** - pessoas sem experiência conseguem contribuir
✅ **Fácil de testar** - Fernando pode testar cada parte separadamente

---

## 🚀 Ordem de Desenvolvimento Recomendada

1. **Semana 1**: Todos criam a estrutura de suas pastas
2. **Semana 2**: 
   - Victor implementa as funções
   - Alan cria os templates HTML básicos
   - Andrielli cria as validações
3. **Semana 3**: Fernando integra tudo no `server.py`
4. **Semana 4**: Testes e ajustes finais