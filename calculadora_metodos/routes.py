from flask import Blueprint, jsonify, request
from controllers import home_controller, suma_controller, resta_controller, \
    bisection_controller, punto_fijo_controller, newton_raphson_controller, secante_controller, broyden_controller

api = Blueprint('api', __name__)

@api.route('/')
def home():
    return jsonify(home_controller())


@api.route('/newtonRaphson', methods=['POST'])
def newton_raphson():
    data = request.json
    equation_str = data.get('equation')
    derivative_str = data.get('derivative')
    x0 = data.get('x0', 0)
    tol = data.get('tolerance', 1e-3)

    if not equation_str or not derivative_str:
        return jsonify({"error": "No se proporcionó la ecuación o la derivada"}), 400

    resultado = newton_raphson_controller(equation_str, derivative_str, x0, tol)
    return jsonify(resultado)