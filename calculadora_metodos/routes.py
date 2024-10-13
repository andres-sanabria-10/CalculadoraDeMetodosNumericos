from flask import Blueprint, jsonify, request
from controllers import home_controller, suma_controller, resta_controller,bisection_method # Cambiado de .controllers a controllers

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
    data = request.get_json()
    punto_a = data['punto_inicial_a']  # Debe ser pasado en minúsculas
    punto_b = data['punto_inicial_b']  # Debe ser pasado en minúsculas
    tolerancia = data['tolerancia']
    funcion = data['funcion']  # Se espera que la función sea pasada como string
    max_iteraciones = 100  # Puedes cambiar esto según tus necesidades

    resultado = bisection_method(funcion, punto_a, punto_b, tolerancia, max_iteraciones)

    return jsonify({
        'converged': resultado['converged'],
        'resultado_final': resultado['resultado_final'],
        'numero_iteraciones': resultado['numero_iteraciones'],
        'iteraciones': resultado['iteraciones']
    })