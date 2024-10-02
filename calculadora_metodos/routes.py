from flask import Blueprint, jsonify, request
from controllers import home_controller, biseccion_controller  # Cambiado de .controllers a controllers

api = Blueprint('api', __name__)

@api.route('/')
def home():
    return jsonify(home_controller())

#RUTA METODO BISECCION
@api.route('/biseccion', methods=['POST'])
def biseccion_route():
    data = request.json
    func_input = data.get('func_input')
    Xi = data.get('Xi', 0)
    Xu = data.get('Xu', 0)
    error = data.get('error', 1e-6)

    if func_input is None:
        return jsonify({"error": "Se debe proporcionar la función f(x) como un string."}), 400

    try:
        raiz, iteraciones = biseccion_controller(func_input, Xi, Xu, error)
        return jsonify({
            "raiz_encontrada": raiz,
            "iteraciones": iteraciones
        })
    except ValueError as e:
        return jsonify({"error": str(e)}), 400