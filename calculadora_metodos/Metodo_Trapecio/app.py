import numpy as np
from flask import Flask, request, jsonify
from flask_cors import CORS
import sympy as sp

app = Flask(__name__)
CORS(app)

# Función para evaluar la función en un valor x
def evaluar_funcion(funcion_str, x):
    try:
        # Usar sympy para manejar la expresión simbólica
        funcion = sp.sympify(funcion_str)
        return float(funcion.evalf(subs={sp.symbols('x'): x}))
    except Exception as e:
        raise ValueError(f"Error al evaluar la función: {str(e)}")

# Método del trapecio
def trapecio(a, b, n, funcion_str):
    # Evaluación inicial de la función en los puntos a y b
    f_a = evaluar_funcion(funcion_str, a)
    f_b = evaluar_funcion(funcion_str, b)

    # Caso n = 1 (un solo trapecio)
    if n == 1:
        area = (b - a) * (f_a + f_b) / 2
    # Caso n > 1 (más trapecios)
    elif n > 1:
        h = (b - a) / n
        suma_intermedia = 0
        for i in range(1, n):
            x_i = a + i * h
            suma_intermedia += evaluar_funcion(funcion_str, x_i)
        
        area = (h / 2) * (f_a + 2 * suma_intermedia + f_b)

    # Cálculo del error relativo
    error_relativo = abs((area - (b - a) * (f_a + f_b) / 2) / area) if area != 0 else 0

    # Determinación de convergencia
    convergencia = "Converge" if area != 0 else "Diverge"

    return area, convergencia, error_relativo

@app.route('/trapecio', methods=['POST'])
def metodo_trapecio():
    try:
        data = request.get_json()

        # Validación de parámetros faltantes
        if 'a' not in data:
            return jsonify({'error': "Falta el valor de 'a'. Ingrese el límite inferior."}), 400

        if 'b' not in data:
            return jsonify({'error': "Falta el valor de 'b'. Ingrese el límite superior."}), 400

        if 'n' not in data:
            return jsonify({'error': "Falta el valor de 'n'. Ingrese el número de subintervalos."}), 400

        if 'funcion' not in data:
            return jsonify({'error': "Falta el valor de 'funcion'. Ingrese la expresión de la función."}), 400

        # Obtener valores
        a = data['a']
        b = data['b']
        n = data['n']
        funcion_str = data['funcion']

        # Validar que a < b y n > 0
        if a >= b:
            return jsonify({'error': "El límite inferior debe ser menor que el límite superior."}), 400

        if n <= 0:
            return jsonify({'error': "El número de subintervalos debe ser mayor que cero."}), 400

        # Ejecutar el método del trapecio
        area_trapecio, convergencia, error_relativo = trapecio(a, b, n, funcion_str)

        # Devolver resultado
        return jsonify({
            'area_bajo_la_curva': area_trapecio,
            'convergencia': convergencia,
            'error_relativo': error_relativo
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5503)
