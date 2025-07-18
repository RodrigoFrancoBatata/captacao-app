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
    return render_template('cadastro.html')

@app.route('/cadastro', methods=['POST'])
def cadastro():
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

if __name__ == '__main__':
    app.run(debug=True)
