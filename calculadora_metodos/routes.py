from flask import Blueprint, jsonify, request
from controllers import home_controller, suma_controller, resta_controller, broyden_good # Cambiado de .controllers a controllers
import numpy as np
import scipy.linalg as sla


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

# Ruta para resolver el sistema de ecuaciones usando el método de Broyden
@api.route('/broyden', methods=['POST'])
def broyden():
    data = request.get_json()
    f_equations = data.get('equations', [])
    initial_values = data.get('initial_values', [])  # Valores iniciales como lista
    tol = data.get('tolerance', 1e-10)
    max_iters = data.get('maxIters', 50)

    # Asegurarse de que las dimensiones sean correctas
    if len(initial_values) != len(f_equations):
        return jsonify({"error": "El número de valores iniciales debe coincidir con el número de ecuaciones."}), 400

    iterations, variables, error_message = broyden_good(initial_values, f_equations, tol, max_iters)

    if error_message:
        return jsonify({"iterations": iterations, "variables": variables.tolist(), "error": error_message})

    return jsonify({
        "iterations": iterations,
        "variables": variables.tolist()
    })