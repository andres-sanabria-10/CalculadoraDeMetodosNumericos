from flask import Blueprint, jsonify, request
from controllers import home_controller, suma_controller, resta_controller, broyden_controller # Cambiado de .controllers a controllers
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
    data = request.json
    equations = data.get('equations', [])
    initial_guess = data.get('initial_guess', [])
    E = float(data.get('tolerance', 1e-6))
    max_iterations = int(data.get('max_iterations', 100))

    try:
        solution, iteration_data = broyden_controller(equations, initial_guess, E, max_iterations)
        return jsonify({
            "solution": solution,
            "iterations": iteration_data
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 400