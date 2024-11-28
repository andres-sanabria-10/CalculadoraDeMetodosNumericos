import numpy as np
import sympy as sp
from flask import Flask, request, jsonify

app = Flask(__name__)

# Función para verificar si la matriz es diagonal dominante
def es_diagonal_dominante(A):
    n = len(A)
    for i in range(n):
        suma = sum(abs(A[i][j]) for j in range(n) if j != i)
        if abs(A[i][i]) <= suma:
            return False
    return True

# Método de Gauss-Seidel
def gauss_seidel_method(A, b, tolerancia, max_iter):
    n = len(b)
    x = np.zeros(n, dtype=float)
    historial_iteraciones = []

    for iteracion in range(max_iter):
        x_nuevo = np.copy(x)

        for i in range(n):
            suma = np.dot(A[i], x_nuevo) - A[i][i] * x_nuevo[i]
            x_nuevo[i] = (b[i] - suma) / A[i][i]

        error = max(abs(x_nuevo - x)) / max(abs(x_nuevo))

        historial_iteraciones.append({
            'iteracion': iteracion + 1,
            'solucion': x_nuevo.tolist(),
            'error': error
        })

        if error < tolerancia:
            return {
                'converged': True,
                'resultado_final': x_nuevo.tolist(),
                'numero_iteraciones': iteracion + 1,
                'iteraciones': historial_iteraciones,
                'mensaje': f"Convergió después de {iteracion + 1} iteraciones."
            }

        x = x_nuevo

    return {
        'converged': False,
        'resultado_final': None,
        'numero_iteraciones': max_iter,
        'iteraciones': historial_iteraciones,
        'mensaje': "No se alcanzó la convergencia dentro del número máximo de iteraciones."
    }

# Función para procesar las ecuaciones
def parse_ecuaciones(ecuaciones):
    exprs = []
    for ecuacion in ecuaciones:
        if '=' not in ecuacion:
            raise ValueError(f"Formato incorrecto: falta el '=' en la ecuación '{ecuacion}'.")
        
        lhs, rhs = ecuacion.split("=")
        expr = sp.sympify(lhs) - sp.sympify(rhs)
        exprs.append(expr)

    variables = sorted(list(set().union(*[expr.free_symbols for expr in exprs])), key=lambda x: str(x))
    n = len(variables)

    if len(exprs) != n:
        raise ValueError(f"El sistema debe tener {n} ecuaciones para ser cuadrado, pero se encontraron {len(exprs)}.")

    A = np.zeros((n, n))
    b = np.zeros(n)

    for i, expr in enumerate(exprs):
        for j, var in enumerate(variables):
            coef = expr.coeff(var)
            A[i, j] = float(coef)
        b[i] = -float(expr.as_coeff_add()[0])

    return A, b, variables

@app.route('/gauss-seidel', methods=['POST'])
def gauss_seidel():
    try:
        data = request.get_json()

        # Validación de parámetros faltantes
        if 'ecuaciones' not in data or not data['ecuaciones']:
            return jsonify({'error': "Falta el valor de 'ecuaciones'. Ingrese las ecuaciones del sistema."}), 400

        if 'tolerancia' not in data:
            return jsonify({'error': "Falta el valor de 'tolerancia'. Ingrese una tolerancia válida."}), 400

        if 'max_iteraciones' not in data:
            return jsonify({'error': "Falta el valor de 'max_iteraciones'. Ingrese un número válido de iteraciones."}), 400

        # Obtener valores
        ecuaciones_str = data['ecuaciones']
        tolerancia = data['tolerancia']
        max_iteraciones = data['max_iteraciones']

        # Procesar ecuaciones
        A, b, variables = parse_ecuaciones(ecuaciones_str)

        # Validar diagonal dominante
        if not es_diagonal_dominante(A):
            return jsonify({'error': "La matriz no es diagonal dominante. Ordene el sistema adecuadamente."}), 400

        # Ejecutar método de Gauss-Seidel
        resultado = gauss_seidel_method(A, b, tolerancia, max_iteraciones)
        return jsonify(resultado)

    except ValueError as ve:
        return jsonify({'error': str(ve)}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5502)
