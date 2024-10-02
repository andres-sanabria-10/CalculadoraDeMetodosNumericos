#from scipy import optimize
import numpy as np
import sympy as sp
import math

#BORRADOR METODO DE BISECCION

def biseccion_controller(func_input, Xi, Xu, error=1e-6):
    umbral = 1e10 
    x = sp.Symbol('x')
    try:
        f_expr = sp.sympify(func_input)  # Convertir la expresión de texto a simbólica
        f = sp.lambdify(x, f_expr, 'numpy')  # Crear una función ejecutable a partir de la expresión
    except Exception as e:
        raise ValueError(f"Error al procesar la función: {e}")

    # Bisección
    num_puntos = 10
    puntos = np.linspace(Xi, Xu, num_puntos)
    f_puntos = [f(p) for p in puntos]

    # Verificar cambio de signo en el intervalo
    cambio_signo = any(f_puntos[i] * f_puntos[i + 1] < 0 for i in range(len(f_puntos) - 1))
    if not cambio_signo:
        raise ValueError("No hay un cambio de signo en el intervalo, no hay una raíz factible.")

    iteraciones = []
    contador = 0
    while True:
        Xr = (Xi + Xu) / 2
        fXr = f(Xr)

        # Verificar si el valor es demasiado grande
        if abs(fXr) > umbral:
            raise ValueError("La ecuación diverge. Los valores son demasiado grandes.")

        error_relativo = (Xu - Xi) / 2

        iteraciones.append({
            'iteracion': contador + 1,
            'Xi': round(Xi, 8),
            'Xu': round(Xu, 8),
            'Xr': round(Xr, 8),
            'f(Xr)': round(fXr, 8),
            'error': round(error_relativo, 8),
        })

        # Comprobar convergencia
        if abs(fXr) < error or error_relativo < error:
            return Xr, iteraciones

        # Actualizar los extremos del intervalo
        if f(Xi) * fXr < 0:
            Xu = Xr
        else:
            Xi = Xr

        contador += 1