from flask import Flask, request, jsonify
from flask_cors import CORS
import sympy as sp
import re  

app = Flask(__name__)
CORS(app)

def es_valido(entrada):
    # Permite solo letras, números, paréntesis y operadores matemáticos básicos
    patron = r'^[a-zA-Z0-9+\-*/^(). ]+$'
    return re.match(patron, entrada) is not None

def es_expresion_valida(expresion_str):
    try:
        # Convertir la cadena en una expresión de sympy
        expr = sp.sympify(expresion_str).subs(sp.Symbol('e'), sp.exp(1))
        # Verificar que la expresión contiene solo la variable 'x'
        if len(expr.free_symbols) == 0:
            raise ValueError("La función no contiene variables.")
        for variable in expr.free_symbols:
            if str(variable) != 'x':  # Si la variable no es 'x'
                raise ValueError("Solo se permite la variable 'x'.")
        return True, ""
    except (sp.SympifyError, TypeError, ValueError) as e:
        return False, f"La función no es matemáticamente correcta o no contiene solo la variable 'x'. Error: {str(e)}"


def calculo_error(a, b):
    try:
        if abs(a) < 1e-10:
            return float('inf')
        return abs((a - b) / a)
    except ZeroDivisionError:
        return float('inf')

def is_infinite_or_large(value):
    """Verifica si el valor es infinito o muy grande."""
    threshold = 1e10  # Umbral para considerar un valor extremadamente grande
    return abs(value) > threshold or sp.oo in [value, -value]

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

        if tolerance <= 0:
            return jsonify({
                'error': 'La tolerancia debe ser un valor positivo',
                'mensaje': 'Por favor, ingrese una tolerancia positiva.'
            }), 400

        if not es_valido(function_str) or not es_valido(transformada_str):
            return jsonify({
                'error': 'Las funciones contienen caracteres no permitidos.',
                'mensaje': 'Solo se permiten letras, números, operadores matemáticos y paréntesis en las funciones.'
            }), 400

        if not es_expresion_valida(function_str) or not es_expresion_valida(transformada_str):
            return jsonify({
                'error': 'Las funciones deben ser expresiones matemáticas válidas.',
                'mensaje': 'Por favor, asegúrese de que las funciones sean matemáticamente correctas y contenga solo la variable x'
            }), 400

        try:
            # Procesar las expresiones
            function_expr = sp.sympify(function_str).subs(sp.Symbol('e'), sp.exp(1))
            transformada_expr = sp.sympify(transformada_str).subs(sp.Symbol('e'), sp.exp(1))
            
            # Obtener las variables de ambas expresiones
            variables = list(function_expr.free_symbols | transformada_expr.free_symbols)

            # Validar que haya exactamente una variable y que sea 'x'
            if len(variables) != 1 or str(variables[0]) != 'x':
                return jsonify({
                    'error': 'Las funciones deben contener exactamente una variable, y esa debe ser "x".',
                    'mensaje': 'Asegúrese de que las funciones sean matemáticamente correctas y contengan solo la variable "x".'
                }), 400

            # Asegurarse de que la expresión no sea solo un número (es decir, que contenga variables)
            if function_expr.is_number or transformada_expr.is_number:
                return jsonify({
                    'error': 'Las funciones no pueden ser solo números.',
                    'mensaje': 'Asegúrese de que las funciones contengan al menos una variable "x".'
                }), 400

            variable = variables[0]

        except Exception as e:
            return jsonify({
                'error': 'Error al procesar las funciones: ' + str(e),
                'mensaje': 'Ocurrió un error al procesar las funciones dadas: Asegúrese de que las funciones sean matemáticamente correctas'
            }), 400



        X0 = initial_guess
        error = 1.0
        steps = []
        iteraciones = 0
        max_iteraciones = 1000

        while error > tolerance and iteraciones < max_iteraciones:
            X0_nuevo = transformada_expr.subs(variable, X0)
            if sp.im(X0_nuevo) != 0:
                return jsonify({
                    'error': 'La función transformada generó un número complejo.',
                    'mensaje': 'La función transformada produjo un valor complejo. Intente con otro punto inicial o ajuste la función transformada.'
                }), 400

            X0_nuevo = float(X0_nuevo)
            if is_infinite_or_large(X0_nuevo):
                return jsonify({
                    'error': 'La función transformada generó un valor infinito o muy grande.',
                    'mensaje': 'La función transformada produjo un valor fuera de los límites aceptables. Intente con otro punto inicial o ajuste la función transformada.'
                }), 400

            error = calculo_error(X0_nuevo, X0)
            if is_infinite_or_large(error):
                return jsonify({
                    'error': 'Se produjo un error de cálculo infinito o muy grande.',
                    'mensaje': 'El error en los cálculos se desbordó. Intente con otro punto inicial o ajuste la función transformada.'
                }), 400

            valor_funcion = float(function_expr.subs(variable, X0_nuevo))
            if is_infinite_or_large(valor_funcion):
                return jsonify({
                    'error': 'La evaluación de la función produjo un valor infinito o muy grande.',
                    'mensaje': 'El valor calculado de la función es demasiado grande. Intente con otro punto inicial o ajuste la función.'
                }), 400

            iteraciones += 1
            steps.append({
                'Iteración': iteraciones,
                'X0': X0,
                'X0_nuevo': X0_nuevo,
                'error': error,
                'valor_funcion': valor_funcion
            })
            X0 = X0_nuevo

            if abs(valor_funcion) < tolerance:
                return jsonify({
                    'Resultado Final': X0,
                    'Número iteraciones': iteraciones,
                    'Iteraciones': steps,
                    'mensaje': f"Convergió exitosamente en {iteraciones} iteraciones."
                })

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
