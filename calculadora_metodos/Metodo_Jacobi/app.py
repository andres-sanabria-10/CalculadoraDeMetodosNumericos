from flask import Flask, request, jsonify
from flask_cors import CORS  # Importa CORS
import sympy as sp
import numpy as np

app = Flask(__name__)
CORS(app)  # Habilita CORS para toda la aplicaciónn

def es_diagonal_dominante(A):
    for i in range(len(A)):
        suma = sum(abs(A[i, j]) for j in range(len(A)) if j != i)
        if abs(A[i, i]) <= suma:
            return False
    return True

def parse_ecuaciones(ecuaciones):
    exprs = []
    for ecuacion in ecuaciones:
        lhs, rhs = ecuacion.split("=")
        expr = sp.sympify(lhs) - sp.sympify(rhs)
        exprs.append(expr)
    
    variables = sorted(list(set().union(*[expr.free_symbols for expr in exprs])), key=lambda x: str(x))
    n = len(variables)
    
    A = np.zeros((n, n))
    b = np.zeros(n)
    
    for i, expr in enumerate(exprs):
        for j, var in enumerate(variables):
            coef = expr.coeff(var)
            A[i, j] = float(coef)
        b[i] = -float(expr.as_coeff_add()[0])
    
    return A, b, variables

def jacobi_method(A, b, variables, tolerancia, max_iter):
    n = len(b)
    if not es_diagonal_dominante(A):
        return {'error': "La matriz no es diagonalmente dominante. El método de Jacobi puede no converger."}

    if any(A[i, i] == 0 for i in range(n)):
        return {'error': "La matriz tiene ceros en la diagonal. Esto impide la resolución del sistema con el método de Jacobi."}

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
                return {'error': f"División por cero en la posición {i}, {i}."}

        norma = np.max(np.abs(X0 - X))
        iteraciones.append({
            'iteracion': K,
            'valores': X.tolist(),
            'norma': norma
        })

        if norma > 10**10:
            return {'error': "Divergencia detectada. Los valores están creciendo excesivamente."}

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
            'iteraciones': iteraciones
        }

import numpy as np

app = Flask(__name__)

def metodo_jacobi(A, b, x0, tolerancia=1e-6, max_iteraciones=100):
    n = len(b)
    x = np.copy(x0)
    iteraciones = []

    for iter in range(max_iteraciones):
        x_new = np.copy(x)

        for i in range(n):
            suma = np.dot(A[i], x) - A[i][i] * x[i]
            x_new[i] = (b[i] - suma) / A[i][i]

        error = np.linalg.norm(x_new - x, np.inf)

        iteraciones.append({
            'iteracion': iter + 1,
            'x': x_new.tolist(),
            'error': error
        })

        if error < tolerancia:
            return x_new.tolist(), iteraciones

        x = x_new

    return None, iteraciones

@app.route('/jacobi', methods=['POST'])
def jacobi():
    try:
        data = request.get_json()

        ecuaciones_str = data.get('ecuaciones')
        tolerancia = data.get('tolerancia', 1e-4)
        max_iteraciones = data.get('max_iteraciones', 100)

        # Validar y procesar ecuaciones
        if not ecuaciones_str:
            return jsonify({'error': "No se proporcionaron ecuaciones."}), 400

        ecuaciones = ecuaciones_str.split(",")
        A, b, variables = parse_ecuaciones(ecuaciones)

        # Ejecutar el método de Jacobi
        resultado = jacobi_method(A, b, variables, tolerancia, max_iteraciones)
        
        if 'error' in resultado:
            return jsonify(resultado), 400

        return jsonify(resultado)

        A = np.array(data['A'])
        b = np.array(data['b'])
        x0 = np.array(data['x0'], dtype=float)
        tolerancia = data.get('tolerancia', 1e-6)
        max_iteraciones = data.get('max_iteraciones', 100)

        resultado_final, iteraciones = metodo_jacobi(A, b, x0, tolerancia, max_iteraciones)

        if resultado_final is None:
            return jsonify({
                'converged': False,
                'resultado_final': None,
                'numero_iteraciones': max_iteraciones,
                'iteraciones': iteraciones
            })

        return jsonify({
            'converged': True,
            'resultado_final': resultado_final,
            'numero_iteraciones': len(iteraciones),
            'iteraciones': iteraciones
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':

    app.run(host='0.0.0.0', port=5501)

  
