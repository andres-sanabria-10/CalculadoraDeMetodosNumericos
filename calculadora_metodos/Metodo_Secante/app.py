from flask import Flask, request, jsonify
from flask_cors import CORS  # Importa CORS
import sympy as sp
import math

app = Flask(__name__)
CORS(app)  # Habilita CORS para toda la aplicación

def evaluar_funcion_segura(funcion_str, x):
    try:
        x_sym = sp.Symbol('x')
        expr = sp.sympify(funcion_str)
        return float(expr.subs(x_sym, x))
    except Exception as e:
        raise ValueError(f"Error al evaluar la función: {str(e)}")

@app.route('/secante', methods=['POST'])
def metodo_secante():
    try:
        data = request.get_json()
        x0 = float(data['x0'])
        x1 = float(data['x1'])
        tolerancia = float(data['tolerancia'])
        funcion = data['funcion']
        max_iteraciones = data.get('max_iteraciones', 100)

        # Validación de entrada
        if tolerancia <= 0:
            return jsonify({'error': 'La tolerancia debe ser mayor que 0'}), 400

        iteraciones = []
        function_calls = 0
        converged = False

        for iteracion in range(1, max_iteraciones + 1):
            fx0 = evaluar_funcion_segura(funcion, x0)
            fx1 = evaluar_funcion_segura(funcion, x1)
            function_calls += 2  # Se evalúan dos veces la función en cada iteración

            if fx1 == fx0:
                return jsonify({'error': f'División por cero: f(x0) = f(x1) en la iteración {iteracion}.'}), 400

            x2 = x1 - fx1 * (x1 - x0) / (fx1 - fx0)
            error = abs((x2 - x1) / x2) * 100 if x2 != 0 else float('inf')

            iteraciones.append({
                'iteracion': iteracion,
                'x0': x0,
                'x1': x1,
                'x2': x2,
                'error': error
            })

            if error < tolerancia:
                converged = True
                break

            # Actualizar x0 y x1 para la siguiente iteración
            x0, x1 = x1, x2

        return jsonify({
            'converged': converged,
            'function_calls': function_calls,
            'iteraciones': iteraciones,
            'resultado_final': x2 if converged else None,
            'numero_iteraciones': len(iteraciones)
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5400)
