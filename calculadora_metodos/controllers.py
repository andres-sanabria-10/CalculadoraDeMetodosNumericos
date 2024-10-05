from scipy import optimize
import numpy as np
import math
from sympy import symbols, lambdify

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

    while error > tolerance:
        # Evalúa la función con el punto actual
        X0_nuevo = eval(function_str.replace('x', str(X0)))

        if X0_nuevo != 0.0:
            error = calculo_error(X0_nuevo, X0)

        steps.append({
            'X0': X0,
            'X0_nuevo': X0_nuevo,
            'error': error
        })

        X0 = X0_nuevo

    return X0, steps