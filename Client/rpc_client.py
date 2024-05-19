import requests
import json

API_URL = 'http://localhost:5000/api'

def cadastrar_reserva(usuario, sala, data, hora):
    payload = {
        "jsonrpc": "2.0",
        "method": "App.cadastrar_reserva",
        "params": {"usuario": usuario, "sala": sala, "data": data, "hora": hora},
        "id": 1
    }
    response = requests.post(API_URL, json=payload).json()
    return response

def remover_reserva(usuario, sala, data, hora):
    payload = {
        "jsonrpc": "2.0",
        "method": "App.remover_reserva",
        "params": {"usuario": usuario, "sala": sala, "data": data, "hora": hora},
        "id": 1
    }
    response = requests.post(API_URL, json=payload).json()
    return response

def consultar_reserva(sala, data, hora):
    payload = {
        "jsonrpc": "2.0",
        "method": "App.consultar_reserva",
        "params": {"sala": sala, "data": data, "hora": hora},
        "id": 1
    }
    response = requests.post(API_URL, json=payload).json()
    return response

def consultar_reservas_sala(sala):
    payload = {
        "jsonrpc": "2.0",
        "method": "App.consultar_reservas_sala",
        "params": {"sala": sala},
        "id": 1
    }
    response = requests.post(API_URL, json=payload).json()
    return response

def consultar_reservas_usuario(usuario):
    payload = {
        "jsonrpc": "2.0",
        "method": "App.consultar_reservas_usuario",
        "params": {"usuario": usuario},
        "id": 1
    }
    response = requests.post(API_URL, json=payload).json()
    return response

if __name__ == "__main__":
    # Exemplos de uso
    print(cadastrar_reserva("usuario1", "Sala A", "2024-05-20", "14:00"))
    print(remover_reserva("usuario1", "Sala A", "2024-05-20", "14:00"))
    print(consultar_reserva("Sala A", "2024-05-20", "14:00"))
    print(consultar_reservas_sala("Sala A"))
    print(consultar_reservas_usuario("usuario1"))
