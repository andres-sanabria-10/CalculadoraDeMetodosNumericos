from flask import Blueprint, jsonify, request
from controllers import home_controller, broyden_controller  # Importamos el controlador de Broyden

api = Blueprint('api', __name__)

@api.route('/')
def home():
    return jsonify(home_controller())

# RUTA METODO BROYDEN
@api.route('/broyden', methods=['POST'])
def broyden_route():
    data = request.json
    ecuaciones = data.get('ecuaciones')
    valores_iniciales = data.get('valores_iniciales', [])
    tolerancia = data.get('tolerancia', 1e-6)
    max_iteraciones = data.get('max_iteraciones', 100)

    if ecuaciones is None or not valores_iniciales:
        return jsonify({"error": "Se deben proporcionar las ecuaciones y los valores iniciales."}), 400

    try:
        solucion, iteraciones = broyden_controller(ecuaciones, valores_iniciales, tolerancia, max_iteraciones)
        return jsonify({
            "solucion_encontrada": solucion,
            "iteraciones": iteraciones
        })
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
