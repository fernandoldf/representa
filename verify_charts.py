import requests
import requests
import json
import re

# Configuração
BASE_URL = 'http://127.0.0.1:5000'
LOGIN_URL = f'{BASE_URL}/login'
DASHBOARD_URL = f'{BASE_URL}/dashboard'

# Credenciais de teste
EMAIL = 'chart_test@example.com'
PASSWORD = 'testpassword'

def create_test_user():
    import hashlib
    from services.controle_representates import service
    
    # Verificar se o usuário existe
    if service.buscar_representante_por_email(EMAIL):
        return

    # Criar usuário com senha hash
    senha_hash = hashlib.sha256(PASSWORD.encode()).hexdigest()
    service.adicionar_representante('Chart Test', EMAIL, '123456789', senha=senha_hash)
    print(f"Created test user: {EMAIL}")

def verify_charts():
    create_test_user()
    session = requests.Session()
    
    # 1. Login
    print(f"Logging in as {EMAIL}...")
    response = session.post(LOGIN_URL, data={'email': EMAIL, 'password': PASSWORD})
    
    if response.url != DASHBOARD_URL:
        print(f"Login failed. Current URL: {response.url}")
        # Tentar registrar se o login falhar? Ou apenas falhar.
        # Vamos assumir que o usuário existe dos passos anteriores.
        return False

    print("Login successful.")

    # 2. Obter Dashboard
    print("Fetching dashboard...")
    response = session.get(DASHBOARD_URL)
    
    if response.status_code != 200:
        print(f"Failed to fetch dashboard. Status: {response.status_code}")
        print(f"Response body: {response.text}")
        return False

    html = response.text
    
    # 3. Verificar Dados do Gráfico
    print("Checking for chart data in HTML...")
    
    if 'const msgLabels =' in html and 'const studentLabels =' in html:
        print("SUCCESS: Chart data variables found in HTML.")
        
        # Extrair dados para verificar estrutura (verificação simples de string)
        import re
        msg_labels_match = re.search(r'const msgLabels = (\[.*?\]);', html)
        if msg_labels_match:
            print(f"Message Labels: {msg_labels_match.group(1)}")
        else:
            print("WARNING: Could not extract msgLabels value.")

        student_labels_match = re.search(r'const studentLabels = (\[.*?\]);', html)
        if student_labels_match:
            print(f"Student Labels: {student_labels_match.group(1)}")
        else:
            print("WARNING: Could not extract studentLabels value.")
            
        # Extrair e imprimir a contagem de novos alunos
        # Usar um regex mais flexível para lidar com possíveis espaços em branco
        match = re.search(r'class="text-sm text-green-600 mt-2">\s*\+(\d+)\s+novos esta semana', html)
        if match:
            print(f"SUCCESS: Found new students count: {match.group(1)}")
        else:
            print("WARNING: Could not find new students count in HTML.")
            # Debug: imprimir contexto
            if "novos esta semana" in html:
                print("DEBUG: Found 'novos esta semana' in HTML, but regex failed.")
                start = html.find("novos esta semana") - 50
                end = html.find("novos esta semana") + 50
                print(f"DEBUG Context: {html[start:end]}")
            else:
                print("DEBUG: 'novos esta semana' NOT found in HTML.")
            
        return True
    else:
        print("FAILURE: Chart data variables NOT found in HTML.")
        return False

if __name__ == "__main__":
    try:
        if verify_charts():
            print("\nVerification PASSED.")
        else:
            print("\nVerification FAILED.")
    except Exception as e:
        print(f"\nAn error occurred: {e}")
