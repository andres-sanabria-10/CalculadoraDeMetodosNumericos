from flask import Flask, request, jsonify
import sympy as sp
import math
app = Flask(__name__)

def evaluar_funcion_segura(funcion_str, x):
    try:
        x_sym = sp.Symbol('x')
        expr = sp.sympify(funcion_str)
        return float(expr.subs(x_sym, x))
    except Exception as e:
        raise ValueError(f"Error al evaluar la función: {str(e)}")

@app.route('/biseccion', methods=['POST'])
def biseccion():
    try:
        data = request.get_json()
        punto_a = float(data['punto_inicial_a'])
        punto_b = float(data['punto_inicial_b'])
        tolerancia = float(data['tolerancia'])
        funcion = data['funcion']
        max_iteraciones = data.get('max_iteraciones', 100)

        # Validación de entrada
        if punto_a >= punto_b:
            return jsonify({'error': 'punto_a debe ser menor que punto_b'}), 400
        
        fa = evaluar_funcion_segura(funcion, punto_a)
        fb = evaluar_funcion_segura(funcion, punto_b)
        if fa * fb >= 0:
            return jsonify({'error': 'La función debe tener signos opuestos en los puntos iniciales'}), 400

        iteraciones = []
        function_calls = 0
        converged = False
        punto_medio_anterior = None

        for iteracion in range(1, max_iteraciones + 1):
            punto_medio = (punto_a + punto_b) / 2
            valor_funcion_medio = evaluar_funcion_segura(funcion, punto_medio)
            function_calls += 1

            error = abs((punto_medio - punto_medio_anterior) / punto_medio) * 100 if punto_medio_anterior is not None else float('inf')

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
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)