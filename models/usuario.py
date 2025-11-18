class Usuario:
    def __init__(self, nome: str, email: str, telefone: str):
        self.nome = nome.lower()
        self.email = email.lower()
        self.telefone = telefone
        self.privilegios = None

    def __repr__(self):
        return f"Usuario(nome={self.nome!r}, email={self.email!r}, telefone={self.telefone!r}, privilegios={self.privilegios!r})"


class Representante(Usuario):
    def __init__(self, nome: str, email: str, telefone: str):
        
        super().__init__(nome, email, telefone)
        self.alunos = []
        self.privilegios = 'representante'

    def __repr__(self):
        return f"Representante(nome={self.nome!r}, email={self.email!r}, telefone={self.telefone!r}, alunos={self.alunos!r})"
    
    def atualizar_alunos(self):
        from api_googlesheets import API_Sheety
        api = API_Sheety()
        self.alunos = api.buscar_alunos(self.nome)

    def adicionar_aluno(self, aluno):
        from api_googlesheets import API_Sheety
        api = API_Sheety()
        try:
            if api.adicionar_aluno(aluno):
                return True
            else:
                return False
        except Exception as e:
            print(f"Erro ao adicionar aluno: {e}")
            return False
        
    def enviar_email(self, assunto: str, corpo: str):
        from email_sender import EmailSender
        email_sender = EmailSender()
        print(f"Enviando email para os alunos de {self.nome}: assunto='{assunto}', corpo='{corpo}'")
        try:
            if email_sender.send_email([aluno.email for aluno in self.alunos], assunto, corpo):
                print("Email enviado com sucesso")
                return True
            else:
                print("Falha ao enviar email")
                return False
        except Exception as e:
            print(f"Erro ao enviar email: {e}")
            return False


class Aluno(Usuario):
    def __init__(self, nome: str, email: str, telefone: str, representante: str = None):
        super().__init__(nome, email, telefone)
        self.representante = representante
        self.privilegios = 'aluno'

    def __repr__(self):
        return f"Aluno(nome={self.nome!r}, email={self.email!r}, telefone={self.telefone!r}, representante={self.representante!r})"
