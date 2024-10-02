import sympy as sp
import numpy as np
import math

def home_controller():
    return {"message": "hello world"}


#METODO DE PUNTO FIJO
def punto_fijo_controller(g_func_str, x0, margenError=1e-6, umbral=1e10):
    x = sp.Symbol('x')
    
    try:
        # Convertir la función ingresada en una expresión simbólica
        g_expr = sp.sympify(g_func_str)
        # Usar numpy en lugar de math para manejar mejor las funciones
        g = sp.lambdify(x, g_expr, 'numpy')
    except Exception as e:
        return {"error": f"Error al procesar la función: {e}"}
    
    iteraciones = []
    x_actual = x0
    contador = 0
    
    while True:
        try:
            x_siguiente = g(x_actual)
            if math.isnan(x_siguiente):
                raise ValueError("La ecuación no es válida para este valor de x (resultado indefinido o NaN).")
            if abs(x_siguiente) > umbral:
                raise ValueError("La ecuación diverge")
        except Exception as e:
            return {"error": f"{e}"}
        
        iteraciones.append({
            '#iteracion': contador + 1,
            'xi': x_siguiente,
            'error': abs(x_siguiente - x_actual) / abs(x_siguiente),
        })
        
        if abs(x_siguiente - x_actual) < margenError:
            return {"resultado": x_siguiente, "iteraciones": iteraciones}
        
        x_actual = x_siguiente
        contador += 1

