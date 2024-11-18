from flask import Flask, request, jsonify
from flask_cors import CORS
import sympy as sp
import numpy as np
import re

app = Flask(__name__)
CORS(app)

def es_valido(entrada):
    """Verifica que la entrada contenga solo caracteres permitidos."""
    patron = r'^[a-zA-Z0-9+\-*/^(). ]+$'
    return re.match(patron, entrada) is not None

def es_expresion_valida(expresion_str):
    """Verifica que la expresión sea válida y tenga solo una variable."""
    try:
        expr = sp.sympify(expresion_str).subs(sp.Symbol('e'), sp.exp(1))
        variables = expr.free_symbols
        if len(variables) == 0:
            return False, "La función no contiene variables."
        if len(variables) > 1:
            return False, "La función debe contener exactamente una variable."
        for variable in variables:
            if len(str(variable)) > 2:  # Limitar el nombre de la variable a 2 caracteres
                return False, "Las variables deben tener un nombre de máximo 2 caracteres."
        return True, ""
    except (sp.SympifyError, TypeError, ValueError):
        return False, "La función no es matemáticamente correcta o no contiene variables."

def evaluar_funcion_segura(funcion, x):
    """Evalúa una función matemática de forma segura."""
    try:
        resultado = funcion(x)
        if not isinstance(resultado, (int, float)) or np.isnan(resultado) or np.isinf(resultado):
            raise ValueError("La función devolvió un valor no numérico o indefinido.")
        return resultado
    except Exception as e:
        raise ValueError(f"Error al evaluar la función en x = {x}: {str(e)}")

def biseccion(funcion, Xi, Xu, tolerancia=1e-6, max_iter=1000, umbral=1e10):
    """Implementación del método de bisección con validaciones avanzadas."""
    try:
        num_puntos = 10
        puntos = np.linspace(Xi, Xu, num_puntos)
        f_puntos = [evaluar_funcion_segura(funcion, p) for p in puntos]

        # Verificar si hay cambio de signo en el intervalo
        cambio_signo = any(f_puntos[i] * f_puntos[i + 1] < 0 for i in range(len(f_puntos) - 1))
        if not cambio_signo:
            return {
                'error': 'Error, no hay una raíz factible',
                'mensaje': 'No hay un cambio de signo en el intervalo, no hay una raíz factible.'
            }, 400

        iteraciones = []
        contador = 0

        while contador < max_iter:
            Xr = (Xi + Xu) / 2
            fXr = evaluar_funcion_segura(funcion, Xr)

            # Verificar si el valor es demasiado grande o infinito
            if abs(fXr) > umbral:
                return {
                    'error': 'La ecuación diverge. Los valores son demasiado grandes.',
                    'mensaje': 'Revise la función o proporcione un intervalo diferente.'
                }, 400

            # Calcular el error relativo
            error_relativo = abs((Xu - Xi) / 2)

            # Guardar datos de la iteración actual
            iteraciones.append({
                'iteracion': contador + 1,
                'punto_a': round(Xi, 4),
                'punto_b': round(Xu, 4),
                'punto_medio': round(Xr, 4),
                'f(Xr)': round(fXr, 8),
                'error': round(error_relativo, 8)
            })

            # Comprobar convergencia
            if abs(fXr) < tolerancia or error_relativo < tolerancia:
                return {
                    'resultado_final': round(Xr, 8),
                    'numero_iteraciones': len(iteraciones),
                    'iteraciones': iteraciones,
                    'mensaje': f"Convergió exitosamente en {len(iteraciones)} iteraciones."
                }, 200

            # Actualizar los extremos del intervalo
            if evaluar_funcion_segura(funcion, Xi) * fXr < 0:
                Xu = Xr
            else:
                Xi = Xr

            contador += 1

        return {
            'error': 'Se alcanzó el máximo número de iteraciones sin convergencia.',
            'mensaje': 'El proceso alcanzó el límite de iteraciones sin encontrar una raíz.'
        }, 400
    except Exception as e:
        return {
            'error': f"Error inesperado: {str(e)}",
            'mensaje': 'Ocurrió un error inesperado en el cálculo de la bisección.'
        }, 500

@app.route('/biseccion', methods=['POST'])
def calcular_biseccion():
    try:
        # Obtener datos de la solicitud
        data = request.get_json()

        if 'punto_inicial_a' not in data or 'punto_inicial_b' not in data or 'tolerancia' not in data or 'funcion' not in data:
            return jsonify({
                'error': 'Faltan parámetros requeridos.',
                'mensaje': 'Incluya punto_inicial_a, punto_inicial_b, tolerancia y funcion en la solicitud.'
            }), 400

        try:
            Xi = float(data['punto_inicial_a'])
            Xu = float(data['punto_inicial_b'])
            tolerancia = float(data['tolerancia'])
        except (ValueError, TypeError):
            return jsonify({
                'error': 'Los parámetros deben ser numéricos.',
                'mensaje': 'Asegúrese de que punto_inicial_a, punto_inicial_b y tolerancia sean números válidos.'
            }), 400

        funcion_str = data['funcion']

        # Validar que la función sea válida y tenga solo una variable
        es_valido, mensaje_error = es_expresion_valida(funcion_str)
        if not es_valido:
            return jsonify({
                'error': 'Función inválida.',
                'mensaje': mensaje_error
            }), 400

        # Procesar la función
        expr = sp.sympify(funcion_str).subs(sp.Symbol('e'), sp.exp(1))
        x = list(expr.free_symbols)[0]
        try:
            funcion = sp.lambdify(x, expr, 'numpy')
        except Exception as e:
            return jsonify({
                'error': f'Error al procesar la función: {str(e)}',
                'mensaje': 'Revise la sintaxis de la función proporcionada.'
            }), 400

        # Ejecutar el método de bisección
        resultado, status_code = biseccion(funcion, Xi, Xu, tolerancia)
        return jsonify(resultado), status_code

    except Exception as e:
        return jsonify({
            'error': f"Error inesperado: {str(e)}",
            'mensaje': 'Ocurrió un error inesperado en el servidor.'
        }), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
