from flask import Flask, request, jsonify
from flask_cors import CORS  # Importa CORS
import sympy as sp

app = Flask(__name__)
CORS(app)  # Habilita CORS para toda la aplicación

def calculo_error(a, b):
    try:
        return abs((a - b) / a)
    except ZeroDivisionError:
        return float('inf')  # Retorna un valor infinito para que se detecte como error

@app.route('/punto-fijo', methods=['POST'])
def calculate_fixed_point():
    try:
        data = request.get_json()
        initial_guess = float(data['Punto_inicial'])
        tolerance = float(data['tolerancia'])

        # Validar la tolerancia
        if tolerance <= 0:
            return jsonify({'error': 'La tolerancia debe ser un valor positivo', 'mensaje': 'Por favor, ingrese una tolerancia positiva.'}), 400

        function_str = data['funcion']
        transformada_str = data['transformada']

        # Validar las funciones
        try:
            x = sp.symbols('x')
            function_expr = sp.sympify(function_str)
            transformada_expr = sp.sympify(transformada_str)
        except Exception as e:
            return jsonify({'error': 'Error al procesar las funciones: ' + str(e), 'mensaje': 'Ocurrió un error al procesar las funciones dadas.'}), 400

        X0 = initial_guess
        error = 1.0
        steps = []
        iteraciones = 0
        max_iteraciones = 1000  # Establece un número máximo de iteraciones

        while error > tolerance and iteraciones < max_iteraciones:
            try:
    
                X0_nuevo = transformada_expr.subs(x, X0)
                X0_nuevo = float(X0_nuevo)

            except TypeError:

                return jsonify({
                    'error': 'La función transformada generó un número complejo.',
                    'mensaje': 'La función transformada produjo un valor complejo. Intente con otro punto inicial o ajuste la función transformada.'
                }), 400

            if X0_nuevo == 0:
                return jsonify({
                    'error': 'División por cero detectada en el cálculo de la transformación.',
                    'mensaje': 'División por cero en la transformación. Intente con un valor inicial diferente o ajuste la función transformada.'
                }), 400

            error = calculo_error(X0_nuevo, X0)
            valor_funcion = float(function_expr.subs(x, X0_nuevo))
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
        return jsonify({'error': str(e), 'mensaje': 'Ocurrió un error inesperado en el servidor.'}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5300)
