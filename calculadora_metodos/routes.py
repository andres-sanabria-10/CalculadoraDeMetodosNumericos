from flask import Blueprint, jsonify, request
from controllers import home_controller, metodo_newton_controller

api = Blueprint('api', __name__)

@api.route('/')
def home():
    return jsonify(home_controller())

@api.route('/newton', methods=['POST'])
def newton_route():
    data = request.json
    ecuacion = data.get('ecuacion')
    x_inicial = data.get('x_inicial')
    tolerancia = data.get('tolerancia')
    max_iter = data.get('max_iter')

    # Validar que los parámetros estén presentes
    if ecuacion is None or x_inicial is None or tolerancia is None or max_iter is None:
        return jsonify({'error': 'Faltan parámetros. Proporcione ecuacion, x_inicial, tolerancia y max_iter.'}), 400

    try:
        resultado, iteraciones = metodo_newton_controller(ecuacion, x_inicial, tolerancia, max_iter)
        return jsonify({
            "resultado": resultado,
            "iteraciones": iteraciones
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500
