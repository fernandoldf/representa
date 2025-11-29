import controle_db
repo = controle_db.JSONRepository('db.json')

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
    
    def buscar_dos_forms(self):
        from services.api_googlesheets import API_Sheety
        api = API_Sheety()
        return api.buscar_alunos(nome=self.nome)

    def atualizar_alunos(self):
        alunos_forms = self.buscar_dos_forms()
        global repo
        if alunos_forms is not None:
            for n in alunos_forms:
                if not repo.check_aluno_exists(self.email, n['eMail']):
                    aluno = Aluno(nome=n['nome'], email=n['eMail'], telefone=n['telefone'], representante=self.nome)
                    repo.add_aluno(self.email, aluno.nome, aluno.email, aluno.telefone)
    
    def carregar_alunos(self):
        global repo
        self.atualizar_alunos()
        alunos_dicts = repo.get_alunos_of_representante(self.email)
        for aluno_dict in alunos_dicts:
            aluno_obj = Aluno(aluno_dict.get('nome'), aluno_dict.get('email'), aluno_dict.get('telefone'), representante=self.nome)
            self.alunos.append(aluno_obj)

    def adicionar_aluno(self, aluno):
        if aluno.email not in [a.email for a in self.alunos]:           
            self.alunos.append(aluno)
            aluno.representante = self
            global repo
            repo.add_aluno(self.email, aluno.nome, aluno.email, aluno.telefone)
            return True
        return False
    
    def remover_aluno(self, aluno_email):
        for aluno in self.alunos:
            if aluno.email == aluno_email:
                self.alunos.remove(aluno)
                global repo
                repo.remove_aluno(self.email, aluno_email)
                return True
        return False

        
    def enviar_email(self, assunto: str, corpo: str):
        from services.email_sender import EmailSender
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
