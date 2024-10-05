from scipy import optimize
import math
import sympy as sp

def home_controller():
    return {"message": "hello world"}

def suma_controller(a, b):
    return {"result": a + b}

def resta_controller(a, b):
    return {"result": a - b}

# Función f(x), que se recibirá como cadena y será evaluada
def secante_controller(func_str, x0, x1, E, max_iterations=101):
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
            result = eval(func_str, {"__builtins__": None}, allowed_locals)
            return result
        except ValueError as ve:
            print(f"Error en la evaluación de la función: {ve}")
            return float('nan')  # Retorna NaN para indicar que hubo un error en la evaluación

    
    iteration_data = []  # Para almacenar los datos de las iteraciones
    iteration = 0

    while iteration < max_iterations:
        # Calcular f(x0) y f(x1)
        f_x0 = f(x0)
        f_x1 = f(x1)
        
        # Manejar la división por cero en la fórmula de la secante
        if f_x1 - f_x0 == 0:
            return {"error": "División por cero en la fórmula de la secante"}

        # Aplicar la fórmula de la secante para calcular x_n1
        x_n1 = x1 - f_x1 * (x1 - x0) / (f_x1 - f_x0)

        # Calcular el error absoluto
        error = abs(x_n1 - x1)

        # Almacenar los resultados de la iteración
        iteration_data.append({
            'Iteration': iteration,
            'x_n': x1,
            '|x_n1 - x_n|': error
        })

        # Actualizar x0 y x1 para la próxima iteración
        x0 = x1
        x1 = x_n1

        # Verificar la condición de parada
        if error <= E and abs(f(x_n1)) <= E:
            break

        iteration += 1

    # Retornar la raíz y los datos de las iteraciones
    return {
        "raiz": x_n1,
        "iteraciones": iteration_data
    }
    