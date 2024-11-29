from flask import Flask, request, jsonify
from flask_cors import CORS  # Importa CORS
import sympy as sp
import numpy as np
import re

app = Flask(__name__)
CORS(app)  # Habilita CORS para toda la aplicación

def validar_variables(variables):
    for var in variables:
        if not re.match(r'^x\d*$', var):
            raise ValueError(f"Se ha utilizado una variable no permitida: {var}. Solo se permiten variables del tipo x, x1, x2,... xn.")

def evaluar_funcion_segura(funcion_str, variables):
    try:
        funciones_trigonometricas = {
            'sin': sp.sin, 'cos': sp.cos, 'tan': sp.tan,
            'exp': sp.exp, 'log': sp.log
        }
        # Solo extraemos las variables alfanuméricas, no funciones trigonométricas
        variables_simbolicas = sp.symbols(list(variables.keys()))
        expr = sp.sympify(funcion_str, locals=funciones_trigonometricas)
        result = expr.subs(variables_simbolicas, list(variables.values()))

        # Verificar si el resultado es complejo
        if isinstance(result, sp.core.numbers.Complex):
            raise ValueError("El resultado es un número complejo.")

        # Verificar si el resultado tiende a infinito
        if result.is_infinite:
            raise ValueError("El resultado es infinito.")
        
        return float(result)
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

        # Validación de la estructura del JSON recibido
        if not data:
            return jsonify({'error': "Validación fallida.", 'mensaje': "El cuerpo de la solicitud está vacío."}), 400
        if 'ecuaciones' not in data or 'valores_iniciales' not in data:
            return jsonify({'error': "Validación fallida.", 'mensaje': "Faltan parámetros requeridos: 'ecuaciones' o 'valores_iniciales'."}), 400

        ecuaciones_str = data['ecuaciones']
        valores_iniciales = data['valores_iniciales']
        tolerancia = data.get('tolerancia', 1e-6)
        max_iteraciones = data.get('max_iteraciones', 100)

        # Validar que las ecuaciones no estén vacías
        if not ecuaciones_str.strip():
            return jsonify({'error': "Validación fallida.", 'mensaje': "Las ecuaciones no pueden estar vacías."}), 400

        # Procesar ecuaciones
        ecuaciones = ecuaciones_str.split(",")
        # Extraer solo las variables alfanuméricas
        variables = sorted(list(set(re.findall(r'\b[a-zA-Z_]\w*\b', ecuaciones_str))))  # Solo variables alfanuméricas

        # Filtrar las variables para eliminar funciones trigonométricas
        funciones_trigonometricas = {'sin', 'cos', 'tan', 'exp', 'log'}
        variables = [var for var in variables if var not in funciones_trigonometricas]

        try:
            validar_variables(variables)
        except ValueError as e:
            return jsonify({'error': "Validación fallida.", 'mensaje': str(e)}), 400
        
        if len(variables) != len(valores_iniciales):
            return jsonify({'error': "Validación fallida.", 'mensaje': f"Número de variables ({len(variables)}) no coincide con los valores iniciales ({len(valores_iniciales)})."}), 400


        # Validar que los valores iniciales sean numéricos
        try:
            valores_iniciales = [float(v) for v in valores_iniciales]
        except ValueError:
            return jsonify({'error': "Validación fallida.", 'mensaje': "Los valores iniciales deben ser numéricos."}), 400

        # Crear funciones numéricas
        try:
            funciones_numericas = []
            for ecuacion in ecuaciones:
                ecuacion_simbolica = sp.sympify(ecuacion.strip(), locals={'sin': sp.sin, 'cos': sp.cos, 'tan': sp.tan, 'exp': sp.exp, 'log': sp.log})
                funcion_numerica = sp.lambdify(sp.symbols(variables), ecuacion_simbolica, "numpy")
                funciones_numericas.append(funcion_numerica)
        except Exception as e:
            return jsonify({'error': "Validación fallida.", 'mensaje': f"Error al procesar las ecuaciones: {str(e)}"}), 400

        # Validar que el Jacobiano sea invertible
        try:
            V_actual = np.array(valores_iniciales, dtype=float)
            jacobiano_inicial = calcular_jacobiano(funciones_numericas, V_actual)
            A_inversa = np.linalg.inv(jacobiano_inicial)
        except np.linalg.LinAlgError:
            return jsonify({'error': "Validación fallida.", 'mensaje': "El Jacobiano es singular, lo que indica que el sistema no tiene una solución única."}), 400

        # Implementar el método de Broyden
        iteraciones = []
        for iteracion in range(max_iteraciones):
            try:
                valor_funcion = np.array([f(*V_actual) for f in funciones_numericas])
                
                # Verificar si el resultado de la función es complejo o infinito
                if np.any(np.isnan(valor_funcion)) or np.any(np.isinf(valor_funcion)):
                    return jsonify({'error': "Validación fallida.", 'mensaje': "El valor de la función tiende a infinito o es inválido."}), 400

                if np.linalg.norm(valor_funcion) < tolerancia:
                    return jsonify({
                        'converged': True,
                        'resultado_final': V_actual.tolist(),
                        'numero_iteraciones': iteracion + 1,
                        'iteraciones': iteraciones,
                        'mensaje': f"Convergió exitosamente en {len(iteraciones)} iteraciones."
                    })

                # Actualizar V
                delta_V = -np.dot(A_inversa, valor_funcion)
                nuevo_V = V_actual + delta_V
                nuevo_valor_funcion = np.array([f(*nuevo_V) for f in funciones_numericas])

                # Verificar si el nuevo valor de la función es complejo o infinito
                if np.any(np.isnan(nuevo_valor_funcion)) or np.any(np.isinf(nuevo_valor_funcion)):
                    return jsonify({'error': "Validación fallida.", 'mensaje': "El nuevo valor de la función tiende a infinito o es inválido."}), 400

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
            except Exception as e:
                return jsonify({'error': "Error en la iteración.", 'mensaje': f"{str(e)}"}), 400

        return jsonify({
            'converged': False,
            'resultado_final': None,
            'numero_iteraciones': max_iteraciones,
            'iteraciones': iteraciones,
            'mensaje': "No se alcanzó la convergencia dentro del número máximo de iteraciones."
        })

    except Exception as e:
        return jsonify({'error': "Error interno del servidor.", 'mensaje': str(e)}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5100)
