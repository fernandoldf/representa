"""Controller/utility for managing representantes.

This module used to hold an in-memory list. It now delegates persistence to
`representados_db.JSONRepository` and converts stored dicts into model objects
(`Representante`, `Aluno`). The public API remains the same (add and lookup
by email) which keeps existing call sites unchanged.
"""

from models.usuario import Representante, Aluno
from controle_db import JSONRepository

# Initialize repository using the JSON file at project root
_repo = JSONRepository('db.json')


def _dict_to_representante(d: dict) -> Representante:
    """Convert a stored dictionary into a `Representante` model instance.

    The repository stores simple dicts; higher layers in the app expect
    model instances so we create them here. We preserve aluno entries by
    converting them to `Aluno` objects.
    """
    rep = Representante(d.get('nome', ''), d.get('email', ''), d.get('telefone', ''))
    # preserve identifier from storage
    rep.id = d.get('id')
    # Convert and attach alunos (if any)
    for a in d.get('alunos', []):
        aluno_obj = Aluno(a.get('nome'), a.get('email'), a.get('telefone'), representante=rep.nome)
        aluno_obj.id = a.get('id')
        rep.alunos.append(aluno_obj)
    return rep


def adicionar_representante(nome: str, email: str, telefone: str) -> Representante:
    """Adiciona um novo representante no JSON repository e retorna o modelo."""
    rep_dict = _repo.add_representante(nome, email, telefone)
    return _dict_to_representante(rep_dict)


def buscar_representante_por_email(email: str) -> Representante:
    """Busca um representante no JSON repository pelo email e retorna modelo.

    Returns None if not found.
    """
    d = _repo.get_representante_by_email(email)
    if d:
        return _dict_to_representante(d)
    return None


def adicionar_representado_para(representante_email: str, nome: str, email: str, telefone: str):
    """Adiciona um representado (aluno) ao representante identificado por email.

    Retorna o objeto `Aluno` criado.
    """
    aluno_dict = _repo.add_aluno(representante_email, nome, email, telefone)
    # convert to model Aluno and return
    rep = buscar_representante_por_email(representante_email)
    if rep:
        # find aluno in rep.alunos matching id
        for a in rep.alunos:
            if getattr(a, 'email', None) == aluno_dict.get('email'):
                return a
    # fallback: return as dict when model not found
    return aluno_dict


def atualizar_representado(representante_email: str, aluno_id: str, updates: dict):
    """Atualiza dados do aluno (por id) e retorna o aluno atualizado como dict."""
    updated = _repo.update_aluno(representante_email, aluno_id, updates)
    return updated


def remover_representado(representante_email: str, aluno_id: str) -> bool:
    """Remove um aluno por id. Retorna True se removido."""
    return _repo.remove_aluno_by_id(representante_email, aluno_id)