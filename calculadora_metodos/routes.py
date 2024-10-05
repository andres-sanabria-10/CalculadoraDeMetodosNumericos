from flask import Blueprint, jsonify, request
from controllers import home_controller, suma_controller, resta_controller, newton_raphson_calculation # Cambiado de .controllers a controllers

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
def calculate():
    data = request.json
    func_expr = data.get('function')  # La función a evaluar
    x0 = data.get('x0', 1)  # Valor inicial
    E = data.get('tolerance', 10**-3)  # Tolerancia
    max_iterations = data.get('max_iterations', 100)  # Iteraciones máximas

    # Verificar si se ha proporcionado la función
    if not func_expr:
        return jsonify({"error": "La función es requerida."}), 400

    try:
        # Ejecutar el método de Newton-Raphson
        root, iterations_data = newton_raphson_calculation(func_expr, x0, E, max_iterations)
        
        # Convertir los datos de iteraciones a un formato JSON
        iterations_json = iterations_data.to_dict(orient='records')

        response = {
            "root": root,
            "iterations": iterations_json
        }

        return jsonify(response), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
