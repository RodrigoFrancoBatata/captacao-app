from flask import Flask, render_template, request, redirect, url_for, make_response
from werkzeug.utils import secure_filename
from models import db, ClienteCaptado
from dotenv import load_dotenv
from weasyprint import HTML
import os
import requests

# Carrega variáveis do .env
load_dotenv()

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URL")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Inicializa o banco
db.init_app(app)

# Cria a pasta de uploads se não existir
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

# Cria as tabelas ao iniciar
with app.app_context():
    db.create_all()

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/cadastro')
def cadastro():
    return render_template('cadastro.html')

@app.route('/salvar_cadastro', methods=['POST'])
def salvar_cadastro():
    nome = request.form.get('nome')
    nome_fantasia = request.form.get('nome_fantasia')
    cep = request.form.get('cep')
    endereco = request.form.get('endereco')
    telefone = request.form.get('telefone')
    whatsapp = request.form.get('whatsapp')
    site = request.form.get('site')
    produtos = ",".join(request.form.getlist('produtos'))
    marcas = request.form.get('marcas')
    novas_marcas = request.form.get('novas_marcas')
    info_extra = request.form.get('info_extra')
    data_visita = request.form.get('data_visita') or None
    proxima_visita = request.form.get('proxima_visita') or None

    fotos = []
    for i in range(1, 5):
        foto = request.files.get(f'foto{i}')
        if foto and foto.filename:
            filename = secure_filename(foto.filename)
            path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            foto.save(path)
            fotos.append(filename)
        else:
            fotos.append(None)

    novo_cliente = ClienteCaptado(
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
        foto1=fotos[0],
        foto2=fotos[1],
        foto3=fotos[2],
        foto4=fotos[3],
        data_visita=data_visita,
        proxima_visita=proxima_visita
    )
    db.session.add(novo_cliente)
    db.session.commit()
    return redirect(url_for('home'))

@app.route('/consulta_cep/<cep>')
def consulta_cep(cep):
    r = requests.get(f'https://viacep.com.br/ws/{cep}/json/')
    data = r.json()
    logradouro = data.get('logradouro', '')
    bairro = data.get('bairro', '')
    localidade = data.get('localidade', '')
    uf = data.get('uf', '')
    endereco = f"{logradouro} - {bairro}, {localidade} - {uf}"
    return {'endereco': endereco}

@app.route('/clientes')
def listar_clientes():
    clientes = ClienteCaptado.query.all()
    return render_template("clientes.html", clientes=clientes)

@app.route("/editar/<int:id>", methods=["GET", "POST"])
def editar_cliente(id):
    cliente = ClienteCaptado.query.get_or_404(id)
    if request.method == "POST":
        cliente.nome = request.form.get("nome")
        cliente.nome_fantasia = request.form.get("nome_fantasia")
        cliente.endereco = request.form.get("endereco")
        cliente.telefone = request.form.get("telefone")
        cliente.whatsapp = request.form.get("whatsapp")
        cliente.site = request.form.get("site")
        cliente.produtos = ",".join(request.form.getlist("produtos"))
        cliente.marcas = request.form.get("marcas")
        cliente.novas_marcas = request.form.get("novas_marcas")
        cliente.info_extra = request.form.get("info_extra")
        cliente.proxima_visita = request.form.get("proxima_visita")
        db.session.commit()
        return redirect("/clientes")
    return render_template("editar.html", cliente=cliente)

@app.route('/cliente/<int:id>')
def visualizar_cliente(id):
    cliente = ClienteCaptado.query.get_or_404(id)
    return render_template("cliente.html", cliente=cliente)

@app.route('/cliente/<int:id>/pdf')
def gerar_pdf_cliente(id):
    cliente = ClienteCaptado.query.get_or_404(id)
    html = render_template("cliente.html", cliente=cliente)
    pdf = HTML(string=html, base_url=request.base_url).write_pdf()
    
    response = make_response(pdf)
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = f'inline; filename=cliente_{id}.pdf'
    return response

@app.route('/agenda')
def agenda():
    clientes = ClienteCaptado.query.filter(ClienteCaptado.proxima_visita != None).order_by(ClienteCaptado.proxima_visita).all()
    return render_template("agenda.html", clientes=clientes)


if __name__ == '__main__':
    app.run(debug=True)
