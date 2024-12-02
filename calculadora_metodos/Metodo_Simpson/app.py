import numpy as np
from flask import Flask, request, jsonify
from flask_cors import CORS
import sympy as sp

app = Flask(__name__)
CORS(app)

# Función segura para evaluar la función en un valor de x
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


# Función para validar que la función sea válida y tenga una sola variable 'x'
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


# Función para evaluar la función en un valor x
def evaluar_funcion(funcion_str, x):
    return evaluar_funcion_segura(funcion_str, x)


# Función para generar puntos y sus imágenes
def obtener_puntos_y_imagenes(a, b, n, funcion_str):
    h = (b - a) / n
    puntos = []  # Lista para los puntos x
    imagenes = []  # Lista para las imágenes f(x)

    for i in range(n + 1):  # Incluyendo los puntos a y b
        x_i = a + i * h
        puntos.append(x_i)
        f_x_i = evaluar_funcion(funcion_str, x_i)
        imagenes.append(f_x_i)

    return puntos, imagenes


# Función para generar puntos medios entre los puntos
def obtener_puntos_medios(puntos, n, funcion_str):
    puntos_medios = []  # Lista para los puntos medios
    imagenes_medios = []  # Lista para las imágenes de los puntos medios

    for i in range(n):
        x_medio = (puntos[i] + puntos[i + 1]) / 2
        puntos_medios.append(x_medio)
        f_x_medio = evaluar_funcion(funcion_str, x_medio)
        imagenes_medios.append(f_x_medio)

    return puntos_medios, imagenes_medios


# Método de Simpson
def simpson(a, b, n, funcion_str):
    try:
        # Verificar que n sea par
        if n % 2 != 0:
            raise ValueError("El valor de n debe ser par para el método de Simpson.")

        # Generar los puntos y calcular sus imágenes
        puntos, imagenes = obtener_puntos_y_imagenes(a, b, n, funcion_str)

        # Calcular puntos medios entre puntos consecutivos
        puntos_medios, imagenes_medios = obtener_puntos_medios(puntos, n, funcion_str)

        # Calcular la suma de los puntos impares y pares
        suma_impar = sum(imagenes[i] for i in range(1, n, 2))  # Impares
        suma_par = sum(imagenes[i] for i in range(2, n, 2))  # Pares

        # Evaluar la función en los puntos a y b
        f_a = evaluar_funcion(funcion_str, a)
        f_b = evaluar_funcion(funcion_str, b)

        # Calcular el área bajo la curva
        h = (b - a) / n
        area = (h / 3) * (f_a + 4 * suma_impar + 2 * suma_par + f_b)

        # Estimar el error relativo con el valor de n+2
        area_n2 = simpson_error(a, b, n + 2, funcion_str)
        error_relativo = abs(area - area_n2) / abs(area_n2)

        # Determinar convergencia/divergencia con un umbral más relajado
        convergencia = "Converge" if  area != 0 else "Diverge"

        # Resultados organizados
        resultados = {
            'area_bajo_la_curva': area,
            'error_relativo': error_relativo,
            'convergencia': convergencia,
            'puntos': puntos,
            'puntos_medios': puntos_medios,
            'imagenes_puntos_medios': imagenes_medios,
            'funcion_evaluada_en_puntos': list(zip(puntos, imagenes))
        }

        return resultados

    except Exception as e:
        raise ValueError(f"{str(e)}")


# Método para calcular el área con n+2 subintervalos, usado para el error
def simpson_error(a, b, n, funcion_str):
    try:
        h = (b - a) / n
        puntos, imagenes = obtener_puntos_y_imagenes(a, b, n, funcion_str)

        suma_impar = sum(imagenes[i] for i in range(1, n, 2))  # Impares
        suma_par = sum(imagenes[i] for i in range(2, n, 2))  # Pares

        f_a = evaluar_funcion(funcion_str, a)
        f_b = evaluar_funcion(funcion_str, b)

        area = (h / 3) * (f_a + 4 * suma_impar + 2 * suma_par + f_b)
        return area

    except Exception as e:
        raise ValueError(f"Error al calcular el área con n+2 subintervalos: {str(e)}")


# Endpoint para el método de Simpson
@app.route('/simpson', methods=['POST'])
def metodo_simpson():
    try:
        data = request.get_json()

        # Validación de parámetros faltantes
        if 'a' not in data:
            return jsonify({'error': "Error al ejecutar el método de Simpson.", 'mensaje': "Falta el valor de 'a'. Ingrese el límite inferior."}), 400

        if 'b' not in data:
            return jsonify({'error': "Error al ejecutar el método de Simpson.", 'mensaje': "Falta el valor de 'b'. Ingrese el límite superior."}), 400

        if 'n' not in data:
            return jsonify({'error': "Error al ejecutar el método de Simpson.", 'mensaje': "Falta el valor de 'n'. Ingrese el número de subintervalos."}), 400

        if 'funcion' not in data:
            return jsonify({'error': "Error al ejecutar el método de Simpson.", 'mensaje': "Falta el valor de 'funcion'. Ingrese la expresión de la función."}), 400

        # Obtener valores
        a = data['a']
        b = data['b']
        n = data['n']
        funcion_str = data['funcion']

        # Validar que la función sea válida
        try:
            validar_funcion(funcion_str)
        except ValueError as e:
            return jsonify({'error': "Error al ejecutar el método de Simpson.", 'mensaje': str(e)}), 400

        # Validar que a < b y n > 0
        if a >= b:
            return jsonify({'error': "Error al ejecutar el método de Simpson.", 'mensaje': "El límite inferior debe ser menor que el límite superior."}), 400

        if n <= 0:
            return jsonify({'error': "Error al ejecutar el método de Simpson.", 'mensaje': "El número de subintervalos debe ser mayor que cero."}), 400

        if n % 2 != 0:
            return jsonify({'error': "Error al ejecutar el método de Simpson.", 'mensaje': "El número de subintervalos 'n' debe ser par para el método de Simpson."}), 400

        # Ejecutar el método de Simpson
        try:
            resultados = simpson(a, b, n, funcion_str)
        except ValueError as e:
            return jsonify({'error': "Error al ejecutar el método de Simpson.", 'mensaje': str(e)}), 400

        # Devolver resultado
        return jsonify(resultados)

    except Exception as e:
        return jsonify({'error': "Error inesperado al ejecutar el método de Simpson.", 'mensaje': str(e)}), 400


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5504)
