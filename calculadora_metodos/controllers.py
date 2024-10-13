from scipy import optimize
import math
import sympy as sp

def home_controller():
    return {"message": "hello world"}

def suma_controller(a, b):
    return {"result": a + b}

def resta_controller(a, b):
    return {"result": a - b}


def calculo_raiz(x):
    b = math.sqrt(pow(x, 3))
    c = (pow(x, 2)) / 3.5
    return (-1) / (2 * (b + c - 4))

def calculo_error(a, b):
    return abs((a - b) / a)


def calculo_funcion(function_str, initial_guess, tolerance):
    X0 = initial_guess
    error = 1.0
    steps = []
    iteraciones=0


    # Definir la variable simbólica 'x'
    x = sp.symbols('x')

    # Convertir el string de la función en una expresión simbólica
    function_expr = sp.sympify(function_str)


    while error > tolerance:
        # Evalúa la función con el punto actual
       
        X0_nuevo = float(function_expr.subs(x,X0))

        if X0_nuevo != 0.0:
            error = calculo_error(X0_nuevo, X0)

        iteraciones += 1
        

        steps.append({
            'Iteración': f'Iteración {iteraciones}',
            'X0': X0,
            'X0_nuevo': X0_nuevo,
            'error': error
        })

        X0 = X0_nuevo
        

    return X0, steps, iteraciones