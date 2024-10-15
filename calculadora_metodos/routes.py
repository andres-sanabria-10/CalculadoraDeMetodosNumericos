from flask import Blueprint, jsonify, request
from controllers import broyden_controller,secante_controller, newton_raphson_controller,bisection_method,home_controller,calculo_funcion, suma_controller, resta_controller,punto_fijo_controller # Cambiado de .controllers a controllers

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

@api.route('/punto-fijo', methods=['POST'])
def calculate_fixed_point():
    data = request.get_json()
    # Aquí nos aseguramos de que los valores vengan de Postman y no sean opcionales.
    initial_guess = data.get('Punto_inicial')
    tolerance = data.get('tolerancia')
    function_str = data.get('función')
    transformada_str = data.get('transformada')  # Nueva clave para la transformada


  # Validar si se reciben todos los parámetros necesarios
    if initial_guess is None or tolerance is None or function_str is None or transformada_str is None:
        return jsonify({'error': 'Por favor, proporciona Punto_inicial, tolerancia, función y transformada en el cuerpo de la solicitud.'}), 400

    # Convertir los valores recibidos a los tipos necesarios
    initial_guess = float(initial_guess)
    tolerance = float(tolerance)

    # Llamar a la función de cálculo usando la transformada
    result, steps, iteraciones = calculo_funcion(function_str, transformada_str, initial_guess, tolerance)

    # Preparar la respuesta
    response = {
        'Resultado Final': result,  
        'Número iteraciones': iteraciones,  
        'Iteraciones': steps  
    }

    return jsonify(response)


@api.route('/biseccion', methods=['POST'])
def biseccion():
    data = request.get_json()
    punto_a = data['punto_inicial_a']  # Debe ser pasado en minúsculas
    punto_b = data['punto_inicial_b']  # Debe ser pasado en minúsculas
    tolerancia = data['tolerancia']
    funcion = data['funcion']  # Se espera que la función sea pasada como string
    max_iteraciones = 100  # Puedes cambiar esto según tus necesidades

    resultado = bisection_method(funcion, punto_a, punto_b, tolerancia, max_iteraciones)

    return jsonify({
        'converged': resultado['converged'],
        'resultado_final': resultado['resultado_final'],
        'numero_iteraciones': resultado['numero_iteraciones'],
        'iteraciones': resultado['iteraciones']
    })
    
    
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
    
@api.route('/secante', methods=['POST'])
def secante():
    # Obtener datos del cuerpo de la solicitud
    data = request.json
    func_str = data.get('func_str', '')
    x0 = float(data.get('x0', 0))
    x1 = float(data.get('x1', 1))
    E = float(data.get('E', 1e-6))
    max_iterations = int(data.get('max_iterations', 100))

    # Verificar que func_str no esté vacío
    if not func_str:
        return jsonify({"error": "La función no debe estar vacía"}), 400

    # Llamar al controlador del método de la secante
    result = secante_controller(func_str, x0, x1, E, max_iterations)
    
    # Retornar el resultado como JSON
    return jsonify(result)

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