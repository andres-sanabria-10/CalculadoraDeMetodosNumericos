from scipy import optimize
import math
import sympy as sp

def home_controller():
    return {"message": "hello world"}

def suma_controller(a, b):
    return {"result": a + b}

def resta_controller(a, b):
    return {"result": a - b}


# Función para evaluar la función
def evaluar_funcion(funcion_str, x):
    # Evalúa la función a partir de un string
    return eval(funcion_str)

# Función para evaluar la función
def evaluar_funcion(funcion_str, x):
    # Evalúa la función a partir de un string
    return eval(funcion_str)

# Método de bisección
def bisection_method(funcion, punto_a, punto_b, tolerancia, max_iteraciones):
    iteraciones = []
    function_calls = 0
    converged = False
    punto_medio_anterior = (punto_a + punto_b) / 2  # Inicializa el punto medio anterior

    for iteracion in range(1, max_iteraciones + 1):
        # Calcula el punto medio
        punto_medio = (punto_a + punto_b) / 2
        valor_funcion_medio = evaluar_funcion(funcion, punto_medio)
        function_calls += 1

        # Cálculo del error relativo
        if iteracion > 1:  # Evitar error en la primera iteración
            error = abs((punto_medio - punto_medio_anterior) / punto_medio) * 100
        else:
            error = float('inf')  # No hay error en la primera iteración

        # Guarda los datos de la iteración
        iteraciones.append({
            'iteracion': iteracion,
            'punto_a': punto_a,
            'punto_b': punto_b,
            'punto_medio': punto_medio,
            'error': error
        })

        # Verifica si el valor de la función en el punto medio es suficientemente pequeño
        if abs(valor_funcion_medio) < tolerancia:
            converged = True
            break

        # Actualiza los puntos según el signo de la función
        valor_funcion_a = evaluar_funcion(funcion, punto_a)
        if valor_funcion_a * valor_funcion_medio < 0:  # Hay una raíz en [punto_a, punto_medio]
            punto_b = punto_medio
        else:  # Hay una raíz en [punto_medio, punto_b]
            punto_a = punto_medio

        # Actualiza el punto medio anterior para la siguiente iteración
        punto_medio_anterior = punto_medio

    return {
        'converged': converged,
        'function_calls': function_calls,
        'iteraciones': iteraciones,
        'resultado_final': punto_medio if converged else None,
        'numero_iteraciones': len(iteraciones)
    }