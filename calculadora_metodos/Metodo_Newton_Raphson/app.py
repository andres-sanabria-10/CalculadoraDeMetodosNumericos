from flask import Flask, request, jsonify
from flask_cors import CORS
import sympy as sp
import math

app = Flask(__name__)
CORS(app)

def evaluar_funcion_segura(funcion, x):
    try:
        return float(funcion(x))
    except Exception as e:
        raise ValueError(f"Error al evaluar la función: {str(e)}")

def calcular_derivadas(funcion_str):
    """Calcula la primera y segunda derivada de una función usando SymPy"""
    x_sym = sp.Symbol('x')
    expr = sp.sympify(funcion_str)
    primera_derivada = sp.diff(expr, x_sym)
    segunda_derivada = sp.diff(primera_derivada, x_sym)
    return str(primera_derivada), str(segunda_derivada)

@app.route('/newton-raphson', methods=['POST'])
def newton_raphson():
    try:
        data = request.get_json()

        # Validación de campos requeridos
        if 'punto_inicial' not in data or 'tolerancia' not in data or 'funcion' not in data:
            return jsonify({
                'error': 'Faltan campos requeridos en la solicitud.',
                'mensaje': 'Por favor, incluya punto_inicial, tolerancia y función'
            }), 400

        # Validación de tipo de datos y valores numéricos
        try:
            punto_inicial = float(data['punto_inicial'])
            tolerancia = float(data['tolerancia'])
        except (ValueError, TypeError):
            return jsonify({
                'error': 'Los valores de punto_inicial y tolerancia deben ser numéricos.',
                'mensaje': 'Por favor, proporcione valores numéricos válidos.'
            }), 400

        # Obtiene la función y, si no están, calcula las derivadas
        funcion_str = data['funcion']
        derivada_funcion_str = data.get('derivada')
        segunda_derivada_funcion_str = data.get('segunda_derivada')

        if not derivada_funcion_str or not segunda_derivada_funcion_str:
            derivada_funcion_str, segunda_derivada_funcion_str = calcular_derivadas(funcion_str)

        # Convertir las funciones y derivadas a funciones evaluables
        funcion = lambda x: eval(funcion_str, {"x": x, "math": math})
        derivada_funcion = lambda x: eval(derivada_funcion_str, {"x": x, "math": math})
        segunda_derivada_funcion = lambda x: eval(segunda_derivada_funcion_str, {"x": x, "math": math})

        max_iteraciones = data.get('max_iteraciones', 100)

        # Validación de tolerancia
        if tolerancia <= 0:
            return jsonify({'error': 'La tolerancia debe ser mayor que 0.'}), 400

        # Validación de max_iteraciones
        if not isinstance(max_iteraciones, int) or max_iteraciones <= 0:
            return jsonify({
                'error': 'max_iteraciones debe ser un entero positivo.',
                'mensaje': 'Por favor, proporcione un número entero positivo para max_iteraciones.'
            }), 400

        # Implementación del método Newton-Raphson
        def g(x):
            return x - funcion(x) / derivada_funcion(x)

        x_i = punto_inicial
        iteraciones = []
        converged = False

        for iteracion in range(max_iteraciones):
            x_i1 = g(x_i)
            diferencia = abs(x_i1 - x_i)
            error = abs(diferencia / x_i1) if x_i1 != 0 else float('inf')
            g_prima = 1 - (derivada_funcion(x_i)**2 - funcion(x_i) * segunda_derivada_funcion(x_i)) / derivada_funcion(x_i)**2
            estado = "Convergiendo" if abs(g_prima) else "Divergiendo"
            
            iteraciones.append({
                'iteracion': iteracion,
                'x_i': x_i,
                'diferencia': diferencia,
                'g_prima': g_prima,
                'error': error,
                'estado': estado
            })

            x_i = x_i1
            if diferencia <= tolerancia and abs(funcion(x_i)) <= tolerancia:
                converged = True
                break

        return jsonify({
            'converged': converged,
            'iteraciones': iteraciones,
            'resultado_final': x_i if converged else None,
            'numero_iteraciones': len(iteraciones),
            'primera_derivada': derivada_funcion_str,    # Añade la primera derivada
            'segunda_derivada': segunda_derivada_funcion_str  # Añade la segunda derivada
        })

    except Exception as e:
        return jsonify({
            'error': str(e),
            'mensaje': 'Ocurrió un error inesperado en el servidor.'
        }), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5200)
