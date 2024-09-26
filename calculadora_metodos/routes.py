from flask import Blueprint, jsonify, request
from controllers import home_controller, suma_controller, resta_controller, \
    bisection_controller, punto_fijo_controller

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
    equation_str = data.get('equation')
    xi = data.get('xi', 0)
    xu = data.get('xu', 1)
    tol = data.get('tolerance', 1e-3)

    if not equation_str:
        return jsonify({"error": "No se proporcionó ninguna ecuación"}), 400

    resultado = bisection_controller(equation_str, xi, xu, tol)
    return jsonify(resultado)

@api.route('/puntoFijo', methods=['POST'])
def puntoFijo():
    data = request.json
    equation_str = data.get('equation')  # Recibe la función g(x)
    x0 = data.get('x0', 0)  # Valor inicial
    error_tolerancia = data.get('tolerance', 1e-3)  # Tolerancia opcional

    if not equation_str:
        return jsonify({"error": "No se proporcionó ninguna ecuación"}), 400

    resultado = punto_fijo_controller(equation_str, x0, error_tolerancia)
    return jsonify(resultado)