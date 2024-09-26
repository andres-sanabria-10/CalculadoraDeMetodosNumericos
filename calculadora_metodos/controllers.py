import sympy as sp

def home_controller():
    return {"message": "hello world"}

def suma_controller(a, b):
    return {"result": a + b}

def resta_controller(a, b):
    return {"result": a - b}

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


def punto_fijo_controller(equation_str, x0, tol):
    x = sp.symbols('x')
    g = sp.sympify(equation_str)

    e = 100
    i = 0
    results = []

    while e > tol:
        # Evaluar g(x)
        x_new = float(g.subs(x, x0))  # Convertir a float

        # Calcular el error
        e = abs((x_new - x0) / x_new) * 100

        # Guardar resultados
        results.append({
            'iteration': i,
            'g(x)': float(x0),  # Asegurarse de que sea float
            'f(x)': float(x_new),  # Asegurarse de que sea float
            'error': float(e)  # Asegurarse de que sea float
        })
        i += 1
        x0 = x_new  # Actualizar x0

    return results