from scipy import optimize
import math
import sympy as sp


def home_controller():
    return {"message": "hello world"}

def suma_controller(a, b):
    return {"result": a + b}

def resta_controller(a, b):
    return {"result": a - b}


def newton_raphson_controller(func_str, func_prime_str, x0, E, max_iterations):
    # Definir la variable simbólica
    x = sp.symbols('x')

    # Convertir las cadenas de funciones en funciones simbólicas
    f_sympy = sp.sympify(func_str)
    f_prime_sympy = sp.sympify(func_prime_str)
    f_double_prime_sympy = sp.diff(f_prime_sympy, x)  # Calcular la segunda derivada de f(x)
    
    # Convertir la función simbólica y sus derivadas en funciones evaluables
    f = sp.lambdify(x, f_sympy)
    f_prime = sp.lambdify(x, f_prime_sympy)
    f_double_prime = sp.lambdify(x, f_double_prime_sympy)

    # Definir g(x)
    g_sympy = x - (f_sympy / f_prime_sympy)
    g = sp.lambdify(x, g_sympy)

    # Definir g'(x) = (f(x) * f''(x)) / (f'(x))^2
    def g_prime(x_val):
        f_x = f(x_val)
        f_prime_x = f_prime(x_val)
        f_double_prime_x = f_double_prime(x_val)
        return (f_x * f_double_prime_x) / (f_prime_x ** 2)

    # Implementación de Newton-Raphson
    x_n = float(x0)
    iteration_data = []  # Para almacenar los datos de las iteraciones
    iteration = 0
    
    while iteration < max_iterations:
        x_n1 = g(x_n)

        # Calcular el error
        diferencia = abs(x_n1 - x_n)
        error = abs(diferencia / x_n1)

        # Obtener el valor de g'(x) en x_n
        g_prime_val = g_prime(x_n)

        # Almacenar los resultados de la iteración
        iteration_data.append({
            'Iteración': iteration + 1,
            'x_n': float(x_n),
            "g'(x)": float(g_prime_val),  # Mostrar g'(x)
            '|x_n1 - x_n|': float(diferencia), 
            '|Error|': float(error)
        })

        # Actualizar para la siguiente iteración
        x_n = x_n1

        # Verificar condiciones de parada
        if error <= E and abs(f(x_n)) <= E:
            break
        
        iteration += 1

    return float(x_n), iteration_data