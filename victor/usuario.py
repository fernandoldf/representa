class Usuario:
    def __init__(self, nome: str, email: str, telefone: str):
        self.nome = nome
        self.email = email
        self.telefone = telefone
        self.privilegios = None

    def __repr__(self):
        return f"Usuario(nome={self.nome!r}, email={self.email!r}, telefone={self.telefone!r}, privilegios={self.privilegios!r})"


class Representante(Usuario):
    def __init__(self, nome: str, email: str, telefone: str):
        super().__init__(nome, email, telefone)
        self.privilegios = 'representante'

    def __repr__(self):
        return f"Representante(nome={self.nome!r}, email={self.email!r}, telefone={self.telefone!r})"


class Aluno(Usuario):
    def __init__(self, nome: str, email: str, telefone: str):
        super().__init__(nome, email, telefone)
        self.privilegios = 'aluno'

    def __repr__(self):
        return f"Aluno(nome={self.nome!r}, email={self.email!r}, telefone={self.telefone!r})"
