from flask import Flask, render_template, request, redirect, url_for, flash
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('FLASK_SECRET_KEY', 'dev-secret')

# Import placeholders (modules to be implemented by contributors)
# from victor.enviar_email import enviar_email
# from victor.enviar_whatsapp import enviar_whatsapp
# from victor.aluno import Aluno
# from andrielli.validacao import validar_email, validar_nome, validar_telefone
# import api_googlesheets
# import api_twilio

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Lógica de login (placeholder)
        flash('Login recebido (placeholder)')
        return redirect(url_for('dashboard'))
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@app.route('/adicionar-aluno', methods=['GET', 'POST'])
def adicionar_aluno():
    if request.method == 'POST':
        nome = request.form.get('nome')
        email = request.form.get('email')
        telefone = request.form.get('telefone')
        # validações e lógica de salvamento deverão ser implementadas
        flash('Aluno adicionado (placeholder)')
        return redirect(url_for('dashboard'))
    return render_template('adicionar_aluno.html')

if __name__ == '__main__':
    app.run(debug=True)
