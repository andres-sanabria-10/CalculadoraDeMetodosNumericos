from flask import Blueprint, jsonify, request
from controllers import home_controller, suma_controller, resta_controller,calculo_funcion # Cambiado de .controllers a controllers

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

# Ruta principal para calcular la raíz y el error
@api.route('/punto-fijo', methods=['POST'])
def calculate_fixed_point():
    data = request.get_json()
    initial_guess = data.get('Punto_inicial', 1.5)
    tolerance = data.get('tolerancia', 0.000001)
    function_str = data.get('función', '-1 / (2 * (sqrt(x**3) + (x**2 / 3.5) - 4))')

    result, steps, iteraciones = calculo_funcion(function_str, initial_guess, tolerance)

    response = {
        'Número iteraciones': iteraciones,  # Mover el número de iteraciones a la parte superior
        'Resultado Final': result,  # Mover el resultado final a la parte superior
        'Iteraciones': steps  # Colocar las iteraciones completas abajo
    }

    return jsonify(response)