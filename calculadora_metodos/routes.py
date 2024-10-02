from flask import Blueprint, jsonify, request
from controllers import home_controller, punto_fijo_controller, biseccion_controller  # Cambiado de .controllers a controllers

api = Blueprint('api', __name__)


@api.route('/')
def home():
    return jsonify(home_controller())

#RUTA METODO DE PUNTO FIJO

@api.route('/punto-fijo', methods=['POST'])
def punto_fijo():
    data = request.json
    g_func_str = data.get('g_func_str')
    x0 = data.get('x0', 0)  # Valor inicial por defecto es 0
    margen_error = data.get('margenError', 1e-6)  # Valor por defecto para el margen de error

    if g_func_str is None:
        return jsonify({"error": "Se debe proporcionar la función g(x) como un string."}), 400

    result = punto_fijo_controller(g_func_str, x0, margenError=margen_error)

    # Aquí puedes acceder a la raíz y las iteraciones
    if "resultado" in result:
        return jsonify({
            "raiz_encontrada": result["resultado"],
            "iteraciones": result["iteraciones"]
        })
    else:
        return jsonify(result), 400
    
