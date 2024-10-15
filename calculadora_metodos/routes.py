from flask import Blueprint, jsonify, request
from controllers import home_controller, suma_controller, resta_controller, \
    bisection_controller, punto_fijo_controller, newton_raphson_controller, secante_controller, broyden_controller

api = Blueprint('api', __name__)

@api.route('/')
def home():
    return jsonify(home_controller())


@api.route('/puntoFijo', methods=['POST'])
def puntoFijo():
    data = request.json
    equation_str = data.get('equation')
    x0 = data.get('x0', 0)
    error_tolerancia = data.get('tolerance', 1e-3)

    if not equation_str:
        return jsonify({"error": "No se proporcionó ninguna ecuación"}), 400

    resultado = punto_fijo_controller(equation_str, x0, error_tolerancia)
    return jsonify(resultado)
