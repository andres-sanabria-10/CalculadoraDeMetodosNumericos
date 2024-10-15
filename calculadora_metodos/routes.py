from flask import Blueprint, jsonify, request
from controllers import home_controller, metodo_secante_controller

api = Blueprint('api', __name__)

@api.route('/')
def home():
    return jsonify(home_controller())


@api.route('/secante', methods=['POST'])
def secante_route():
    data = request.json
    ecuacion = data.get('ecuacion')
    x0 = data.get('x0')
    x1 = data.get('x1')
    tolerancia = data.get('tolerancia')
    max_iter = data.get('max_iter')

    # Validar que los parámetros estén presentes
    if ecuacion is None or x0 is None or x1 is None or tolerancia is None or max_iter is None:
        return jsonify({'error': 'Faltan parámetros. Proporcione ecuacion, x0, x1, tolerancia y max_iter.'}), 400

    try:
        resultado, iteraciones = metodo_secante_controller(ecuacion, x0, x1, tolerancia, max_iter)
        return jsonify({
            "resultado": resultado,
            "iteraciones": iteraciones
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500
