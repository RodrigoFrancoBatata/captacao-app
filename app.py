import os
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename
from dotenv import load_dotenv
from models import db, ClienteCaptado
from datetime import datetime

load_dotenv()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URL")
app.config['UPLOAD_FOLDER'] = 'photos'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

with app.app_context():
    db.create_all()

@app.route('/')
def home():
    hoje = datetime.today().date()
    visitas_hoje = ClienteCaptado.query.filter(ClienteCaptado.proxima_visita == hoje).all()
    return render_template('home.html', visitas_hoje=visitas_hoje)

@app.route('/cadastro')
def cadastro():
    return render_template('cadastro.html')

@app.route('/cadastro', methods=['POST'])
def salvar_cadastro():
    nome = request.form['nome']
    nome_fantasia = request.form['nome_fantasia']
    endereco = request.form['endereco']
    telefone = request.form['telefone']
    whatsapp = request.form['whatsapp']
    site = request.form['site']
    produtos = ', '.join(request.form.getlist('produtos'))
    marcas = ', '.join(request.form.getlist('marcas'))
    novas_marcas = request.form['novas_marcas']
    info_extra = request.form['info_extra']
    data_visita = datetime.today().date()
    proxima_visita = datetime.strptime(request.form['proxima_visita'], "%Y-%m-%d").date()

    fotos = []
    for i in range(1, 5):
        foto = request.files.get(f'foto{i}')
        if foto and foto.filename:
            filename = secure_filename(f"{nome}_{i}_{foto.filename}")
            path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            foto.save(path)
            fotos.append(path)
        else:
            fotos.append(None)

    cliente = ClienteCaptado(
        nome=nome,
        nome_fantasia=nome_fantasia,
        endereco=endereco,
        telefone=telefone,
        whatsapp=whatsapp,
        site=site,
        produtos=produtos,
        marcas=marcas,
        novas_marcas=novas_marcas,
        info_extra=info_extra,
        foto1=fotos[0], foto2=fotos[1], foto3=fotos[2], foto4=fotos[3],
        data_visita=data_visita,
        proxima_visita=proxima_visita
    )

    db.session.add(cliente)
    db.session.commit()
    return redirect(url_for('home'))

@app.route('/visitas')
def visitas():
    clientes = ClienteCaptado.query.order_by(ClienteCaptado.data_visita.desc()).all()
    return render_template('visitas.html', clientes=clientes)

@app.route('/visitas-tabela')
def visitas_tabela():
    clientes = ClienteCaptado.query.order_by(ClienteCaptado.proxima_visita).all()
    return render_template('visitas_tabela.html', clientes=clientes)

@app.route('/calendario')
def calendario():
    eventos = ClienteCaptado.query.with_entities(
        ClienteCaptado.nome_fantasia, ClienteCaptado.proxima_visita
    ).all()
    eventos_formatados = [
        {"title": nome, "start": str(data)} for nome, data in eventos if data
    ]
    return render_template('calendario.html', eventos=eventos_formatados)

@app.route('/editar/<int:id>', methods=['GET', 'POST'])
def editar(id):
    cliente = ClienteCaptado.query.get_or_404(id)

    if request.method == 'POST':
        cliente.nome = request.form['nome']
        cliente.nome_fantasia = request.form['nome_fantasia']
        cliente.endereco = request.form['endereco']
        cliente.telefone = request.form['telefone']
        cliente.whatsapp = request.form['whatsapp']
        cliente.site = request.form['site']
        cliente.produtos = ', '.join(request.form.getlist('produtos'))
        cliente.marcas = ', '.join(request.form.getlist('marcas'))
        cliente.novas_marcas = request.form['novas_marcas']
        cliente.info_extra = request.form['info_extra']
        cliente.proxima_visita = datetime.strptime(request.form['proxima_visita'], "%Y-%m-%d").date()

        db.session.commit()
        return redirect(url_for('visitas'))

    return render_template('editar.html', cliente=cliente)

if __name__ == '__main__':
    app.run(debug=True)
