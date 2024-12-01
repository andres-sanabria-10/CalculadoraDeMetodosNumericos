import numpy as np
from flask import Flask, request, jsonify
from flask_cors import CORS
import sympy as sp

app = Flask(__name__)
CORS(app)

# Función para evaluar la función de forma segura
def evaluar_funcion_segura(funcion_str, x):
    try:
        x_sym = sp.Symbol('x')
        expr = sp.sympify(funcion_str).subs(sp.Symbol('e'), sp.exp(1))  # Sustituir 'e' por exp(1)
        resultado = expr.subs(x_sym, x)
        if sp.im(resultado) != 0:  # Verifica si el resultado tiene una parte imaginaria
            raise ValueError("La función generó un número complejo.")
        if abs(resultado) > 1e10:  # Umbral para detectar valores extremadamente grandes
            raise ValueError("La función generó un valor demasiado grande.")
        return float(resultado)
    except Exception as e:
        raise ValueError(f"{str(e)}")

# Validar la función
def validar_funcion(funcion_str):
    try:
        expr = sp.sympify(funcion_str).subs(sp.Symbol('e'), sp.exp(1))  # Convierte la cadena en una expresión simbólica
        variables = expr.free_symbols  # Obtiene las variables simbólicas libres
        if len(variables) != 1 or str(next(iter(variables))) != 'x':
            raise ValueError("La función debe contener exactamente una variable, y debe ser 'x'.")
        return True
    except sp.SympifyError as e:  # Errores relacionados con la conversión de sympy
        raise ValueError("La función proporcionada no es una expresión válida.")
    except ValueError as e:
        raise e

# Método del trapecio
def trapecio(a, b, n, funcion_str):
    try:
        # Validar la función antes de proceder
        validar_funcion(funcion_str)

        # Evaluación inicial de la función en los puntos a y b
        f_a = evaluar_funcion_segura(funcion_str, a)
        f_b = evaluar_funcion_segura(funcion_str, b)

        # Caso n = 1 (un solo trapecio)
        if n == 1:
            area = (b - a) * (f_a + f_b) / 2
        # Caso n > 1 (más trapecios)
        elif n > 1:
            h = (b - a) / n
            suma_intermedia = 0
            for i in range(1, n):
                x_i = a + i * h
                suma_intermedia += evaluar_funcion_segura(funcion_str, x_i)

            area = (h / 2) * (f_a + 2 * suma_intermedia + f_b)

        # Cálculo del error relativo
        error_relativo = abs((area - (b - a) * (f_a + f_b) / 2) / area) if area != 0 else 0

        # Determinación de convergencia
        convergencia = "Converge" if area != 0 else "Diverge"

        return area, convergencia, error_relativo
    except Exception as e:
        raise ValueError(f"{str(e)}")

@app.route('/trapecio', methods=['POST'])
def metodo_trapecio():
    try:
        data = request.get_json()

        # Validación de parámetros faltantes
        if 'a' not in data:
             return jsonify({'error': 'Error', 'mensaje': 'Falta el valor de a. Ingrese el límite inferior'}), 400
        if 'b' not in data:
            return jsonify({'error': 'Error', 'mensaje': 'Falta el valor de b. Ingrese el límite superior'}), 400
        if 'n' not in data:
            return jsonify({'error': 'Error', 'mensaje': 'Falta el valor de n. Ingrese el numero de subintervalos'}), 400
        if 'funcion' not in data:
           return jsonify({'error': 'Error', 'mensaje': 'Ingrese la funcion'}), 400

        # Obtener valores
        a = data['a']
        b = data['b']
        n = data['n']
        funcion_str = data['funcion']

        # Validar que a < b y n > 0
        if a >= b:
            return jsonify({'error': 'Error', 'mensaje': 'El límite inferior debe ser menor que el límite superior'}), 400
        if n <= 0:
            return jsonify({'error': 'Error', 'mensaje': 'El número de subintervalos debe ser mayor que cero'}), 400

        # Ejecutar el método del trapecio
        area_trapecio, convergencia, error_relativo = trapecio(a, b, n, funcion_str)

        # Devolver resultado
        return jsonify({
            'area_bajo_la_curva': area_trapecio,
            'convergencia': convergencia,
            'error_relativo': error_relativo
        })
    except ValueError as e:
        return jsonify({'error': 'Error de validación.', 'mensaje': str(e)}), 400
    except Exception as e:
        return jsonify({'error': 'Error inesperado.', 'mensaje': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5503)
