import sympy as sp
import numpy as np

def home_controller():
    return {"message": "hello world"}


def secante_controller(equation_str, x0, x1, tol, max_iter=100):
    x = sp.symbols('x')
    equation = sp.sympify(equation_str)
    f = sp.lambdify(x, equation)

    iteraciones = []

    for i in range(max_iter):
        f_x0 = float(f(x0))
        f_x1 = float(f(x1))

        if f_x1 - f_x0 == 0:
            return {"error": f"División por cero en la iteración {i}"}

        x2 = x1 - (x1 - x0) * f_x1 / (f_x1 - f_x0)

        error = abs(x2 - x1)

        iteraciones.append({
            "iteracion": i + 1,
            "x0": float(x0),
            "x1": float(x1),
            "x2": float(x2),
            "error": float(error)
        })

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
