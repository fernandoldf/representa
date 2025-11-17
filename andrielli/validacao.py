"""Validações básicas de entrada."""

def validar_email(email: str) -> bool:
    if not email:
        return False
    return "@" in email and "." in email


def validar_nome(nome: str) -> bool:
    return bool(nome and nome.strip())


def validar_telefone(telefone: str) -> bool:
    if not telefone:
        return False
    digits = [c for c in telefone if c.isdigit()]
    return 8 <= len(digits) <= 15
