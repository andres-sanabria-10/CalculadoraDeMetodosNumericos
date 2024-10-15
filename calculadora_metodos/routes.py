from flask import Blueprint, jsonify, request
from controllers import home_controller, suma_controller, resta_controller, \
    bisection_controller, punto_fijo_controller, newton_raphson_controller, secante_controller, broyden_controller

api = Blueprint('api', __name__)

@api.route('/')
def home():
    return jsonify(home_controller())


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
