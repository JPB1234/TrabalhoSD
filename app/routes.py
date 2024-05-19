from flask import request, jsonify
from app import app, db
from app.modelo import Sala, Reserva

@app.route('/salas', methods=['GET'])
def get_salas():
    salas = Sala.query.all()
    return jsonify([sala.serialize() for sala in salas])

@app.route('/salas/<int:sala_id>', methods=['GET'])
def get_sala(sala_id):
    sala = Sala.query.get(sala_id)
    if sala:
        return jsonify(sala.serialize())
    else:
        return jsonify({'error': 'Sala não encontrada'}), 404

@app.route('/salas', methods=['POST'])
def create_sala():
    data = request.get_json()
    if not data or 'nome' not in data:
        return jsonify({'error': 'Dados inválidos'}), 400

    nome = data['nome']
    if Sala.query.filter_by(nome=nome).first():
        return jsonify({'error': 'Sala já existente'}), 400

    sala = Sala(nome=nome)
    db.session.add(sala)
    db.session.commit()

    return jsonify(sala.serialize()), 201

@app.route('/salas/<int:sala_id>', methods=['PUT'])
def update_sala(sala_id):
    data = request.get_json()
    if not data or 'nome' not in data:
        return jsonify({'error': 'Dados inválidos'}), 400

    nome = data['nome']
    sala = Sala.query.get(sala_id)
    if not sala:
        return jsonify({'error': 'Sala não encontrada'}), 404

    if Sala.query.filter_by(nome=nome).first() and sala.id != Sala.query.filter_by(nome=nome).first().id:
        return jsonify({'error': 'Nome já existente'}), 400

    sala.nome = nome
    db.session.commit()

    return jsonify(sala.serialize()), 200

@app.route('/salas/<int:sala_id>', methods=['DELETE'])
def delete_sala(sala_id):
    sala = Sala.query.get(sala_id)
    if not sala:
        return jsonify({'error': 'Sala não encontrada'}), 404

    db.session.delete(sala)
    db.session.commit()

    return jsonify({'message': 'Sala removida'}), 200

@app.route('/reservas', methods=['GET'])
def get_reservas():
    reservas = Reserva.query.all()
    return jsonify([reserva.serialize() for reserva in reservas])

@app.route('/reservas/<int:reserva_id>', methods=['GET'])
def get_reserva(reserva_id):
    reserva = Reserva.query.get(reserva_id)
    if reserva:
        return jsonify(reserva.serialize())
    else:
        return jsonify({'error': 'Reserva não encontrada'}), 404

@app.route('/reservas', methods=['POST'])
def create_reserva():
    data = request.get_json()
    if not data or 'sala_id' not in data or 'usuario' not in data or 'data' not in data or 'hora' not in data:
        return jsonify({'error': 'Dados inválidos'}), 400

    sala_id = data['sala_id']
    sala = Sala.query.get(sala_id)
    if not sala:
        return jsonify({'error': 'Sala não encontrada'}), 404

    usuario = data['usuario']
    data_str = data['data']
    try:
        from datetime import datetime
        data_obj = datetime.strptime(data_str, '%Y-%m-%d').date()
    except ValueError:
        return jsonify({'error': 'Formato de data inválido (YYYY-MM-DD)'}), 400

    hora_str = data['hora']
    try:
        hora_obj = datetime.strptime(hora_str, '%H:%M').time()
    except ValueError:
        return jsonify({'error': 'Formato de hora inválido (HH:MM)'}), 400

    conflitos = Reserva.query.filter_by(sala_id=sala_id, data=data_obj, hora=hora_obj).first()
    if conflitos:
        return jsonify({'error': 'Sala ocupada'}), 409

    reserva = Reserva(sala_id=sala_id, usuario=usuario, data=data_obj, hora=hora_obj)
    db.session.add(reserva)
    db.session.commit()

    return jsonify(reserva.serialize()), 201

@app.route('/reservas/<int:reserva_id>', methods=['PUT'])
def update_reserva(reserva_id):
    data = request.get_json()
    if not data or 'sala_id' not in data or 'usuario' not in data or 'data' not in data or 'hora' not in data:
        return jsonify({'error': 'Dados inválidos'}), 400

    reserva = Reserva.query.get(reserva_id)
    if not reserva:
        return jsonify({'error': 'Reserva não encontrada'}), 404

    sala_id = data['sala_id']
    sala = Sala.query.get(sala_id)
    if not sala:
        return jsonify({'error': 'Sala não encontrada'}), 404

    usuario = data['usuario']
    data_str = data['data']
    try:
        from datetime import datetime
        data_obj = datetime.strptime(data_str, '%Y-%m-%d').date()
    except ValueError:
        return jsonify({'error': 'Formato de data inválido (YYYY-MM-DD)'}), 400

    hora_str = data['hora']
    try:
        hora_obj = datetime.strptime(hora_str, '%H:%M').time()
    except ValueError:
        return jsonify({'error': 'Formato de hora inválido (HH:MM)'}), 400

    conflitos = Reserva.query.filter_by(sala_id=sala_id, data=data_obj, hora=hora_obj).filter(Reserva.id != reserva_id).first()
    if conflitos:
        return jsonify({'error': 'Sala ocupada'}), 409

    reserva.sala_id = sala_id
    reserva.usuario = usuario
    reserva.data = data_obj
    reserva.hora = hora_obj
    db.session.commit()

    return jsonify(reserva.serialize()), 200

@app.route('/reservas/<int:reserva_id>', methods=['DELETE'])
def delete_reserva(reserva_id):
    reserva = Reserva.query.get(reserva_id)
    if not reserva:
        return jsonify({'error': 'Reserva não encontrada'}), 404

    db.session.delete(reserva)
    db.session.commit()

    return jsonify({'message': 'Reserva removida'}), 200
