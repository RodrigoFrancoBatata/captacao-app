from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class ClienteCaptado(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100))
    nome_fantasia = db.Column(db.String(100))
    endereco = db.Column(db.String(200))
    telefone = db.Column(db.String(20))
    whatsapp = db.Column(db.String(20))
    site = db.Column(db.String(150))
    produtos = db.Column(db.String(300))
    marcas = db.Column(db.String(300))
    novas_marcas = db.Column(db.String(300))
    info_extra = db.Column(db.Text)
    foto1 = db.Column(db.String(200))
    foto2 = db.Column(db.String(200))
    foto3 = db.Column(db.String(200))
    foto4 = db.Column(db.String(200))
    data_visita = db.Column(db.Date)
    proxima_visita = db.Column(db.Date)
