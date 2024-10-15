import numpy as np
import sympy as sp
import re

def home_controller():
    return {"message": "hello world"}

# CONTROLADOR METODO DE BROYDEN
def broyden_controller(ecuaciones_str, valores_iniciales, tolerancia=1e-6, max_iteraciones=100):
    umbral = 1e10
    ecuaciones = ecuaciones_str.split(",")
    ecuaciones_completas = " ".join(ecuaciones)
    variables = sorted(list(set(re.findall(r'[a-zA-Z]\w*', ecuaciones_completas))))
    funciones_matematicas = ['sin', 'cos', 'tan', 'cot', 'asin', 'acos', 'atan', 'exp', 'log']
    variables = [var for var in variables if var not in funciones_matematicas]
    if len(variables) != len(valores_iniciales):
        raise ValueError(f"Número de variables ({len(variables)}) no coincide con los valores iniciales ({len(valores_iniciales)}).")
    
    variables_simbolicas = sp.symbols(variables)
    
    sistema_ecuaciones_numerico = []
    try:
        funciones_trigonometricas = {
            'sin': sp.sin, 'cos': sp.cos, 'tan': sp.tan, 'cot': sp.cot,
            'asin': sp.asin, 'acos': sp.acos, 'atan': sp.atan,
            'exp': sp.exp, 'log': sp.log
        }

        for ecuacion in ecuaciones:
            ecuacion_simbolica = sp.sympify(ecuacion.strip(), locals=funciones_trigonometricas)  # Reconocer funciones matemáticas
            funcion_numerica = sp.lambdify(variables_simbolicas, ecuacion_simbolica, "numpy")
            sistema_ecuaciones_numerico.append(funcion_numerica)
    except Exception as e:
        raise ValueError(f"Error al procesar las ecuaciones: {e}")

    valores_iniciales = [float(v) for v in valores_iniciales]

    # Calculo para jacobiano inicial
    def calcular_jacobiano(funciones, V, h=1e-8):
        numero_variables = len(V)
        jacobiano = np.zeros((len(funciones), numero_variables))
        funcion_evaluada = np.array([f(*V) for f in funciones])
        for i in range(numero_variables):
            V_modificado = np.copy(V)
            V_modificado[i] += h
            funcion_modificada = np.array([f(*V_modificado) for f in funciones])
            jacobiano[:, i] = (funcion_modificada - funcion_evaluada) / h
        return jacobiano

    def metodo_broyden(funciones, vector_inicial, tolerancia=1e-6, maximo_iteraciones=100):
        V_actual = np.array(vector_inicial, dtype=float)
        jacobiano_inicial = calcular_jacobiano(funciones, V_actual)
        A_inversa = np.linalg.inv(jacobiano_inicial)

        iteraciones = []
        iteracion = 0
        while iteracion < maximo_iteraciones:
            valor_funcion = np.array([f(*V_actual) for f in funciones])

            if np.linalg.norm(valor_funcion) > umbral:
                raise ValueError("La ecuación diverge. Los valores son demasiado grandes.")

            if np.linalg.norm(valor_funcion) < tolerancia:
                return V_actual.tolist(), iteraciones 

            # Calculamos la actualización para el vector V
            delta_V = -np.dot(A_inversa, valor_funcion)
            nuevo_V = V_actual + delta_V
            nuevo_valor_funcion = np.array([f(*nuevo_V) for f in funciones])

            diferencia_V = nuevo_V - V_actual
            diferencia_funcion = nuevo_valor_funcion - valor_funcion

            # Actualizamos la aproximación de la inversa del Jacobiano
            A_inversa += np.outer(diferencia_V - np.dot(A_inversa, diferencia_funcion), 
                                  np.dot(A_inversa, diferencia_funcion)) / np.dot(np.dot(A_inversa, diferencia_funcion), diferencia_funcion)

            iteraciones.append({
                'iteracion': iteracion + 1,
                'V': V_actual.tolist(),
                'error': np.linalg.norm(valor_funcion)
            })

            V_actual = nuevo_V
            iteracion += 1

        raise ValueError("No se alcanzó la convergencia dentro del número máximo de iteraciones.")

    solucion_final = metodo_broyden(sistema_ecuaciones_numerico, valores_iniciales, tolerancia, max_iteraciones)
    return solucion_final
