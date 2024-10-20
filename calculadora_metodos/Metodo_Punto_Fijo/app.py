from flask import Flask, request, jsonify
import sympy as sp

app = Flask(__name__)

def calculo_error(a, b):
    return abs((a - b) / a)

@app.route('/punto-fijo', methods=['POST'])
def calculate_fixed_point():
    try:
        data = request.get_json()
        initial_guess = float(data['Punto_inicial'])
        tolerance = float(data['tolerancia'])
        function_str = data['función']
        transformada_str = data['transformada']

        x = sp.symbols('x')
        function_expr = sp.sympify(function_str)
        transformada_expr = sp.sympify(transformada_str)

        X0 = initial_guess
        error = 1.0
        steps = []
        iteraciones = 0
        max_iteraciones = 1000  # Establece un número máximo de iteraciones

        while error > tolerance and iteraciones < max_iteraciones:
            X0_nuevo = float(transformada_expr.subs(x, X0))
            if X0_nuevo != 0.0:
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

            if abs(valor_funcion) < tolerance:
                break

        if iteraciones == max_iteraciones:
            return jsonify({'error': 'Se alcanzó el máximo de iteraciones sin convergencia'}), 400

        return jsonify({
            'Resultado Final': X0,
            'Número iteraciones': iteraciones,
            'Iteraciones': steps
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5300)