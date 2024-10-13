from scipy import optimize
import math
import sympy as sp
import numpy as np
import scipy.linalg as sla



def home_controller():
    return {"message": "hello world"}

def suma_controller(a, b):
    return {"result": a + b}

def resta_controller(a, b):
    return {"result": a - b}

def eval_equations(f_equations, variables):
    """Evalúa las ecuaciones dadas las variables."""
    # Utilizar eval para evaluar dinámicamente las ecuaciones
    return np.array([eval(eq, {**dict(zip(['x', 'y', 'z'], variables)), 'np': np}) for eq in f_equations])

def broyden_good(variables, f_equations, tol=1e-10, maxIters=50):
    steps_taken = 0
    f = eval_equations(f_equations, variables)
    J = np.zeros((len(f_equations), len(variables)))  # Jacobiana inicial

    # Estimar la Jacobiana inicial
    h = 1e-8  # Pequeña perturbación para aproximar la Jacobiana
    for i in range(len(f_equations)):
        for j in range(len(variables)):
            temp_vars = variables.copy()
            temp_vars[j] += h
            J[i, j] = (eval_equations(f_equations, temp_vars)[i] - f[i]) / h

    while np.linalg.norm(f, 2) > tol and steps_taken < maxIters:
        try:
            s = sla.solve(J, -f)
        except sla.LinAlgError:
            print("Matriz singular. Intentando perturbar la Jacobiana.")
            # Perturbar la Jacobiana para evitar singularidad
            J += np.eye(len(variables)) * 1e-5
            try:
                s = sla.solve(J, -f)
            except sla.LinAlgError:
                return steps_taken, variables, "Matrix singular after perturbation, unable to solve."

        variables += s  # Actualiza todas las variables
        newf = eval_equations(f_equations, variables)
        z = newf - f

        # Actualiza la Jacobiana
        J += (np.outer((z - np.dot(J, s)), s)) / (np.dot(s, s))

        f = newf
        steps_taken += 1

        # Verificar si el método está estancado
        if np.linalg.norm(s) < tol:
            break

    return steps_taken, variables, None  # Añadir None si no hay error