from flask import Flask, request, jsonify
from flask_cors import CORS
import sympy as sp
import math

app = Flask(__name__)
CORS(app)

def evaluar_funcion_segura(funcion_str, x):
    try:
        x_sym = sp.Symbol('x')
        expr = sp.sympify(funcion_str)
        return float(expr.subs(x_sym, x))
    except Exception as e:
        raise ValueError(f"Error al evaluar la función: {str(e)}")

def derivada_funcion_segura(funcion_str, x):
    try:
        x_sym = sp.Symbol('x')
        expr = sp.sympify(funcion_str)
        derivada_expr = sp.diff(expr, x_sym)
        return float(derivada_expr.subs(x_sym, x))
    except Exception as e:
        raise ValueError(f"Error al evaluar la derivada de la función: {str(e)}")

@app.route('/newton-raphson', methods=['POST'])
def newton_raphson():
    try:
        data = request.get_json()

        # Validación de campos requeridos
        if 'punto_inicial' not in data or 'tolerancia' not in data or 'funcion' not in data or 'funcion_derivada' not in data:
            return jsonify({
                'error': 'Faltan campos requeridos en la solicitud.',
                'mensaje': 'Por favor, incluya punto_inicial, tolerancia, función y su derivada'
            }), 400

        # Validación de tipo de datos y valores numéricos
        try:
            punto_inicial = float(data['punto_inicial'])
            tolerancia = float(data['tolerancia'])
        except (ValueError, TypeError):
            return jsonify({
                'error': 'El valor de punto_inicial debe ser numérico.',
                'mensaje': 'Por favor, proporcione valores numéricos válidos para punto_inicial.'
            }), 400

        funcion = data['funcion']
        max_iteraciones = data.get('max_iteraciones', 1000)

        # Validación de valor positivo para la tolerancia
        if tolerancia <= 0:
            return jsonify({'error': 'La tolerancia debe ser mayor que 0.'}), 400

        # Validación de max_iteraciones
        if not isinstance(max_iteraciones, int) or max_iteraciones <= 0:
            return jsonify({
                'error': 'max_iteraciones debe ser un entero positivo.',
                'mensaje': 'Por favor, proporcione un número entero positivo para max_iteraciones.'
            }), 400

        iteraciones = []
        function_calls = 0
        converged = False
        x_anterior = punto_inicial

        for iteracion in range(1, max_iteraciones + 1):
            # Evaluar función y derivada en el punto actual
            fx = evaluar_funcion_segura(funcion, x_anterior)
            dfx = derivada_funcion_segura(funcion, x_anterior)
            function_calls += 2

            # Validar si la derivada es cero
            if dfx == 0:
                return jsonify({
                    'error': f'La derivada es cero en x = {x_anterior}. No se puede continuar.',
                    'mensaje': 'El método de Newton-Raphson no puede avanzar si la derivada es cero.'
                }), 400

            # Calcular el siguiente punto y el error relativo
            x_nuevo = x_anterior - fx / dfx
            error = abs((x_nuevo - x_anterior) / x_nuevo) * 100 if x_nuevo != 0 else float('inf')

            iteraciones.append({
                'iteracion': iteracion,
                'x_anterior': x_anterior,
                'x_nuevo': x_nuevo,
                'error': error
            })

            # Comprobar convergencia
            if math.isclose(fx, 0, abs_tol=tolerancia) or error < tolerancia:
                converged = True
                break

            x_anterior = x_nuevo

        return jsonify({
            'converged': converged,
            'function_calls': function_calls,
            'iteraciones': iteraciones,
            'resultado_final': x_nuevo if converged else None,
            'numero_iteraciones': len(iteraciones)
        })

    except Exception as e:
        return jsonify({
            'error': str(e),
            'mensaje': 'Ocurrió un error inesperado en el servidor.'
        }), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5200)
