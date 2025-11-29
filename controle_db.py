"""JSON-backed repository for `representados.json`.

This class provides simple atomic load/save and CRUD helpers to treat
`representados.json` as a lightweight persistent store.

Notes:
- Uses a file lock to avoid concurrent write corruption (requires filelock).
- Writes are atomic (writes to temporary file then os.replace).
"""
from __future__ import annotations

import json
import os
import tempfile
from datetime import datetime
from typing import Optional

try:
    from filelock import FileLock
except Exception:  # pragma: no cover - optional dependency
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
            # No-op lock: filelock not installed — caller must ensure single writer
            return None
        return FileLock(self.lock_path, timeout=5)

    def load(self) -> dict:
        """Load the JSON file. Ensures file exists first."""
        self._ensure_file()
        with open(self.path, 'r', encoding='utf-8') as f:
            return json.load(f)

    def save(self, data: dict) -> None:
        """Save data atomically.

        Writes to a temporary file then os.replace to avoid partial writes.
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

    # --- Repository operations ---
    def get_representante_by_email(self, email: str) -> Optional[dict]:
        data = self.load()
        email = email.lower() if email else email
        for r in data.get('representantes', []):
            if r.get('email', '').lower() == email:
                return r
        return None

    def add_representante(self, nome: str, email: str, telefone: Optional[str] = None) -> dict:
        """Add a new representante and return the created dict."""
        lock = self._acquire_lock()
        if lock:
            lock.acquire()
        try:
            data = self.load()
            # simple duplicate check
            if self.get_representante_by_email(email) is not None:
                raise ValueError('representante already exists')

            ident = f"r{data.get('next_id', 1)}"
            data['next_id'] = data.get('next_id', 1) + 1
            rep = {
                'id': ident,
                'nome': nome.lower() if isinstance(nome, str) else nome,
                'email': email.lower() if isinstance(email, str) else email,
                'telefone': telefone,
                'alunos': [],
                'metadata': {'created_at': datetime.utcnow().isoformat()}
            }
            data.setdefault('representantes', []).append(rep)
            self.save(data)
            return rep
        finally:
            if lock:
                lock.release()

    def add_aluno(self, representante_email: str, nome: str, email: Optional[str] = None, telefone: Optional[str] = None) -> dict:
        """Append an aluno to the representante identified by email. Returns aluno dict."""
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
        """Remove an aluno by email from the given representante. Returns True if removed."""
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
        """Check if an aluno with given email exists under the representante."""
        data = self.load()
        for r in data.get('representantes', []):
            if r.get('email', '').lower() == representante_email.lower():
                for a in r.get('alunos', []):
                    if a.get('email', '').lower() == aluno_email.lower():
                        return True
        return False
    
    def get_alunos_of_representante(self, representante_email: str) -> list[dict]:
        """Return list of alunos for the given representante email."""
        data = self.load()
        for r in data.get('representantes', []):
            if r.get('email', '').lower() == representante_email.lower():
                return r.get('alunos', [])
        return []

    def update_aluno(self, representante_email: str, aluno_id: str, updates: dict) -> dict:
        """Update an aluno by id for the given representante and return updated aluno."""
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
                    # Only allow updating known fields
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
        """Remove an aluno by id. Returns True if removed."""
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