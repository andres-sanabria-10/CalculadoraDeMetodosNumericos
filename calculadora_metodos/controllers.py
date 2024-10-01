from scipy import optimize
import numpy as np
import math

def home_controller():
    return {"message": "hello world"}

def suma_controller(a, b):
    return {"result": a + b}

def resta_controller(a, b):
    return {"result": a - b}

def biseccion_controller(func_str, a, b, tolerancia=1e-6, max_iteraciones=100):
    def f(x):
        return eval(func_str)
    
    try:
        resultado = optimize.root_scalar(f, method='bisect', bracket=[a, b], 
                                         rtol=tolerancia, maxiter=max_iteraciones)
        return {
            "root": resultado.root,
            "iterations": resultado.iterations,
            "converged": resultado.converged,
            "function_calls": resultado.function_calls
        }
    except ValueError as e:
        return {"error": str(e)}
    
# Modificar evaluar_funcion para permitir funciones específicas como sqrt
def evaluar_funcion(func_str, x):
    # Definición de funciones básicas y diccionario seguro para eval
    def sin(x):
        resultado = 0
        for n in range(10):
            resultado += (-1) ** n * x ** (2 * n + 1) / factorial(2 * n + 1)
        return resultado

    def cos(x):
        resultado = 0
        for n in range(10):
            resultado += (-1) ** n * x ** (2 * n) / factorial(2 * n)
        return resultado

    def exp(x):
        resultado = 0
        for n in range(10):
            resultado += x ** n / factorial(n)
        return resultado

    def factorial(n):
        if n == 0 or n == 1:
            return 1
        return n * factorial(n - 1)

    # Diccionario seguro con funciones permitidas
    safe_dict = {
        'sin': sin,
        'cos': cos,
        'exp': exp,
        'sqrt': math.sqrt,
        'x': x,
        'factorial': factorial
    }

    # Ahora puedes usar eval de forma más segura
    try:
        # Evaluar la función de forma segura
        return eval(func_str, {"__builtins__": None}, safe_dict)
    except ZeroDivisionError:
        print("Error: División por cero")
        return float('nan')
    except Exception as e:
        print(f"Error evaluando la función: {e}")
        return float('nan')


def calcular_puntos_punto_fijo(f, g_list, x0, tolerancia):
    puntos = []
    for i, g in enumerate(g_list):
        x = x0
        for iteracion in range(1, 21):
            x_nuevo = evaluar_funcion(g, x)

            # Si x_nuevo es None o complejo, saltar esta iteración
            if x_nuevo is None or isinstance(x_nuevo, complex):
                print(f"Iteración {iteracion}: Resultado inválido ({x_nuevo}). Pasando a la siguiente función.")
                break

            # Cálculo del error relativo
            error_relativo = abs((x_nuevo - x) / x_nuevo) if x_nuevo != 0 else abs(x_nuevo - x)
            puntos.append({
                'iteracion': iteracion,
                'x_nuevo': x_nuevo,
                'error_relativo': error_relativo
            })

            if error_relativo < tolerancia:
                return puntos, x_nuevo, iteracion, True

            x = x_nuevo

    return puntos, x, iteracion, False