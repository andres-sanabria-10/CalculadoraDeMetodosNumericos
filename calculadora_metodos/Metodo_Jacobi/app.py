from flask import Flask, request, jsonify
from flask_cors import CORS  # Importa CORS
import sympy as sp
import numpy as np

app = Flask(__name__)
CORS(app)  # Habilita CORS para toda la aplicaciónn


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
    app.run(host='0.0.0.0', port=5800)