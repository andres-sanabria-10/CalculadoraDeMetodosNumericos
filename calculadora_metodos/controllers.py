import sympy as sp
import numpy as np

def home_controller():
    return {"message": "hello world"}


def bisection_controller(equation_str, xi, xu, tol):
    x = sp.symbols('x')
    equation = sp.sympify(equation_str)

    erp = 100
    xr = 0
    i = 1
    results = []

    while erp > tol:
        aux = xr
        xr = (xi + xu) / 2
        fxi = equation.subs(x, xi)
        fxr = equation.subs(x, xr)

        z = fxi * fxr

        if z > 0:
            xi = xr
        else:
            xu = xr

        erp = abs((xr - aux) / xr) * 100

        results.append({'iteration': i, 'xr': xr, 'error': erp})
        i += 1

    return {"root": xr, "error": erp, "iterations": results}
