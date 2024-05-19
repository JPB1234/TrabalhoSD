from . import db

class Sala(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(255), unique=True, nullable=False)

    def serialize(self):
        return {
            'id': self.id,
            'nome': self.nome,
        }

class Reserva(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sala_id = db.Column(db.Integer, db.ForeignKey('sala.id'), nullable=False)
    usuario = db.Column(db.String(255), nullable=False)
    data = db.Column(db.Date, nullable=False)
    hora = db.Column(db.Time, nullable=False)

    sala = db.relationship('Sala', backref='reservas')

    def serialize(self):
        return {
            'id': self.id,
            'sala_id': self.sala_id,
            'usuario': self.usuario,
            'data': self.data.strftime('%Y-%m-%d'),
            'hora': self.hora.strftime('%H:%M'),
        }
