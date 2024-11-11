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
        expr = sp.sympify(expresion_str)
        return len(expr.free_symbols) > 0
    except (sp.SympifyError, TypeError):
        return False

def verificar_una_variable(funcion_str):
    try:
        # Convertir la función a una expresión simbólica y obtener las variables
        expr = sp.sympify(funcion_str)
        variables = list(expr.free_symbols)
        return len(variables) == 1, variables[0] if len(variables) == 1 else None
    except Exception:
        return False, None

def is_infinite_or_large(value):
    """Verifica si el valor es infinito o muy grande."""
    threshold = 1e10  # Umbral para considerar un valor extremadamente grande
    return abs(value) > threshold or sp.oo in [value, -value]

def calcular_derivadas(funcion_str):
    """Calcula la primera y segunda derivada de una función usando SymPy"""
    expr = sp.sympify(funcion_str)
    variable = list(expr.free_symbols)[0]  # Detectar automáticamente la variable
    primera_derivada = sp.diff(expr, variable)
    segunda_derivada = sp.diff(primera_derivada, variable)
    return str(primera_derivada), str(segunda_derivada), variable

@app.route('/newton-raphson', methods=['POST'])
def newton_raphson():
    try:
        data = request.get_json()

        # Validación de campos requeridos
        if 'punto_inicial' not in data:
            return jsonify({
                'error': 'Falta el campo punto_inicial.',
                'mensaje': 'Por favor, ingrese el punto inicial.'
            }), 400
        if 'funcion' not in data:
            return jsonify({
                'error': 'Falta el campo funcion.',
                'mensaje': 'Por favor, ingrese la ecuación de la función.'
            }), 400
        if 'tolerancia' not in data:
            return jsonify({
                'error': 'Falta el campo tolerancia.',
                'mensaje': 'Por favor, seleccione una tolerancia.'
            }), 400

        # Validación de tipo de datos y valores numéricos
        try:
            punto_inicial = float(data['punto_inicial'])
            tolerancia = float(data['tolerancia'])
        except (ValueError, TypeError):
            return jsonify({
                'error': 'El punto_inicial y la tolerancia deben ser numéricos.',
                'mensaje': 'Por favor, ingrese valores numéricos válidos.'
            }), 400

        # Validación de tolerancia
        if tolerancia <= 0:
            return jsonify({
                'error': 'La tolerancia debe ser un valor positivo.',
                'mensaje': 'Por favor, ingrese una tolerancia positiva.'
            }), 400

        funcion_str = data['funcion']
        
        # Validar la expresión de la función
        if not es_valido(funcion_str):
            return jsonify({
                'error': 'Las funciones contienen caracteres no permitidos.',
                'mensaje': 'Solo se permiten letras, números, operadores matemáticos y paréntesis en las funciones.'
            }), 400

        if not es_expresion_valida(funcion_str):
            return jsonify({
                'error': 'Las funciones deben ser expresiones matemáticas válidas.',
                'mensaje': 'Por favor, asegúrese de que las funciones sean matemáticamente correctas.'
            }), 400

        # Verificar que solo haya una variable en la expresión
        valida_variable, variable = verificar_una_variable(funcion_str)
        if not valida_variable:
            return jsonify({
                'error': 'La función debe contener exactamente una variable.',
                'mensaje': 'Asegúrese de que la función sea matemáticamente correcta y use solo una variable.'
            }), 400

        try:
            # Convertir la función a una expresión simbólica y calcular las derivadas
            funcion_expr = sp.sympify(funcion_str)
            derivada_funcion_str, segunda_derivada_funcion_str, variable = calcular_derivadas(funcion_str)

            # Convertir las expresiones de la función y sus derivadas en funciones evaluables
            funcion = lambda x: float(funcion_expr.subs(variable, x))
            derivada_funcion_expr = sp.sympify(derivada_funcion_str)
            segunda_derivada_funcion_expr = sp.sympify(segunda_derivada_funcion_str)

            derivada_funcion = lambda x: float(derivada_funcion_expr.subs(variable, x))
            segunda_derivada_funcion = lambda x: float(segunda_derivada_funcion_expr.subs(variable, x))

        except Exception as e:
            return jsonify({
                'error': 'Error al procesar la función o sus derivadas: ' + str(e),
                'mensaje': 'Ocurrió un error al procesar las funciones dadas. Asegúrese de que sean matemáticamente correctas.'
            }), 400

        max_iteraciones = data.get('max_iteraciones', 1000)

        # Validación de max_iteraciones
        if not isinstance(max_iteraciones, int) or max_iteraciones <= 0:
            return jsonify({
                'error': 'max_iteraciones debe ser un entero positivo.',
                'mensaje': 'Por favor, proporcione un número entero positivo para max_iteraciones.'
            }), 400

        # Implementación del método Newton-Raphson
        x_i = punto_inicial
        iteraciones = []
        converged = False

        for iteracion in range(max_iteraciones):
            try:
                valor_funcion = funcion(x_i)
                valor_derivada = derivada_funcion(x_i)
                
                if is_infinite_or_large(valor_funcion) or is_infinite_or_large(valor_derivada):
                    return jsonify({
                        'error': 'La función o su derivada generaron un valor infinito o muy grande.',
                        'mensaje': 'La función o su derivada produjo un valor fuera de los límites aceptables. Intente con otro punto inicial o ajuste la función.'
                    }), 400

                if valor_derivada == 0:
                    return jsonify({
                        'error': 'La derivada de la función es cero en un punto, lo que provoca una división por cero.',
                        'mensaje': 'Intente con un valor inicial diferente.'
                    }), 400

                # Cálculo del siguiente valor de x
                x_i1 = x_i - valor_funcion / valor_derivada
                diferencia = abs(x_i1 - x_i)
                error = abs(diferencia / x_i1) if x_i1 != 0 else float('inf')
                g_prima = 1 - ((derivada_funcion(x_i) ** 2 - funcion(x_i) * segunda_derivada_funcion(x_i)) / derivada_funcion(x_i) ** 2)
                estado = "Convergiendo" if abs(g_prima) < 1 else "Divergiendo"

                iteraciones.append({
                    'iteracion': iteracion,
                    'x_i': x_i,
                    'diferencia': diferencia,
                    'g_prima': g_prima,
                    'error': error,
                    'estado': estado
                })

                if diferencia <= tolerancia and abs(valor_funcion) <= tolerancia:
                    converged = True
                    break

                x_i = x_i1

            except ZeroDivisionError:
                return jsonify({
                    'error': 'División por cero en el cálculo.',
                    'mensaje': 'La derivada de la función es cero en algún punto del cálculo. Intente con un valor inicial diferente o ajuste la función.'
                }), 400

            except OverflowError:
                return jsonify({
                    'error': 'Se produjo un valor extremadamente grande en el cálculo.',
                    'mensaje': 'El cálculo generó valores demasiado grandes para procesar. Intente con otro punto inicial o ajuste la función.'
                }), 400

        if not converged:
            return jsonify({
                'error': 'Se alcanzó el máximo de iteraciones sin convergencia',
                'mensaje': 'El proceso alcanzó el límite de iteraciones sin converger. Intente con un valor inicial diferente o ajuste la función.'
            }), 400

        return jsonify({
            'converged': converged,
            'iteraciones': iteraciones,
            'resultado_final': x_i if converged else None,
            'numero_iteraciones': len(iteraciones),
            'primera_derivada': derivada_funcion_str,
            'segunda_derivada': segunda_derivada_funcion_str,
            'mensaje': f"Convergió exitosamente en {len(iteraciones)} iteraciones." if converged else 'No convergió dentro del límite de iteraciones.'
        })

    except Exception as e:
        return jsonify({
            'error': str(e),
            'mensaje': 'Ocurrió un error inesperado en el servidor.'
        }), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5200)
