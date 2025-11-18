import requests
import os
from datetime import datetime
from dotenv import load_dotenv
from victor.usuario import Aluno, Representante


"""Stubs for Google Sheets API integration.

Implement: adicionar_aluno(aluno) and buscar_alunos() as needed.
"""
load_dotenv()
ENDPOINT = f'https://api.sheety.co/{os.getenv("SHEETY_PROJECT_ID")}/representa/dados'
headers = {"Authorization": f"Basic {os.getenv('SHEETY_ACCESS_TOKEN')}"}


class API_Sheety:
    
    def __init__(self):
        self.endpoint = ENDPOINT
        self.headers = headers
        
    def adicionar_aluno(self, aluno):
        add_json = {"dado": {
                    "data": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
                    "nome": aluno.nome,
                    "eMail": aluno.email,
                    "telefone": aluno.telefone,
                    "representante": aluno.representante}
        }
        response = requests.post(self.endpoint, json=add_json, headers=headers)
        if response.status_code == 200 or response.status_code == 201:
            print("Aluno added successfully")
            return True
        else:
            print(f"Failed to add aluno: {response.status_code}")
            return False

    
    def buscar_alunos(self, nome=None):
        """Return list of alunos for a given representante from Google Sheets (to be implemented)."""
        if nome is not None:
            self.endpoint = f"{self.endpoint}?filter[representante]={nome}"
        response = requests.get(self.endpoint, headers=self.headers)
        if response.status_code == 200:
            alunos = []
            print("Alunos fetched successfully")
            for dado in response.json().get('dados', []):
                alunos.append(self.criar_aluno(dado))
            return alunos
        else:
            print(f"Failed to fetch alunos: {response.status_code}")
            return []

    def criar_aluno(self, json_data):
        return Aluno(
            nome=json_data.get('nome', ''),
            email=json_data.get('eMail', ''),
            telefone=json_data.get('telefone', ''),
            representante=json_data.get('representante', None)
        )
    
if __name__ == "__main__":
    # Test fetching alunos
    # aluno = Aluno("Teste", "teste@example.com", "123456789")
    # adicionar_aluno(aluno)
    api_sheety = API_Sheety()
    representante = Representante("victor", "alice@aqui.com", "987654321")
    representante.atualizar_alunos()
    print(representante)