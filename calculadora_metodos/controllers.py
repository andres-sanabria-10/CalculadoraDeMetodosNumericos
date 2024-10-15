import sympy as sp
import numpy as np

def home_controller():
    return {"message": "hello world"}


def broyden_controller(f1_str, f2_str, x0, y0, tol, max_iter=100):
    x, y = sp.symbols('x y')

    f1 = sp.sympify(f1_str)
    f2 = sp.sympify(f2_str)

    f1E = sp.lambdify((x, y), f1)
    f2E = sp.lambdify((x, y), f2)

    f1x = sp.diff(f1, x)
    f1y = sp.diff(f1, y)
    f2x = sp.diff(f2, x)
    f2y = sp.diff(f2, y)

    f1xE = sp.lambdify((x, y), f1x)
    f1yE = sp.lambdify((x, y), f1y)
    f2xE = sp.lambdify((x, y), f2x)
    f2yE = sp.lambdify((x, y), f2y)

    J = np.array([[f1xE(x0, y0), f1yE(x0, y0)],
                  [f2xE(x0, y0), f2yE(x0, y0)]])
    x_vec = np.array([x0, y0])
    f_val = np.array([f1E(x0, y0), f2E(x0, y0)])

    iteraciones = []

    for i in range(max_iter):
        delta_x = np.linalg.solve(J, -f_val)

        x_vec = x_vec + delta_x
o
        f_val_new = np.array([f1E(x_vec[0], x_vec[1]), f2E(x_vec[0], x_vec[1])])

        error = np.linalg.norm(f_val_new)

        iteraciones.append({
            "iteracion": i + 1,
            "x": float(x_vec[0]),
            "y": float(x_vec[1]),
            "error": float(error)
        })

        if error < tol:
            return {
                "solucion": [float(x_vec[0]), float(x_vec[1])],
                "iteraciones": iteraciones,
                "convergencia": True
            }

        delta_f = f_val_new - f_val
        f_val = f_val_new
        J = J + np.outer((delta_f - J @ delta_x) / np.dot(delta_x, delta_x), delta_x)

    return {
        "error": "No convergió en el número máximo de iteraciones",
        "iteraciones": iteraciones,
        "convergencia": False
    }