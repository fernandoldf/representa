import requests
import os
from datetime import datetime
from dotenv import load_dotenv
from models.usuario import Aluno, Representante


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
    
    def get_alunos_filtered(self, nome=None):
        """Return list of alunos for a given representante from Google Sheets (to be implemented)."""
        if nome is not None:
            self.endpoint = f"{self.endpoint}?filter[representante]={nome}"
        response = requests.get(self.endpoint, headers=self.headers)
        print(response.json())
        if response.status_code == 200:
            return response.json().get('dados', [])
        else:
            print(f"Failed to fetch alunos: {response.status_code}")
            raise Exception("Erro ao buscar alunos do Google Sheets")

    def buscar_alunos(self, nome=None):
        """Return list of alunos for a given representante from Google Sheets (to be implemented)."""
        try:
            alunos_data = self.get_alunos_filtered(nome)
            alunos = []
            print("Alunos fetched successfully")
            for dado in alunos_data:
                alunos.append({"nome": dado.get('nome', ''),
                               "eMail": dado.get('eMail', ''),
                               "telefone": dado.get('telefone', ''),
                               "representante": dado.get('representante', '')})
            return alunos
        except Exception as e:
            print(f"Failed to fetch alunos: {e}")
            return None

    def deletar_aluno(self, aluno_id: str):
        """Delete an aluno by ID from Google Sheets (to be implemented)."""
        delete_endpoint = f"{self.endpoint}/{aluno_id}"
        response = requests.delete(delete_endpoint, headers=self.headers)
        if response.status_code == 200:
            print(f"Aluno with ID {aluno_id} deleted successfully from Google Sheets")
            return True
        else:
            print(f"Failed to delete aluno with ID {aluno_id}: {response.status_code}")
            return False
    
if __name__ == "__main__":
    # Test fetching alunos
    # aluno = Aluno("Teste", "teste@example.com", "123456789")
    # adicionar_aluno(aluno)
    api_sheety = API_Sheety()
    representante = Representante("victor", "alice@aqui.com", "987654321")
    representante.atualizar_alunos()
    print(representante)