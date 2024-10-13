from flask import Blueprint, jsonify, request
from controllers import home_controller, suma_controller, resta_controller, newton_raphson_controller # Cambiado de .controllers a controllers

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


@api.route('/newton-raphson', methods=['POST'])
def newton_raphson():
    data = request.json
    func_str = data.get('func_str')
    func_prime_str = data.get('func_prime_str')
    x0 = data.get('x0')
    E = data.get('E')
    max_iterations = data.get('max_iterations')
    
    try:
        root, iteration_data = newton_raphson_controller(func_str, func_prime_str, x0, E, max_iterations)
        return jsonify({
            "raiz": root,
            "iteraciones": iteration_data
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    