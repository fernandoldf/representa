import requests
import os
from datetime import datetime
from dotenv import load_dotenv
from victor.usuario import Aluno
"""Stubs for Google Sheets API integration.

Implement: adicionar_aluno(aluno) and buscar_alunos() as needed.
"""
load_dotenv()
ENDPOINT = f'https://api.sheety.co/{os.getenv("SHEETY_PROJECT_ID")}/representa/dados'
headers = {"Authorization": f"Basic {os.getenv('SHEETY_ACCESS_TOKEN')}"}

def adicionar_aluno(aluno):
    add_json = {"dado": {"data": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
                "nome": aluno.nome,
                "eMail": aluno.email,
                "telefone": aluno.telefone}}
    response = requests.post(ENDPOINT, json=add_json, headers=headers)
    print(response.json())
    if response.status_code == 200 or response.status_code == 201:
        print("Aluno added successfully")
        return True
    else:
        print(f"Failed to add aluno: {response.status_code}")
        return False


def buscar_alunos():
    """Return list of alunos from Google Sheets (to be implemented)."""
    response = requests.get(ENDPOINT, headers=headers)
    if response.status_code == 200:
        print("Alunos fetched successfully")
        return response.json().get('dados', [])
    else:
        print(f"Failed to fetch alunos: {response.status_code}")
        return []
    
if __name__ == "__main__":
    # Test fetching alunos
    aluno = Aluno("Teste", "teste@example.com", "123456789")
    adicionar_aluno(aluno)
    alunos = buscar_alunos()
    print(alunos)