from flask import Blueprint, jsonify, request
from controllers import home_controller, suma_controller, resta_controller, \
    bisection_controller, punto_fijo_controller, newton_raphson_controller, secante_controller, broyden_controller

api = Blueprint('api', __name__)

@api.route('/')
def home():
    return jsonify(home_controller())


@api.route('/broyden', methods=['POST'])
def broyden():
    data = request.json
    f1_str = data.get('f1')
    f2_str = data.get('f2')
    x0 = data.get('x0', 0)
    y0 = data.get('y0', 0)
    tol = data.get('tolerance', 1e-6)

    if not f1_str or not f2_str:
        return jsonify({"error": "No se proporcionaron las ecuaciones f1 o f2"}), 400

    resultado = broyden_controller(f1_str, f2_str, x0, y0, tol)
    return jsonify(resultado)