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
            raise ValueError("La función contiene caracteres no permitidos.")
        
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
        if 'punto_inicial_a' not in data or 'punto_inicial_b' not in data or 'tolerancia' not in data or 'funcion' not in data:
            return jsonify({
                'error': 'Faltan campos requeridos en la solicitud.',
                'mensaje': 'Por favor, asegúrese de incluir punto_inicial_a, punto_inicial_b, tolerancia y funcion.'
            }), 400

        try:
            punto_a = float(data['punto_inicial_a'])
            punto_b = float(data['punto_inicial_b'])
            tolerancia = float(data['tolerancia'])
        except (ValueError, TypeError):
            return jsonify({
                'error': 'Los valores de punto_inicial_a, punto_inicial_b y tolerancia deben ser numéricos.',
                'mensaje': 'Por favor, proporcione en los puntos iniciales valores numéricos válidos.'
            }), 400

        funcion = data['funcion']
        max_iteraciones = data.get('max_iteraciones', 1000)

        # Validación de entrada
        if punto_a >= punto_b:
            return jsonify({'error': 'punto_a debe ser menor que punto_b'}), 400
        
        fa = evaluar_funcion_segura(funcion, punto_a)
        fb = evaluar_funcion_segura(funcion, punto_b)
        if fa * fb >= 0:
            return jsonify({
                'error': 'Los valores de la función en los puntos iniciales deberían ser de signos opuestos.',
                'mensaje': 'Se recomienda que f(a) y f(b) tengan signos opuestos para asegurar la convergencia, pero el método de bisección puede funcionar incluso cuando los puntos iniciales tienen el mismo signo'
            }), 400 
        
        iteraciones = []
        function_calls = 0
        converged = False
        punto_medio_anterior = None

        for iteracion in range(1, max_iteraciones + 1):
            punto_medio = (punto_a + punto_b) / 2
            valor_funcion_medio = evaluar_funcion_segura(funcion, punto_medio)
            function_calls += 1

            # Calcular el error de manera segura con manejo de división por cero
            try:
                error = abs((punto_medio - punto_medio_anterior) / punto_medio) * 100 if punto_medio_anterior  is not None else 1e10
            except ZeroDivisionError:
                error = 1e10 # Si ocurre una división por cero, el error es infinito

            iteraciones.append({
                'iteracion': iteracion,
                'punto_a': punto_a,
                'punto_b': punto_b,
                'punto_medio': punto_medio,
                'error': error
            })

            if math.isclose(valor_funcion_medio, 0, abs_tol=tolerancia) or error < tolerancia:
                converged = True
                break

            if fa * valor_funcion_medio < 0:
                punto_b = punto_medio
            else:
                punto_a = punto_medio
                fa = valor_funcion_medio

            punto_medio_anterior = punto_medio

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
    app.run(host='0.0.0.0', port=5000)
