class Usuario:
    def __init__(self, nome: str, email: str, telefone: str):
        self.nome = nome.lower()
        self.email = email.lower()
        self.telefone = telefone
        self.privilegios = None

    def __repr__(self):
        return f"Usuario(nome={self.nome!r}, email={self.email!r}, telefone={self.telefone!r}, privilegios={self.privilegios!r})"

class Representante(Usuario):
    def __init__(self, nome: str, email: str, telefone: str, senha: str = None):
        super().__init__(nome, email, telefone)
        self.senha = senha
        self.alunos = []
        self.mensagens = []
        self.privilegios = 'representante'
        self.metadata = {}
        self.id = None # Adicionado para suportar rastreamento de ID

    def __repr__(self):
        return f"Representante(nome={self.nome!r}, email={self.email!r}, telefone={self.telefone!r}, alunos={self.alunos!r})"

class Aluno(Usuario):
    def __init__(self, nome: str, email: str, telefone: str, representante: str = None, data_adicionado: str = None):
        super().__init__(nome, email, telefone)
        self.representante = representante
        self.privilegios = 'aluno'
        self.id = None # Adicionado para suportar rastreamento de ID
        self.data_adicionado = data_adicionado

    def __repr__(self):
        return f"Aluno(nome={self.nome!r}, email={self.email!r}, telefone={self.telefone!r}, representante={self.representante!r}, data_adicionado={self.data_adicionado!r})"
