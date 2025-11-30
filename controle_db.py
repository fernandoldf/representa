"""Repositório baseado em JSON para `representados.json`.

Esta classe fornece operações simples de carga/salvamento atômico e auxiliares CRUD para tratar
`representados.json` como um armazenamento persistente leve.

Notas:
- Usa um bloqueio de arquivo para evitar corrupção por escrita simultânea (requer filelock).
- As escritas são atômicas (escreve em arquivo temporário depois os.replace).
"""
from __future__ import annotations

import json
import os
import tempfile
from datetime import datetime
from typing import Optional

try:
    from filelock import FileLock
except Exception:  # pragma: no cover - dependência opcional
    FileLock = None  # type: ignore


class JSONRepository:
    def __init__(self, path: str = 'representados.json'):
        self.path = path
        self.lock_path = f'{path}.lock'

    def _ensure_file(self) -> None:
        if not os.path.exists(self.path):
            initial = {"representantes": [], "next_id": 1}
            self.save(initial)

    def _acquire_lock(self):
        if FileLock is None:
            # Lock inoperante: filelock não instalado — chamador deve garantir escrita única
            return None
        return FileLock(self.lock_path, timeout=5)

    def load(self) -> dict:
        """Carrega o arquivo JSON. Garante que o arquivo existe primeiro."""
        self._ensure_file()
        with open(self.path, 'r', encoding='utf-8') as f:
            return json.load(f)

    def save(self, data: dict) -> None:
        """Salva dados atomicamente.

        Escreve em um arquivo temporário e depois usa os.replace para evitar escritas parciais.
        """
        dirn = os.path.dirname(self.path) or '.'
        fd, tmp = tempfile.mkstemp(dir=dirn)
        try:
            with os.fdopen(fd, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            os.replace(tmp, self.path)
        finally:
            if os.path.exists(tmp):
                try:
                    os.remove(tmp)
                except Exception:
                    pass

    # --- Operações do Repositório ---
    def get_representante_by_email(self, email: str) -> Optional[dict]:
        data = self.load()
        email = email.lower() if email else email
        for r in data.get('representantes', []):
            if r.get('email', '').lower() == email:
                return r
        return None

    def add_representante(self, nome: str, email: str, telefone: Optional[str] = None, senha: Optional[str] = None, mensagens: Optional[list] = None) -> dict:
        """Adiciona um novo representante e retorna o dicionário criado."""
        lock = self._acquire_lock()
        if lock:
            lock.acquire()
        try:
            data = self.load()
            # verificação simples de duplicata
            if self.get_representante_by_email(email) is not None:
                raise ValueError('representante already exists')

            ident = f"r{data.get('next_id', 1)}"
            data['next_id'] = data.get('next_id', 1) + 1
            rep = {
                'id': ident,
                'nome': nome.lower() if isinstance(nome, str) else nome,
                'email': email.lower() if isinstance(email, str) else email,
                'telefone': telefone,
                'senha': senha,
                'alunos': [],
                'mensagens': [],    
                'metadata': {'created_at': datetime.utcnow().isoformat()}
            }
            data.setdefault('representantes', []).append(rep)
            self.save(data)
            return rep
        finally:
            if lock:
                lock.release()

    def add_aluno(self, representante_email: str, nome: str, email: Optional[str] = None, telefone: Optional[str] = None) -> dict:
        """Anexa um aluno ao representante identificado por email. Retorna o dicionário do aluno."""
        lock = self._acquire_lock()
        if lock:
            lock.acquire()
        try:
            data = self.load()
            rep = None
            for r in data.get('representantes', []):
                if r.get('email', '').lower() == representante_email.lower():
                    rep = r
                    break
            if rep is None:
                raise KeyError('representante not found')

            aid = f"a{data.get('next_id', 1)}"
            data['next_id'] = data.get('next_id', 1) + 1
            aluno = {
                'id': aid,
                'nome': nome.lower() if isinstance(nome, str) else nome,
                'email': email.lower() if isinstance(email, str) and email else None,
                'telefone': telefone,
                'data_adicionado': datetime.utcnow().isoformat()
            }
            rep.setdefault('alunos', []).append(aluno)
            self.save(data)
            return aluno
        finally:
            if lock:
                lock.release()

    def remove_aluno(self, representante_email: str, aluno_email: str) -> bool:
        """Remove um aluno por email do representante dado. Retorna True se removido."""
        lock = self._acquire_lock()
        if lock:
            lock.acquire()
        try:
            data = self.load()
            rep = None
            for r in data.get('representantes', []):
                if r.get('email', '').lower() == representante_email.lower():
                    rep = r
                    break
            if rep is None:
                raise KeyError('representante not found')

            alunos = rep.get('alunos', [])
            for i, a in enumerate(alunos):
                if a.get('email', '').lower() == aluno_email.lower():
                    del alunos[i]
                    self.save(data)
                    return True
            return False
        finally:
            if lock:
                lock.release()
        
    def check_aluno_exists(self, representante_email: str, aluno_email: str) -> bool:
        """Verifica se um aluno com o email dado existe sob o representante."""
        data = self.load()
        for r in data.get('representantes', []):
            if r.get('email', '').lower() == representante_email.lower():
                for a in r.get('alunos', []):
                    if a.get('email', '').lower() == aluno_email.lower():
                        return True
        return False
    
    def get_alunos_of_representante(self, representante_email: str) -> list[dict]:
        """Retorna lista de alunos para o email do representante dado."""
        data = self.load()
        for r in data.get('representantes', []):
            if r.get('email', '').lower() == representante_email.lower():
                return r.get('alunos', [])
        return []

    def update_aluno(self, representante_email: str, aluno_id: str, updates: dict) -> dict:
        """Atualiza um aluno por id para o representante dado e retorna o aluno atualizado."""
        lock = self._acquire_lock()
        if lock:
            lock.acquire()
        try:
            data = self.load()
            rep = None
            for r in data.get('representantes', []):
                if r.get('email', '').lower() == representante_email.lower():
                    rep = r
                    break
            if rep is None:
                raise KeyError('representante not found')

            alunos = rep.setdefault('alunos', [])
            for a in alunos:
                if a.get('id') == aluno_id:
                    # Permitir apenas atualização de campos conhecidos
                    for k, v in updates.items():
                        if k in ('nome', 'email', 'telefone'):
                            a[k] = v.lower() if isinstance(v, str) and k in ('nome','email') else v
                    self.save(data)
                    return a
            raise KeyError('aluno not found')
        finally:
            if lock:
                lock.release()

    def remove_aluno_by_id(self, representante_email: str, aluno_id: str) -> bool:
        """Remove um aluno por id. Retorna True se removido."""
        lock = self._acquire_lock()
        if lock:
            lock.acquire()
        try:
            data = self.load()
            rep = None
            for r in data.get('representantes', []):
                if r.get('email', '').lower() == representante_email.lower():
                    rep = r
                    break
            if rep is None:
                raise KeyError('representante not found')

            alunos = rep.get('alunos', [])
            for i, a in enumerate(alunos):
                if a.get('id') == aluno_id:
                    del alunos[i]
                    self.save(data)
                    return True
            return False
        finally:
            if lock:
                lock.release()

    def adicionar_mensagem(self, representante_email: str, mensagem: dict) -> None:
        lock = self._acquire_lock()
        if lock:
            lock.acquire()
        try:
            data = self.load()
            rep = None
            for r in data.get('representantes', []):
                if r.get('email', '').lower() == representante_email.lower():
                    rep = r
                    break
            if rep is None:
                raise KeyError('representante not found')

            mensagens = rep.setdefault('mensagens', [])
            mensagens.append(mensagem)
            self.save(data)
        finally:
            if lock:
                lock.release()
    
    def get_mensagens_of_representante(self, representante_email: str) -> list[dict]:
        """Retorna lista de mensagens para o email do representante dado."""
        data = self.load()
        for r in data.get('representantes', []):
            if r.get('email', '').lower() == representante_email.lower():
                return r.get('mensagens', [])
        return []
