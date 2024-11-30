import numpy as np
from flask import Flask, request, jsonify
import sympy as sp

app = Flask(__name__)

# Función para evaluar la función en un valor x
def evaluar_funcion(funcion_str, x):
    # Usar sympy para manejar la expresión simbólica
    funcion = sp.sympify(funcion_str)
    return float(funcion.evalf(subs={sp.symbols('x'): x}))

# Función para generar puntos y sus imágenes
def obtener_puntos_y_imagenes(a, b, n, funcion_str):
    h = (b - a) / n
    puntos = []  # Lista para los puntos x
    imagenes = []  # Lista para las imágenes f(x)

    for i in range(n+1):  # Incluyendo los puntos a y b
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
        x_medio = (puntos[i] + puntos[i+1]) / 2
        puntos_medios.append(x_medio)
        f_x_medio = evaluar_funcion(funcion_str, x_medio)
        imagenes_medios.append(f_x_medio)

    return puntos_medios, imagenes_medios

# Método de Simpson
def simpson(a, b, n, funcion_str):
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
    
    # Determinar convergencia/ divergencia con un umbral más relajado
    convergencia = "Converge" if error_relativo < 1e-4 else "Diverge"
    
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

# Método para calcular el área con n+2 subintervalos, usado para el error
def simpson_error(a, b, n, funcion_str):
    h = (b - a) / n
    puntos, imagenes = obtener_puntos_y_imagenes(a, b, n, funcion_str)
    
    suma_impar = sum(imagenes[i] for i in range(1, n, 2))  # Impares
    suma_par = sum(imagenes[i] for i in range(2, n, 2))  # Pares
    
    f_a = evaluar_funcion(funcion_str, a)
    f_b = evaluar_funcion(funcion_str, b)
    
    area = (h / 3) * (f_a + 4 * suma_impar + 2 * suma_par + f_b)
    return area

@app.route('/simpson', methods=['POST'])
def metodo_simpson():
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

        # Ejecutar el método de Simpson
        resultados = simpson(a, b, n, funcion_str)

        # Devolver resultado
        return jsonify(resultados)

    except Exception as e:
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5504)
