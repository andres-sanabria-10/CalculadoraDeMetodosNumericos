from flask import Blueprint, jsonify, request
from controllers import home_controller, suma_controller, resta_controller,punto_fijo_controller # Cambiado de .controllers a controllers

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
    valor_inicial = data.get('Punto_inicial')
    tolerancia = data.get('tolerancia')
    func_inicial_str = data.get('función')
    func_despejada_str = data.get('funcion_despejada')  # Nueva clave para la función despejada
    max_iteraciones = data.get('max_iteraciones', 100)  # Valor por defecto de 100 iteraciones

    # Validar si se reciben todos los parámetros necesarios
    if valor_inicial is None or tolerancia is None or func_inicial_str is None or func_despejada_str is None:
        return jsonify({'error': 'Por favor, proporciona Punto_inicial, tolerancia, función y funcion_despejada en el cuerpo de la solicitud.'}), 400

    # Convertir los valores recibidos a los tipos necesarios
    valor_inicial = float(valor_inicial)
    tolerancia = float(tolerancia)

    # Llamar a la función de cálculo (nuevo controlador)
    result = punto_fijo_controller(func_inicial_str, func_despejada_str, valor_inicial, tolerancia, max_iteraciones)

    return jsonify(result)