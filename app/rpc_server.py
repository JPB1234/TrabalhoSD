from app import app, db
from app.models import Sala, Reserva
from flask import jsonify
from datetime import datetime
from flask_jsonrpc import JSONRPC

jsonrpc = JSONRPC(app, '/api')

@jsonrpc.method('App.cadastrar_reserva')
def cadastrar_reserva(usuario: str, sala: str, data: str, hora: str) -> str:
    sala_obj = Sala.query.filter_by(nome=sala).first()
    if not sala_obj:
        return jsonify({'error': 'Sala não encontrada'}), 404

    data_obj = datetime.strptime(data, '%Y-%m-%d').date()
    hora_obj = datetime.strptime(hora, '%H:%M').time()

    conflitos = Reserva.query.filter_by(sala_id=sala_obj.id, data=data_obj, hora=hora_obj).first()
    if conflitos:
        return jsonify({'error': 'Sala ocupada'}), 409

    reserva = Reserva(sala_id=sala_obj.id, usuario=usuario, data=data_obj, hora=hora_obj)
    db.session.add(reserva)
    db.session.commit()
    return jsonify({'message': 'Reserva criada com sucesso'}), 201

@jsonrpc.method('App.remover_reserva')
def remover_reserva(usuario: str, sala: str, data: str, hora: str) -> str:
    sala_obj = Sala.query.filter_by(nome=sala).first()
    if not sala_obj:
        return jsonify({'error': 'Sala não encontrada'}), 404

    data_obj = datetime.strptime(data, '%Y-%m-%d').date()
    hora_obj = datetime.strptime(hora, '%H:%M').time()

    reserva = Reserva.query.filter_by(sala_id=sala_obj.id, usuario=usuario, data=data_obj, hora=hora_obj).first()
    if not reserva:
        return jsonify({'error': 'Reserva não encontrada'}), 404

    db.session.delete(reserva)
    db.session.commit()
    return jsonify({'message': 'Reserva removida com sucesso'}), 200

@jsonrpc.method('App.consultar_reserva')
def consultar_reserva(sala: str, data: str, hora: str) -> str:
    sala_obj = Sala.query.filter_by(nome=sala).first()
    if not sala_obj:
        return jsonify({'error': 'Sala não encontrada'}), 404

    data_obj = datetime.strptime(data, '%Y-%m-%d').date()
    hora_obj = datetime.strptime(hora, '%H:%M').time()

    reserva = Reserva.query.filter_by(sala_id=sala_obj.id, data=data_obj, hora=hora_obj).first()
    if reserva:
        return jsonify({'message': 'Sala reservada'}), 200
    else:
        return jsonify({'message': 'Sala disponível'}), 200

@jsonrpc.method('App.consultar_reservas_sala')
def consultar_reservas_sala(sala: str) -> list:
    sala_obj = Sala.query.filter_by(nome=sala).first()
    if not sala_obj:
        return jsonify({'error': 'Sala não encontrada'}), 404

    reservas = Reserva.query.filter_by(sala_id=sala_obj.id).all()
    return jsonify([reserva.serialize() for reserva in reservas]), 200

@jsonrpc.method('App.consultar_reservas_usuario')
def consultar_reservas_usuario(usuario: str) -> list:
    reservas = Reserva.query.filter_by(usuario=usuario).all()
    return jsonify([reserva.serialize() for reserva in reservas]), 200
