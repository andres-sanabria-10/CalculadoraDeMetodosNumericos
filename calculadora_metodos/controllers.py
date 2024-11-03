#from scipy import optimize
import math
import sympy as sp
import re
import numpy as np

def home_controller():
    return {"message": "hello world"}

def suma_controller(a, b):
    return {"result": a + b}

def resta_controller(a, b):
    return {"result": a - b}


def calculo_error(a, b):
    return abs((a - b) / a)
def evaluar_funcion(funcion_str, x):
    # Evalúa la función a partir de un string
    return eval(funcion_str)

def calculo_funcion(function_str, transformada_str, initial_guess, tolerance):
    X0 = initial_guess
    error = 1.0
    steps = []
    iteraciones = 0

    # Definir la variable simbólica 'x'
    x = sp.symbols('x')

    # Convertir el string de la función en una expresión simbólica
    function_expr = sp.sympify(function_str)
    transformada_expr = sp.sympify(transformada_str)

    while error > tolerance:
        # Evalúa la función con el punto actual
        X0_nuevo = float(transformada_expr.subs(x, X0))

        if X0_nuevo != 0.0:
            error = calculo_error(X0_nuevo, X0)

        iteraciones += 1

        steps.append({
            'Iteración': f'Iteración {iteraciones}', 
            'X0': X0,
            'X0_nuevo': X0_nuevo,
            'error': error
        })

        X0 = X0_nuevo

    return X0, steps, iteraciones


def bisection_method(funcion, punto_a, punto_b, tolerancia, max_iteraciones):
    iteraciones = []
    function_calls = 0
    converged = False
    punto_medio_anterior = (punto_a + punto_b) / 2  # Inicializa el punto medio anterior

    for iteracion in range(1, max_iteraciones + 1):
        # Calcula el punto medio
        punto_medio = (punto_a + punto_b) / 2
        valor_funcion_medio = evaluar_funcion(funcion, punto_medio)
        function_calls += 1

        # Cálculo del error relativo
        if iteracion > 1:  # Evitar error en la primera iteración
            error = abs((punto_medio - punto_medio_anterior) / punto_medio) * 100
        else:
            error = float('inf')  # No hay error en la primera iteración

        # Guarda los datos de la iteración
        iteraciones.append({
            'iteracion': iteracion,
            'punto_a': punto_a,
            'punto_b': punto_b,
            'punto_medio': punto_medio,
            'error': error
        })

        # Verifica si el valor de la función en el punto medio es suficientemente pequeño
        if abs(valor_funcion_medio) < tolerancia:
            converged = True
            break

        # Actualiza los puntos según el signo de la función
        valor_funcion_a = evaluar_funcion(funcion, punto_a)
        if valor_funcion_a * valor_funcion_medio < 0:  # Hay una raíz en [punto_a, punto_medio]
            punto_b = punto_medio
        else:  # Hay una raíz en [punto_medio, punto_b]
            punto_a = punto_medio

        # Actualiza el punto medio anterior para la siguiente iteración
        punto_medio_anterior = punto_medio

    return {
        'converged': converged,
        'function_calls': function_calls,
        'iteraciones': iteraciones,
        'resultado_final': punto_medio if converged else None,
        'numero_iteraciones': len(iteraciones)
    }



def newton_raphson_controller(func_str, func_prime_str, x0, E, max_iterations):
    # Definir la variable simbólica
    x = sp.symbols('x')

    # Convertir las cadenas de funciones en funciones simbólicas
    f_sympy = sp.sympify(func_str)
    f_prime_sympy = sp.sympify(func_prime_str)
    f_double_prime_sympy = sp.diff(f_prime_sympy, x)  # Calcular la segunda derivada de f(x)
    
    # Convertir la función simbólica y sus derivadas en funciones evaluables
    f = sp.lambdify(x, f_sympy)
    f_prime = sp.lambdify(x, f_prime_sympy)
    f_double_prime = sp.lambdify(x, f_double_prime_sympy)

    # Definir g(x)
    g_sympy = x - (f_sympy / f_prime_sympy)
    g = sp.lambdify(x, g_sympy)

    # Definir g'(x) = (f(x) * f''(x)) / (f'(x))^2
    def g_prime(x_val):
        f_x = f(x_val)
        f_prime_x = f_prime(x_val)
        f_double_prime_x = f_double_prime(x_val)
        return (f_x * f_double_prime_x) / (f_prime_x ** 2)

    # Implementación de Newton-Raphson
    x_n = float(x0)
    iteration_data = []  # Para almacenar los datos de las iteraciones
    iteration = 0
    
    while iteration < max_iterations:
        x_n1 = g(x_n)

        # Calcular el error
        diferencia = abs(x_n1 - x_n)
        error = abs(diferencia / x_n1)

        # Obtener el valor de g'(x) en x_n
        g_prime_val = g_prime(x_n)

        # Almacenar los resultados de la iteración
        iteration_data.append({
            'Iteración': iteration + 1,
            'x_n': float(x_n),
            "g'(x)": float(g_prime_val),  # Mostrar g'(x)
            '|x_n1 - x_n|': float(diferencia), 
            '|Error|': float(error)
        })

        # Actualizar para la siguiente iteración
        x_n = x_n1

        # Verificar condiciones de parada
        if error <= E and abs(f(x_n)) <= E:
            break
        
        iteration += 1

    return float(x_n), iteration_data

def secante_controller(func_str, x0, x1, E, max_iterations=100):
     # Crear un contexto seguro para eval
    allowed_locals = {
        'math': math,
        'exp': math.exp,
        'log': math.log,
        'sqrt': math.sqrt,
        'sin': math.sin,
        'cos': math.cos,
        'tan': math.tan,
        'pi': math.pi,
        'e': math.e
    }
    
    def f(x):
        # Asegurarse de que la expresión sea evaluable
        try:
            result = eval(func_str, {"__builtins__": None}, {**allowed_locals, 'x': x})
            return result
        except ValueError as ve:
            print(f"Error en la evaluación de la función: {ve}")
            return float('nan')  # Retorna NaN para indicar que hubo un error en la evaluación

    iteration_data = []  # Para almacenar los datos de las iteraciones
    iteration = 1

    while iteration < max_iterations:
        # Calcular f(x0) y f(x1)
        f_x0 = f(x0)
        f_x1 = f(x1)
        
        # Manejar la división por cero en la fórmula de la secante
        if f_x1 - f_x0 == 0:
            return {"error": "División por cero en la fórmula de la secante"}

        # Aplicar la fórmula de la secante para calcular x_n1
        x_n1 = x1 - f_x1 * (x1 - x0) / (f_x1 - f_x0)

        # Calcular el error relativo en porcentaje
        diferencia = abs(x_n1 - x1)
        error=abs(diferencia/x_n1)

        

        


        # Almacenar los resultados de la iteración
        iteration_data.append({
            'Iteración': iteration  ,
            'x': x_n1,
            'F(x)': f(x_n1),
            '|x(i) - x(i-1)|': error
        })

        # Actualizar x0 y x1 para la próxima iteración
        x0 = x1
        x1 = x_n1

        # Verificar la condición de parada
        if error <= E:
            break

        iteration += 1

    # Retornar la raíz y los datos de las iteraciones
    return {
        "iteraciones": iteration_data,
        "raiz": x_n1,
        "Iteracion": iteration

    }
    
    
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