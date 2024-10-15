import sympy as sp
import numpy as np

def home_controller():
    return {"message": "hello world"}


def punto_fijo_controller(equation_str, x0, tol):
    x = sp.symbols('x')
    g = sp.sympify(equation_str)

    e = 100
    i = 0
    results = []

    while e > tol:
        x_new = float(g.subs(x, x0))

        e = abs((x_new - x0) / x_new) * 100

        results.append({
            'iteration': i,
            'g(x)': float(x0),
            'f(x)': float(x_new),
            'error': float(e)
        })
        i += 1
        x0 = x_new

    return results
