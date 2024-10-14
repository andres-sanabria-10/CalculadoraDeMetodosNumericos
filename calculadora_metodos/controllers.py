from sympy import symbols, Matrix
import sympy as sp
import numpy as np
from scipy.optimize import fsolve



def home_controller():
    return {"message": "hello world"}

def suma_controller(a, b):
    return {"result": a + b}

def resta_controller(a, b):
    return {"result": a - b}


def broyden_controller(equations, initial_guess, tolerance, max_iterations):
    # Define the symbols
    symbols = sp.symbols(' '.join(['x' + str(i) for i in range(len(initial_guess))]))

    # Convert the equations into sympy expressions
    f = [sp.sympify(eq) for eq in equations]

    # Initial guess
    x_n = np.array(initial_guess, dtype=float)
    
    # Create the Jacobian (initially the identity matrix)
    J_n = np.eye(len(equations))
    
    iteration_data = []
    
    for iteration in range(max_iterations):
        # Calculate function values
        F_n = np.array([func.evalf(subs={symbols[i]: x_n[i] for i in range(len(x_n))}) for func in f], dtype=float)

        # Solve the linear system J_n * delta = -F_n
        delta = np.linalg.solve(J_n, -F_n)

        # Update x_n
        x_n1 = x_n + delta

        # Update Jacobian using Broyden's update formula
        s = x_n1 - x_n
        y = np.array([func.evalf(subs={symbols[i]: x_n1[i] for i in range(len(x_n1))}) for func in f], dtype=float) - F_n
        
        J_n += np.outer((y - J_n @ s), s) / (s.T @ s)

        # Store iteration data
        iteration_data.append({
            'Iteración': iteration + 1,
            'x': x_n1.tolist(),
            'F(x)': F_n.tolist(),
            '||x_n1 - x_n||': np.linalg.norm(delta)
        })

        # Check convergence
        if np.linalg.norm(delta) < tolerance:
            break

        # Update for next iteration
        x_n = x_n1
    
    return x_n.tolist(), iteration_data