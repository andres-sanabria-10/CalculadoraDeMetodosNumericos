from flask import Flask, request, jsonify
from flask_cors import CORS  # Importa CORS
import sympy as sp
import numpy as np
import re

app = Flask(__name__)
CORS(app)  # Habilita CORS para toda la aplicación

def evaluar_funcion_segura(funcion_str, variables):
    try:
        funciones_trigonometricas = {
            'sin': sp.sin, 'cos': sp.cos, 'tan': sp.tan,
            'exp': sp.exp, 'log': sp.log
        }
        variables_simbolicas = sp.symbols(list(variables.keys()))
        expr = sp.sympify(funcion_str, locals=funciones_trigonometricas)
        return float(expr.subs(variables_simbolicas, list(variables.values())))
    except Exception as e:
        raise ValueError(f"Error al evaluar la función: {str(e)}")

def calcular_jacobiano(funciones, V, h=1e-8):
    numero_variables = len(V)
    jacobiano = np.zeros((len(funciones), numero_variables))
    funcion_evaluada = np.array([f(*V) for f in funciones])
    for i in range(numero_variables):
        V_modificado = np.copy(V)
        V_modificado[i] += h
        funcion_modificada = np.array([f(*V_modificado) for f in funciones])
        jacobiano[:, i] = (funcion_modificada - funcion_evaluada) / h
    return jacobiano

@app.route('/broyden', methods=['POST'])
def broyden():
    try:
        data = request.get_json()
        ecuaciones_str = data['ecuaciones']
        valores_iniciales = data['valores_iniciales']
        tolerancia = data.get('tolerancia', 1e-6)
        max_iteraciones = data.get('max_iteraciones', 100)

        # Procesar ecuaciones
        ecuaciones = ecuaciones_str.split(",")
        variables = sorted(list(set(re.findall(r'[a-zA-Z]\w*', ecuaciones_str))))
        if len(variables) != len(valores_iniciales):
            return jsonify({'error': f"Número de variables ({len(variables)}) no coincide con los valores iniciales ({len(valores_iniciales)})."}), 400

        # Crear funciones numéricas
        funciones_numericas = []
        for ecuacion in ecuaciones:
            ecuacion_simbolica = sp.sympify(ecuacion.strip())
            funcion_numerica = sp.lambdify(sp.symbols(variables), ecuacion_simbolica, "numpy")
            funciones_numericas.append(funcion_numerica)

        valores_iniciales = [float(v) for v in valores_iniciales]

        # Implementar el método de Broyden
        V_actual = np.array(valores_iniciales, dtype=float)
        jacobiano_inicial = calcular_jacobiano(funciones_numericas, V_actual)
        A_inversa = np.linalg.inv(jacobiano_inicial)

        iteraciones = []
        for iteracion in range(max_iteraciones):
            valor_funcion = np.array([f(*V_actual) for f in funciones_numericas])
            if np.linalg.norm(valor_funcion) < tolerancia:
                return jsonify({
                    'converged': True,
                    'resultado_final': V_actual.tolist(),
                    'numero_iteraciones': iteracion + 1,
                    'iteraciones': iteraciones
                })

            # Actualizar V
            delta_V = -np.dot(A_inversa, valor_funcion)
            nuevo_V = V_actual + delta_V
            nuevo_valor_funcion = np.array([f(*nuevo_V) for f in funciones_numericas])

            diferencia_V = nuevo_V - V_actual
            diferencia_funcion = nuevo_valor_funcion - valor_funcion

            # Actualizar la inversa del Jacobiano
            A_inversa += np.outer(diferencia_V - np.dot(A_inversa, diferencia_funcion), 
                                  np.dot(A_inversa, diferencia_funcion)) / np.dot(np.dot(A_inversa, diferencia_funcion), diferencia_funcion)

            iteraciones.append({
                'iteracion': iteracion + 1,
                'V': V_actual.tolist(),
                'error': np.linalg.norm(valor_funcion)
            })

            V_actual = nuevo_V

        return jsonify({
            'converged': False,
            'resultado_final': None,
            'numero_iteraciones': max_iteraciones,
            'iteraciones': iteraciones
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5100)
