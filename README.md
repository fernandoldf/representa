# Representa - Sistema de Gestão para Representantes de Turma

O **Representa** é uma aplicação web desenvolvida em Python com Flask, projetada para auxiliar representantes de turma na gestão de alunos e comunicação eficiente. O sistema centraliza informações, facilita o envio de comunicados e oferece uma visão geral da turma através de um dashboard intuitivo.

## 🚀 Funcionalidades

- **Dashboard Interativo**: Visualização rápida de estatísticas da turma, incluindo total de alunos e mensagens enviadas, com gráficos dinâmicos.
- **Gestão de Alunos (Representados)**:
  - Adicionar novos alunos manualmente.
  - Editar informações de contato (email, telefone).
  - Remover alunos da lista.
- **Auto-Cadastro Público**: Página pública onde os próprios alunos podem se cadastrar e selecionar seu representante.
- **Comunicação em Massa**:
  - Envio de emails para toda a turma ou alunos selecionados.
  - Integração preparada para envio de mensagens via WhatsApp (Twilio).
- **Autenticação Segura**: Sistema de login e cadastro para representantes, com proteção de rotas e sessões seguras.

## 🛠️ Tecnologias Utilizadas

- **Backend**: Python 3, Flask
- **Frontend**: HTML5, CSS3, JavaScript (Chart.js para gráficos)
- **Banco de Dados**: TinyDB (Armazenamento local em JSON) / Integração com Google Sheets (Opcional/Legado)
- **Serviços**:
  - **Email**: SMTP (Gmail/Outlook)
  - **WhatsApp**: Twilio API

## 📦 Estrutura do Projeto

```
representa/
├── server.py                    # Aplicação principal Flask e rotas
├── controle_db.py               # Gerenciamento direto do banco de dados
├── db.json                      # Arquivo de banco de dados (TinyDB)
├── models/                      # Modelos de dados (Usuario, Aluno, Representante)
├── services/                    # Lógica de negócios
│   ├── controle_representates.py # Serviço principal de gestão
│   ├── chart_service.py          # Geração de dados para gráficos
│   └── email_sender.py           # Envio de emails
├── static/                      # Arquivos estáticos (CSS, Imagens, JS)
├── templates/                   # Templates HTML (Jinja2)
└── requirements.txt             # Dependências do projeto
```

## 🔧 Como Rodar o Projeto

### Pré-requisitos

- Python 3.8 ou superior
- Git

### Passo a Passo

1. **Clone o repositório**
   ```bash
   git clone https://github.com/seu-usuario/representa.git
   cd representa
   ```

2. **Crie e ative um ambiente virtual**
   - Windows:
     ```bash
     python -m venv venv
     venv\Scripts\activate
     ```
   - Linux/macOS:
     ```bash
     python3 -m venv venv
     source venv/bin/activate
     ```

3. **Instale as dependências**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure as Variáveis de Ambiente**
   Crie um arquivo `.env` na raiz do projeto e adicione as seguintes configurações (ajuste conforme necessário):

   ```env
   # Configurações do Flask
   FLASK_SECRET_KEY=sua_chave_secreta_super_segura

   # Configurações de Email (Exemplo Gmail)
   EMAIL_ADDRESS=seu_email@gmail.com
   EMAIL_PASSWORD=sua_senha_de_app
   
   # Configurações Twilio (Opcional)
   TWILIO_ACCOUNT_SID=seu_sid
   TWILIO_AUTH_TOKEN=seu_token
   TWILIO_PHONE_NUMBER=seu_numero_twilio
   ```

5. **Execute a aplicação**
   ```bash
   python server.py
   ```

6. **Acesse no navegador**
   Abra `http://localhost:5000` para ver a aplicação rodando.

## 👥 Contribuição

Este projeto foi desenvolvido com uma divisão clara de responsabilidades:
- **Infraestrutura & Backend**: Fernando
- **Frontend & Design**: Alan
- **Lógica de Comunicação**: Victor
- **Validação & Documentação**: Andrielli

## 📄 Licença

Este projeto está sob a licença [MIT](LICENSE).
