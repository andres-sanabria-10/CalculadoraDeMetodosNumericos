from flask import Blueprint, jsonify, request
from controllers import home_controller, suma_controller, resta_controller, \
    bisection_controller, punto_fijo_controller, newton_raphson_controller, secante_controller, broyden_controller

api = Blueprint('api', __name__)

@api.route('/')
def home():
    return jsonify(home_controller())


@api.route('/secante', methods=['POST'])
def secante():
    data = request.json
    equation_str = data.get('equation')
    x0 = data.get('x0', 0)
    x1 = data.get('x1', 1)
    tol = data.get('tolerance', 1e-3)

    if not equation_str:
        return jsonify({"error": "No se proporcionó ninguna ecuación"}), 400

    resultado = secante_controller(equation_str, x0, x1, tol)
    return jsonify(resultado)
