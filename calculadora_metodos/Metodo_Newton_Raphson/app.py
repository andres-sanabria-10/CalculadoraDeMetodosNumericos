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
    """Verifica que la expresión sea válida y tenga solo una variable."""
    try:
        # Procesamos la expresión usando sympy
        expr = sp.sympify(expresion_str).subs(sp.Symbol('e'), sp.exp(1))
        # Obtener las variables en la expresión
        variables = expr.free_symbols
        # Verificar que la expresión contenga exactamente una variable
        if len(variables) == 0:
            return False, "La función no contiene variables."
        if len(variables) > 1:
            return False, "La función debe contener solo la variable x"
        # Verificar que la única variable sea 'x'
        if str(variables.pop()) != 'x':
            return False, "La función debe contener solo la variable 'x'."        
        return True, ""
    except (sp.SympifyError, TypeError, ValueError):
        return False, "La función no es matemáticamente correcta o no contiene variables."

def verificar_una_variable(funcion_str):
    try:
        expr = sp.sympify(funcion_str).subs(sp.Symbol('e'), sp.exp(1))
        variables = list(expr.free_symbols)
        if len(variables) == 1:
            return True, variables[0]
        elif len(variables) == 0:
            return False, "No hay variables en la expresión."
        else:
            return False, "La función debe contener solo la variable x"
    except Exception as e:
        return False, str(e)

def is_infinite_or_large(value):
    """Verifica si el valor es infinito o muy grande."""
    threshold = 1e10  # Umbral para considerar un valor extremadamente grande
    return abs(value) > threshold or sp.oo in [value, -value]

def calcular_derivadas(funcion_str):
    """Calcula la primera y segunda derivada de una función usando SymPy"""
    expr = sp.sympify(funcion_str).subs(sp.Symbol('e'), sp.exp(1))
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
                'error': 'La función contiene caracteres no permitidos.',
                'mensaje': 'Por favor, asegúrese de que la función contenga solo caracteres permitidos como letras, números, paréntesis y operadores matemáticos básicos.'
            }), 400

        es_valida, mensaje_error = es_expresion_valida(funcion_str)
        if not es_valida:
            return jsonify({
                'error': 'La función ingresada no es válida.',
                'mensaje': mensaje_error
            }), 400

        # Verificar que solo haya una variable en la expresión
        valida_variable, variable = verificar_una_variable(funcion_str)
        if not valida_variable:
            return jsonify({
                'error': 'La función debe contener exactamente una variable.',
                'mensaje': f'Por favor, asegúrese de que la función sea matemáticamente correcta y contenga solo una variable'
            }), 400

        try:
            # Convertir la función a una expresión simbólica y calcular las derivadas
            funcion_expr = sp.sympify(funcion_str).subs(sp.Symbol('e'), sp.exp(1))
            derivada_funcion_str, segunda_derivada_funcion_str, variable = calcular_derivadas(funcion_str)

            # Convertir las expresiones de la función y sus derivadas en funciones evaluables
            funcion = lambda x: float(funcion_expr.subs(variable, x))
            derivada_funcion_expr = sp.sympify(derivada_funcion_str)
            segunda_derivada_funcion_expr = sp.sympify(segunda_derivada_funcion_str)

            derivada_funcion = lambda x: float(derivada_funcion_expr.subs(variable, x))
            segunda_derivada_funcion = lambda x: float(segunda_derivada_funcion_expr.subs(variable, x))
        except (sp.SympifyError, ValueError, TypeError) as e:
            return jsonify({
                'error': 'Error al procesar las funciones.',
                'mensaje': f'Ocurrió un error al procesar las funciones dadas. Asegúrese de que la función sea válida y no cause errores matemáticos'
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
                valor_segunda_derivada = segunda_derivada_funcion(x_i)

                if is_infinite_or_large(valor_funcion) or is_infinite_or_large(valor_derivada) or is_infinite_or_large(valor_segunda_derivada):
                    return jsonify({
                        'error': 'La función o sus derivadas generaron un valor infinito o muy grande.',
                        'mensaje': 'La función o sus derivadas produjeron un valor fuera de los límites aceptables. Intente con otro punto inicial o ajuste la función.'
                    }), 400

                if abs(valor_derivada) == 0 or abs(valor_segunda_derivada) == 0:
                    return jsonify({
                        'error': 'La derivada de la función es cercana a cero, lo que provoca una posible división por cero.',
                        'mensaje': 'Una de las derivadas de la función es cero, o revise la funcion'
                    }), 400 
                if abs(valor_derivada) < 1e-10:  # Umbral para evitar divisiones problemáticas
                    return jsonify({
                        'error': 'La derivada de la función es cercana a cero, lo que provoca una posible división por cero.',
                        'mensaje': 'La derivada de la función es cercana a cero, intente con un valor inicial diferente o revise la funcion'
                    }), 400

                if abs(valor_segunda_derivada) < 1e-10:  # Umbral para evitar divisiones problemáticas en la segunda derivada
                    return jsonify({
                        'error': 'La segunda derivada de la función es cercana a cero, lo que puede afectar la convergencia.',
                        'mensaje': 'La segunda derivada de la función es cercana a cero, intente con un valor inicial diferente o revise la funcion'
                    }), 400

                # Cálculo del siguiente valor de x
                x_i1 = x_i - valor_funcion / valor_derivada
                diferencia = abs(x_i1 - x_i)
                error = abs(diferencia / x_i1) if x_i1 != 0 else "infinito"
                g_prima = 1 - ((derivada_funcion(x_i) ** 2 - funcion(x_i) * valor_segunda_derivada) / derivada_funcion(x_i) ** 2)
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

            except Exception as e:
                return jsonify({
                    'error': 'Error inesperado durante la iteración',
                    'mensaje': 'Ocurrió un error inesperado durante la iteración. Revise la función y los valores proporcionados.'
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
            'mensaje': f"Convergó exitosamente en {len(iteraciones)} iteraciones." if converged else 'No convergió dentro del límite de iteraciones.'
        })

    except Exception as e:
        return jsonify({
            'error': 'Error en el servidor: ' + str(e),
            'mensaje': 'Ocurrió un error inesperado en el servidor'
        }), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5200)


