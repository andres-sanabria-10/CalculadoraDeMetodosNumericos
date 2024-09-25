from scipy import optimize
import numpy as np
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