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


@api.route('/punto-fijo', methods=['POST'])
def calculate_fixed_point():
    data = request.get_json()
    # Aquí nos aseguramos de que los valores vengan de Postman y no sean opcionales.
    initial_guess = data.get('Punto_inicial')
    tolerance = data.get('tolerancia')
    function_str = data.get('función')
    transformada_str = data.get('transformada')  # Nueva clave para la transformada


  # Validar si se reciben todos los parámetros necesarios
    if initial_guess is None or tolerance is None or function_str is None or transformada_str is None:
        return jsonify({'error': 'Por favor, proporciona Punto_inicial, tolerancia, función y transformada en el cuerpo de la solicitud.'}), 400

    # Convertir los valores recibidos a los tipos necesarios
    initial_guess = float(initial_guess)
    tolerance = float(tolerance)

    # Llamar a la función de cálculo usando la transformada
    result, steps, iteraciones = calculo_funcion(function_str, transformada_str, initial_guess, tolerance)

    # Preparar la respuesta
    response = {
        'Resultado Final': result,  
        'Número iteraciones': iteraciones,  
        'Iteraciones': steps  
    }

    return jsonify(response)