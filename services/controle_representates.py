"""Camada de Controlador/Serviço para gerenciar representantes.

Este módulo fornece a classe `RepresentanteService` que atua como uma fachada
para todas as operações relacionadas a representantes, incluindo persistência
e envio de e-mail.
"""

from typing import Optional, List
from models.usuario import Representante, Aluno
from controle_db import JSONRepository
from services.email_sender import EmailSender

class RepresentanteService:
    def __init__(self, db_path: str = 'db.json'):
        self._repo = JSONRepository(db_path)
        self._email_sender = EmailSender()

    def _dict_to_representante(self, d: dict) -> Representante:
        """Converte um dicionário armazenado em uma instância do modelo Representante."""
        rep = Representante(d.get('nome', ''), d.get('email', ''), d.get('telefone', ''), d.get('senha', ''))
        rep.id = d.get('id')
        
        # Converter e anexar alunos
        for a in d.get('alunos', []):
            aluno_obj = Aluno(
                a.get('nome'), 
                a.get('email'), 
                a.get('telefone'), 
                representante=rep.nome,
                data_adicionado=a.get('data_adicionado')
            )
            aluno_obj.id = a.get('id')
            rep.alunos.append(aluno_obj)
            
        # Anexar mensagens
        rep.mensagens = d.get('mensagens', [])
        rep.metadata = d.get('metadata', {})
        return rep

    def adicionar_representante(self, nome: str, email: str, telefone: str, senha: str = None) -> Representante:
        """Adiciona um novo representante e retorna o modelo."""
        rep_dict = self._repo.add_representante(nome, email, telefone, senha=senha)
        return self._dict_to_representante(rep_dict)

    def buscar_representante_por_email(self, email: str) -> Optional[dict]:
        """Busca um representante pelo email e retorna dict (dados brutos)."""
        return self._repo.get_representante_by_email(email)

    def retornar_representante(self, email: str) -> Optional[Representante]:
        """Retorna uma instância de Representante totalmente carregada."""
        d = self.buscar_representante_por_email(email)
        if d:
            return self._dict_to_representante(d)
        return None

    def listar_representantes(self) -> List[dict]:
        """Retorna uma lista de todos os representantes (nome e email)."""
        data = self._repo.load()
        reps = []
        for r in data.get('representantes', []):
            reps.append({'nome': r.get('nome'), 'email': r.get('email')})
        return reps

    def adicionar_aluno(self, representante_email: str, nome: str, email: str, telefone: str) -> Aluno:
        """Adiciona um aluno ao representante."""
        aluno_dict = self._repo.add_aluno(representante_email, nome, email, telefone)
        aluno = Aluno(aluno_dict.get('nome'), aluno_dict.get('email'), aluno_dict.get('telefone'))
        aluno.id = aluno_dict.get('id')
        return aluno

    def remover_aluno(self, representante_email: str, aluno_id: str) -> bool:
        """Remove um aluno por ID."""
        return self._repo.remove_aluno_by_id(representante_email, aluno_id)

    def atualizar_aluno(self, representante_email: str, aluno_id: str, updates: dict) -> dict:
        """Atualiza dados de um aluno."""
        return self._repo.update_aluno(representante_email, aluno_id, updates)

    def enviar_mensagem(self, representante: Representante, assunto: str, corpo: str) -> bool:
        """Envia email para todos os alunos e salva a mensagem no histórico."""
        print(f"Enviando email para os alunos de {representante.nome}: assunto='{assunto}'")
        destinatarios = [aluno.email for aluno in representante.alunos if aluno.email]
        
        try:
            sucesso = self._email_sender.send_email(
                destinatarios, 
                f"{representante.nome.title()} - {assunto}", 
                f"Representante {representante.nome.title()} informa:\n{corpo}"
            )
            
            if sucesso:
                from datetime import datetime
                msg_data = {
                    "assunto": assunto, 
                    "corpo": corpo, 
                    "data": datetime.now().strftime("%d/%m/%Y %H:%M:%S")
                }
                self._repo.adicionar_mensagem(representante.email, msg_data)
                representante.mensagens.append(msg_data)
                return True
            return False
        except Exception as e:
            print(f"Erro ao enviar mensagem: {e}")
            return False

# Instância global para facilidade de uso no código do servidor existente,
# embora injeção de dependência fosse melhor em uma aplicação maior.
service = RepresentanteService()