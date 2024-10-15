import sympy as sp
import numpy as np

def home_controller():
    return {"message": "hello world"}


def newton_raphson_controller(equation_str, derivative_str, x0, tol):
    x = sp.symbols('x')
    f = sp.sympify(equation_str)
    f_prime = sp.sympify(derivative_str)

    xi = x0
    erp = 100
    i = 0
    results = []

    while erp > tol:
        f_xi = f.subs(x, xi)
        f_prime_xi = f_prime.subs(x, xi)

        if f_prime_xi == 0:
            return {"error": "División por cero, la derivada es cero en la iteración", "iteration": i}

        xi_next = float(xi - (f_xi / f_prime_xi))
        erp = abs((xi_next - xi) / xi_next) * 100

        results.append({
            'iteration': i,
            'xi': float(xi),
            'xi_next': float(xi_next),
            'error': float(erp)
        })

        xi = xi_next
        i += 1

    return {"root": float(xi), "iterations": results, "final_error": float(erp)}


        if error < tol:
            return {
                "raiz": float(x2),
                "iteraciones": iteraciones,
                "convergencia": True
            }

        x0, x1 = x1, x2

    return {
        "error": "Se alcanzó el número máximo de iteraciones sin convergencia",
        "iteraciones": iteraciones,
        "convergencia": False
    }
