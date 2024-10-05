from scipy import optimize
import math
import sympy as sp


def home_controller():
    return {"message": "hello world"}

def suma_controller(a, b):
    return {"result": a + b}

def resta_controller(a, b):
    return {"result": a - b}

# Implementar el método de Newton-Raphson con función y derivada proporcionadas por el usuario
def newton_raphson_controller(func_str, func_prime_str, x0, E, max_iterations=100):
    # Definir la variable simbólica
    x = sp.symbols('x')

    # Convertir las cadenas de funciones en funciones simbólicas
    f_sympy = sp.sympify(func_str)
    f_prime_sympy = sp.sympify(func_prime_str)
    
    # Convertir la función simbólica y su derivada en funciones evaluables
    f = sp.lambdify(x, f_sympy)
    f_prime = sp.lambdify(x, f_prime_sympy)

    # Definir la función g(x)
    def g(x_val):
        return float(x_val - f(x_val) / f_prime(x_val))

    # Implementación de Newton-Raphson
    x_n = float(x0)
    iteration_data = []  # Para almacenar los datos de las iteraciones
    iteration = 0
    
    while iteration < max_iterations:
        # Calcular el nuevo valor de x
        x_n1 = g(x_n)

        # Calcular el error absoluto
        error = abs(x_n1 - x_n)

        # Almacenar los resultados de la iteración
        iteration_data.append({
            'Iteration': iteration,
            'x_n': float(x_n),
            '|x_n1 - x_n|': float(error)
        })

        # Actualizar x_n para la próxima iteración
        x_n = x_n1

        # Verificar condiciones de parada
        if error <= E and abs(f(x_n)) <= E:
            break
        
        iteration += 1

    return float(x_n), iteration_data