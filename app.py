from flask import Flask, render_template, request, redirect, url_for
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads'

if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/cadastro')
def cadastro():
    return render_template('cadastro.html')

@app.route('/visitas')
def visitas():
    return "Página de Visitas em construção."

@app.route('/salvar_cadastro', methods=['POST'])
def salvar_cadastro():
    nome = request.form.get('nome')
    loja = request.form.get('loja')
    cep = request.form.get('cep')
    endereco = request.form.get('endereco')
    telefone = request.form.get('telefone')
    whatsapp = request.form.get('whatsapp')
    site = request.form.get('site')
    produtos = request.form.getlist('produtos')
    marcas = request.form.get('marcas')

    # Salvar imagem (se enviada)
    foto = request.files.get('foto')
    if foto and foto.filename != '':
        filename = secure_filename(foto.filename)
        path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        foto.save(path)

    print("Cadastro recebido:", nome, loja, cep, produtos, marcas)
    return redirect(url_for('home'))

@app.route('/consulta_cep/<cep>')
def consulta_cep(cep):
    import requests
    r = requests.get(f'https://viacep.com.br/ws/{cep}/json/')
    data = r.json()
    logradouro = data.get('logradouro', '')
    bairro = data.get('bairro', '')
    localidade = data.get('localidade', '')
    uf = data.get('uf', '')
    endereco = f"{logradouro} - {bairro}, {localidade} - {uf}"
    return {'endereco': endereco}

if __name__ == '__main__':
    app.run(debug=True)
