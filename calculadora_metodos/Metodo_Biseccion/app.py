from flask import Flask, request, jsonify
from flask_cors import CORS  # Importa CORS
import sympy as sp
import math
import re  # Importar para expresiones regulares

app = Flask(__name__)
CORS(app)  # Habilita CORS para toda la aplicación

def evaluar_funcion_segura(funcion_str, x):
    try:
        # Validar que la función no contenga caracteres no permitidos
        if not re.match(r'^[0-9x+\-*/().^ ]+$', funcion_str):
            return jsonify({
                'error': 'Las funciones contienen caracteres no permitidos.',
                'mensaje': 'Solo se permiten letras, números, operadores matemáticos y paréntesis en las funciones.'
            }), 400
        
        x_sym = sp.Symbol('x')
        expr = sp.sympify(funcion_str)

        # Verificar divisiones por cero
        if x == 0 and '1/x' in funcion_str:
            raise ValueError("División por cero detectada en la evaluación.")
        
        # Verificar raíces negativas
        if isinstance(expr, sp.Pow) and expr.args[1] % 2 == 0 and expr.args[0] < 0:
            raise ValueError("Raíz negativa detectada. Se requiere un número no negativo.")

        return float(expr.subs(x_sym, x))
    
    except Exception as e:
        raise ValueError(f"Error al evaluar la función: {str(e)}")

@app.route('/biseccion', methods=['POST'])
def biseccion():
    try:
        data = request.get_json()

        # Validación de campos requeridos en el JSON
        campos_requeridos = ['punto_inicial_a', 'punto_inicial_b', 'tolerancia', 'funcion']
        for campo in campos_requeridos:
            if campo not in data:
                return jsonify({
                    'error': f'Falta el campo requerido: {campo}',
                    'mensaje': f'Por favor, asegúrese de incluir {campo}.'
                }), 400

        # Validación de que punto_a y punto_b sean numéricos
        try:
            punto_a = float(data['punto_inicial_a'])
            punto_b = float(data['punto_inicial_b'])
        except (ValueError, TypeError):
            return jsonify({
                'error': 'Los valores de punto_inicial_a y punto_inicial_b deben ser numéricos.',
                'mensaje': 'Por favor, proporcione en los puntos iniciales valores numéricos válidos.'
            }), 400

        tolerancia = float(data['tolerancia'])
        funcion = data['funcion']
        max_iteraciones = data.get('max_iteraciones', 1000)

        # Validación de que punto_a sea menor que punto_b
        if punto_a >= punto_b:
            return jsonify({
                'error': 'punto_a debe ser menor que punto_b',
                'mensaje': 'El punto a debe ser menor que el punto b'
            }), 400
        
        # Evaluación de la función en los puntos iniciales
        fa = evaluar_funcion_segura(funcion, punto_a)
        fb = evaluar_funcion_segura(funcion, punto_b)

        # Variables de control para el ciclo de iteraciones
        iteraciones = []
        function_calls = 0
        converged = False
        punto_medio_anterior = None

        # Ciclo de iteraciones
        for iteracion in range(1, max_iteraciones + 1):
            punto_medio = (punto_a + punto_b) / 2
            valor_funcion_medio = evaluar_funcion_segura(funcion, punto_medio)
            function_calls += 1

            # Calcular el error solo a partir de la segunda iteración
            if punto_medio_anterior is not None:
                error = abs((punto_medio - punto_medio_anterior) / punto_medio) * 100
            else:
                error = None  # No calculamos error en la primera iteración

            iteraciones.append({
                'iteracion': iteracion,
                'punto_a': punto_a,
                'punto_b': punto_b,
                'punto_medio': punto_medio,
                'error': error
            })

            # Verificación de convergencia
            if math.isclose(valor_funcion_medio, 0, abs_tol=tolerancia) or (error is not None and error < tolerancia):
                converged = True
                break

            # Actualización de los puntos a y b
            if fa * valor_funcion_medio < 0:
                punto_b = punto_medio
            else:
                punto_a = punto_medio
                fa = valor_funcion_medio

            punto_medio_anterior = punto_medio

        # Caso en que se alcanza el máximo de iteraciones
        if iteracion == max_iteraciones:
            return jsonify({
                'error': 'Se alcanzó el máximo de iteraciones sin convergencia',
                'mensaje': 'El proceso alcanzó el límite de iteraciones sin converger. Intente con un valor inicial diferente.'
            }), 400

        # Respuesta final
        return jsonify({
            'converged': converged,
            'function_calls': function_calls,
            'iteraciones': iteraciones,
            'resultado_final': punto_medio if converged else None,
            'numero_iteraciones': len(iteraciones)
        })

    except Exception as e:
        return jsonify({
            'error': str(e),
            'mensaje': 'Ocurrió un error inesperado en el servidor.'
        }), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5800)
