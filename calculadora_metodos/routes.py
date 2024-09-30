from flask import Blueprint, jsonify, request
from controllers import home_controller, suma_controller, resta_controller, biseccion_controller,punto_fijo_controller  # Cambiado de .controllers a controllers

api = Blueprint('api', __name__)

@api.route('/')
def home():
    return jsonify(home_controller())

@api.route('/suma', methods=['POST'])
def suma():
    data = request.json
    a = data.get('a', 0)
    b = data.get('b', 0)
    return jsonify(suma_controller(a, b))

@api.route('/resta', methods=['POST'])
def resta():
    data = request.json
    a = data.get('a', 0)
    b = data.get('b', 0)
    return jsonify(resta_controller(a, b))

@api.route('/biseccion', methods=['POST'])
def biseccion():
    data = request.json
    func_str = data.get('func_str', '')
    a = float(data.get('a', 0))
    b = float(data.get('b', 0))
    tolerancia = float(data.get('tolerancia', 1e-6))
    max_iteraciones = int(data.get('max_iteraciones', 100))
    return jsonify(biseccion_controller(func_str, a, b, tolerancia, max_iteraciones))


@api.route('/puntofijo', methods=['POST'])
def punto_fijo():
    try:
        data = request.json
        func_inicial_str = data['func_inicial_str']
        func_despejada_str = data['func_despejada_str']
        valor_inicial = float(data['valor_inicial'])
        tolerancia = float(data.get('tolerancia', 1e-6))
        max_iteraciones = int(data.get('max_iteraciones', 100))
        
        resultado = punto_fijo_controller(func_inicial_str, func_despejada_str, valor_inicial, tolerancia, max_iteraciones)
        return jsonify(resultado) 
    except Exception as e:
        return jsonify({"error": str(e)}), 500