from flask import Flask, request, jsonify
from flask_cors import CORS  # Importa CORS
import sympy as sp
import re  

app = Flask(__name__)
CORS(app)  # Habilita CORS para toda la aplicación

def es_valido(entrada):
    # Permite solo letras, números, paréntesis y operadores matemáticos básicos
    patron = r'^[a-zA-Z0-9+\-*/^(). ]+$'
    return re.match(patron, entrada) is not None

def es_expresion_valida(expresion_str):
    try:
        # Intenta convertir la expresión en una expresión SymPy válida
        expr = sp.sympify(expresion_str)
        # Asegura que la expresión tenga al menos una variable
        return len(expr.free_symbols) > 0
    except (sp.SympifyError, TypeError):
        return False

def calculo_error(a, b):
    try:
        return abs((a - b) / a)
    except ZeroDivisionError:
        return float('inf')  

@app.route('/punto-fijo', methods=['POST'])
def calculate_fixed_point():
    try:
        data = request.get_json()
        
        if 'Punto_inicial' not in data:
            return jsonify({
                'error': 'Falta el campo Punto_inicial.',
                'mensaje': 'Por favor, ingrese el Punto_inicial.'
            }), 400
        if 'funcion' not in data:
            return jsonify({
                'error': 'Falta el campo funcion.',
                'mensaje': 'Por favor, ingrese la ecuación original.'
            }), 400
        if 'transformada' not in data:
            return jsonify({
                'error': 'Falta el campo transformada.',
                'mensaje': 'Por favor, ingrese la ecuación despejada.'
            }), 400
        if 'tolerancia' not in data:
            return jsonify({
                'error': 'Falta el campo tolerancia.',
                'mensaje': 'Por favor, seleccione una tolerancia.'
            }), 400
        
        # Validar que el punto inicial es un número
        try:
            initial_guess = float(data['Punto_inicial'])
        except (ValueError, TypeError):
            return jsonify({
                'error': 'El Punto_inicial debe ser un número.',
                'mensaje': 'Por favor, ingrese un valor numérico válido para el Punto_inicial.'
            }), 400
            
        tolerance = float(data['tolerancia'])
        function_str = data['funcion']
        transformada_str = data['transformada']

        # Validar la tolerancia
        if tolerance <= 0:
            return jsonify({
                'error': 'La tolerancia debe ser un valor positivo',
                'mensaje': 'Por favor, ingrese una tolerancia positiva.'
            }), 400

        # Validar sintaxis y caracteres permitidos en las funciones
        if not es_valido(function_str) or not es_valido(transformada_str):
            return jsonify({
                'error': 'Las funciones contienen caracteres no permitidos.',
                'mensaje': 'Solo se permiten letras, números, operadores matemáticos y paréntesis en las funciones.'
            }), 400

        # Validar que las expresiones sean matemáticamente válidas y contengan una variable
        if not es_expresion_valida(function_str) or not es_expresion_valida(transformada_str):
            return jsonify({
                'error': 'Las funciones deben ser expresiones matemáticas válidas que incluyan una variable.',
                'mensaje': 'Por favor, asegúrese de que las funciones sean matemáticamente correctas y contengan al menos una variable, como "x".'
            }), 400

        try:
            # Verificar si la función es válida en SymPy
            function_expr = sp.sympify(function_str)
            transformada_expr = sp.sympify(transformada_str)

            # Verificar que ambas expresiones contengan exactamente una variable
            variables = list(function_expr.free_symbols | transformada_expr.free_symbols)
            if len(variables) != 1:
                return jsonify({
                    'error': 'Las funciones deben contener exactamente una variable.',
                    'mensaje': 'Asegúrese de que las funciones solo usen una variable, como "x" o "t".'
                }), 400
            variable = variables[0]
        except Exception as e:
            return jsonify({
                'error': 'Error al procesar las funciones: ' + str(e),
                'mensaje': 'Ocurrió un error al procesar las funciones dadas.'
            }), 400

        X0 = initial_guess
        error = 1.0
        steps = []
        iteraciones = 0
        max_iteraciones = 1000  # Establece un número máximo de iteraciones

        # Bucle principal para el cálculo de Punto Fijo
        while error > tolerance and iteraciones < max_iteraciones:
            X0_nuevo = transformada_expr.subs(variable, X0)
                        
            # Verificar si el resultado es complejo
            if sp.im(X0_nuevo) != 0:
                return jsonify({
                    'error': 'La función transformada generó un número complejo.',
                    'mensaje': 'La función transformada produjo un valor complejo. Intente con otro punto inicial o ajuste la función transformada.'
                }), 400

            X0_nuevo = float(X0_nuevo)  # Convertir a float después de verificar que no es complejo

            error = calculo_error(X0_nuevo, X0)
            valor_funcion = float(function_expr.subs(variable, X0_nuevo))
            iteraciones += 1
            steps.append({
                'Iteración': iteraciones,
                'X0': X0,
                'X0_nuevo': X0_nuevo,
                'error': error,
                'valor_funcion': valor_funcion
            })
            X0 = X0_nuevo

            # Verificación de convergencia
            if abs(valor_funcion) < tolerance:
                return jsonify({
                    'Resultado Final': X0,
                    'Número iteraciones': iteraciones,
                    'Iteraciones': steps,
                    'mensaje': f"Convergió exitosamente en {iteraciones} iteraciones."
                })

        # Caso en que se alcanza el máximo de iteraciones
        if iteraciones == max_iteraciones:
            return jsonify({
                'error': 'Se alcanzó el máximo de iteraciones sin convergencia',
                'mensaje': 'El proceso alcanzó el límite de iteraciones sin converger. Intente con un valor inicial diferente o ajuste la función transformada.'
            }), 400

        return jsonify({
            'Resultado Final': X0,
            'Número iteraciones': iteraciones,
            'Iteraciones': steps,
            'mensaje': f"Convergió en {iteraciones} iteraciones."
        })

    except Exception as e:
        return jsonify({
            'error': str(e),
            'mensaje': 'Ocurrió un error inesperado en el servidor.'
        }), 400
    
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5201)
