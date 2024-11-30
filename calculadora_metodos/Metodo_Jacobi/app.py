from flask import Flask, request, jsonify
from flask_cors import CORS  # Importa CORS
import sympy as sp
import numpy as np
import re  # Para validar las variables

app = Flask(__name__)
CORS(app)  # Habilita CORS para toda la aplicación


def validar_variables(variables):
    """Valida que las variables sigan el formato permitido: x, x1, x2, ..., xn."""
    for var in variables:
        if not re.match(r'^x\d*$', str(var)):
            raise ValueError(f"Se ha utilizado una variable no permitida: {var}. Solo se permiten variables del tipo x, x1, x2,... xn.")


def es_diagonal_dominante(A):
    """Verifica si la matriz A es diagonalmente dominante."""
    for i in range(len(A)):
        suma = sum(abs(A[i, j]) for j in range(len(A)) if j != i)
        if abs(A[i, i]) <= suma:
            return False
    return True


def parse_ecuaciones(ecuaciones):
    """Convierte un sistema de ecuaciones en la forma Ax = b."""
    try:
        exprs = []
        for ecuacion in ecuaciones:
            if "=" not in ecuacion:
                raise ValueError("Cada ecuación debe contener el símbolo '='.")
            lhs, rhs = ecuacion.split("=")
            expr = sp.sympify(lhs) - sp.sympify(rhs)
            exprs.append(expr)

        # Extraer variables
        variables = sorted(list(set().union(*[expr.free_symbols for expr in exprs])), key=lambda x: str(x))

        # Validar formato de las variables
        validar_variables(variables)

        # Inicializar matrices A y b
        n = len(variables)
        A = np.zeros((n, n))
        b = np.zeros(n)

        # Llenar matrices
        for i, expr in enumerate(exprs):
            for j, var in enumerate(variables):
                coef = expr.coeff(var)
                A[i, j] = float(coef)
            # Obtener término independiente
            term_indep = expr.as_coeff_add()[0]
            b[i] = -float(term_indep)

        return A, b, variables

    except ValueError as e:
        # Error específico de validación
        raise ValueError(f"Error al procesar las ecuaciones: {str(e)}")
    except Exception as e:
        # Error general
        raise ValueError("Error inesperado al procesar las ecuaciones.")



def jacobi_method(A, b, variables, tolerancia, max_iter):
    """Implementa el método de Jacobi."""
    n = len(b)

    # Verificar si la matriz es diagonalmente dominante
    if not es_diagonal_dominante(A):
        return {'error': "Validación fallida.", 'mensaje': "La matriz no es diagonalmente dominante. El método de Jacobi puede no converger."}

    # Verificar ceros en la diagonal principal
    if any(A[i, i] == 0 for i in range(n)):
        return {'error': "Validación fallida.", 'mensaje': "La matriz tiene ceros en la diagonal principal. Esto impide la resolución del sistema."}

    X0 = np.zeros(n)
    X = np.zeros(n)
    K = 0
    norma = 1
    iteraciones = []

    while norma > tolerancia and K < max_iter:
        K += 1
        for i in range(n):
            suma = sum(A[i, j] * X0[j] for j in range(n) if j != i)
            if A[i, i] != 0:
                X[i] = (b[i] - suma) / A[i, i]
            else:
                return {'error': "Validación fallida.", 'mensaje': f"División por cero en la posición {i}, {i}."}

        norma = np.max(np.abs(X0 - X))
        iteraciones.append({
            'iteracion': K,
            'valores': X.tolist(),
            'norma': norma
        })

        if norma > 10**10:
            return {'error': "Divergencia detectada.", 'mensaje': "Los valores están creciendo excesivamente."}

        X0 = X.copy()

    if K == max_iter:
        return {
            'converged': False,
            'resultado_final': None,
            'numero_iteraciones': max_iter,
            'iteraciones': iteraciones,
            'mensaje': "No se alcanzó la convergencia dentro del número máximo de iteraciones."
        }
    else:
        return {
            'converged': True,
            'resultado_final': X.tolist(),
            'numero_iteraciones': K,
            'iteraciones': iteraciones,
            'mensaje': f"Convergió exitosamente en {len(iteraciones)} iteraciones."
        }


@app.route('/jacobi', methods=['POST'])
def jacobi():
    try:
        data = request.get_json()
        ecuaciones_str = data.get('ecuaciones')
        tolerancia = data.get('tolerancia', 1e-4)
        max_iteraciones = data.get('max_iteraciones', 100)

        # Validar que las ecuaciones se proporcionaron
        if not ecuaciones_str:
            return jsonify({
                'error': 'Validación fallida.',
                'mensaje': 'No se proporcionaron ecuaciones.'
            }), 400

        # Procesar ecuaciones
        try:
            ecuaciones = ecuaciones_str.split(",")
            A, b, variables = parse_ecuaciones(ecuaciones)
        except ValueError as e:
            return jsonify({
                'error': 'Error al procesar las ecuaciones.',
                'mensaje': str(e)
            }), 400

        # Ejecutar el método de Jacobi
        resultado = jacobi_method(A, b, variables, tolerancia, max_iteraciones)

        if 'error' in resultado:
            return jsonify({
                'error': 'Validación fallida.',
                'mensaje': resultado['mensaje']
            }), 400

        return jsonify(resultado)

    except Exception as e:
        return jsonify({
            'error': 'Error del servidor.',
            'mensaje': str(e)
        }), 500



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5501)
