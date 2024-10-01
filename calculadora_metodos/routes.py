from flask import Blueprint, jsonify, request
from controllers import home_controller, suma_controller, resta_controller, biseccion_controller,calcular_puntos_punto_fijo  # Cambiado de .controllers a controllers

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

@api.route('/biseccion', methods=['POST'])
def biseccion():
    data = request.json
    func_str = data.get('func_str', '')
    a = float(data.get('a', 0))
    b = float(data.get('b', 0))
    tolerancia = float(data.get('tolerancia', 1e-6))
    max_iteraciones = int(data.get('max_iteraciones', 100))
    return jsonify(biseccion_controller(func_str, a, b, tolerancia, max_iteraciones))

@api.route('/punto-fijo', methods=['POST'])
def calcular_punto_fijo():
    try:
        # Obtener los datos del cuerpo de la solicitud
        data = request.get_json()
        
        # Verificar si el cuerpo de la solicitud está vacío
        if data is None:
            return jsonify({'error': 'El cuerpo de la solicitud está vacío o mal formado'}), 400
        
        # Extraer las variables necesarias
        f = data.get('f')
        g_list = data.get('g_list')
        x0 = data.get('x0')
        tolerancia = data.get('tolerancia')
        
        # Verificar si se proporcionaron todos los parámetros necesarios
        if not f or not g_list or x0 is None or tolerancia is None:
            return jsonify({'error': 'Faltan parámetros. Se requiere f, g_list, x0, y tolerancia'}), 400
        
        # Convertir x0 y tolerancia a float (si no lo son ya)
        try:
            x0 = float(x0)
            tolerancia = float(tolerancia)
        except ValueError:
            return jsonify({'error': 'x0 y tolerancia deben ser números válidos'}), 400

        # Llamar a la función de cálculo
        puntos, x_final, iteraciones, convergio = calcular_puntos_punto_fijo (f, g_list, x0, tolerancia)
        
        # Devolver los resultados
        return jsonify({
            'puntos': puntos,
            'iteraciones': iteraciones,
            'convergio': convergio,
            'raiz': x_final
        }), 200
    
    except Exception as e:
        # Devolver el error con un mensaje claro
        return jsonify({'error': 'Error interno en el servidor: ' + str(e)}), 500