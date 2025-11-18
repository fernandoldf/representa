from models.usuario import Representante

usuarios = [Representante("Fernando", "fernandes.fernando@live.com", "82982234422"),
            Representante("Andrielli", "andrielli@example.com", "82982234423"),
            Representante("Victor", "victor@example.com", "82982234424")]

def adicionar_representante(nome: str, email: str, telefone: str) -> Representante:
    """Adiciona um novo representante à lista de usuários."""
    global usuarios
    novo_representante = Representante(nome, email, telefone)
    usuarios.append(novo_representante)
    return novo_representante

def buscar_representante_por_email(email: str) -> Representante:
    """Busca um representante na lista de usuários pelo email."""
    global usuarios
    for usuario in usuarios:
        if isinstance(usuario, Representante) and usuario.email == email.lower():
            return usuario
    return None