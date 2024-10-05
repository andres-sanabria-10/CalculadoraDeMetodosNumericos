from flask import Blueprint, jsonify, request
from controllers import home_controller, suma_controller, resta_controller, secante_controller # Cambiado de .controllers a controllers

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

@api.route('/secante', methods=['POST'])
def secante():
    # Obtener datos del cuerpo de la solicitud
    data = request.json
    func_str = data.get('func_str', '')
    x0 = float(data.get('x0', 0))
    x1 = float(data.get('x1', 1))
    E = float(data.get('E', 1e-6))
    max_iterations = int(data.get('max_iterations', 100))

    # Llamar al controlador del método de la secante
    result = secante_controller(func_str, x0, x1, E, max_iterations)
    
    # Retornar el resultado como JSON
    return jsonify(result)

