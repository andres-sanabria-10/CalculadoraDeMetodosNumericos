import sympy as sp
import numpy as np
import math

def home_controller():
    return {"message": "hello world"}


#BORRADOR METODO DE PUNTO FIJO
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