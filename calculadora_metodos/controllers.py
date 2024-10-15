from scipy import optimize
import math
import sympy as sp

def home_controller():
    return {"message": "hello world"}

def suma_controller(a, b):
    return {"result": a + b}

def resta_controller(a, b):
    return {"result": a - b}


def calculo_error(a, b):
    return abs((a - b) / a)

def punto_fijo_controller(func_inicial_str, func_despejada_str, valor_inicial, tolerancia, max_iteraciones):
    def FuncionIn(x):
        return eval(func_inicial_str)
    def Function_Des(x):
        return eval(func_despejada_str)
    table_PF = []  # Tabla para almacenar iteraciones
    root = []
    x = valor_inicial
    err = 100
    Itera = 1
    root.append(x)
    while abs(err) > tolerancia and Itera <= max_iteraciones:  # Añadir límite de iteraciones
        xs = Function_Des(x)   # Se calcula una nueva iteración
        root.append(xs)
        err = abs((xs - x) / xs) * 100  # Se calcula el error relativo
        table_PF.append([Itera, x, xs, abs(FuncionIn(x)), abs(err)])
        x = xs
        Itera += 1
    response = {
        "tabla_punto_fijo": table_PF,
        "raiz": x,
        "mensaje": "Cálculo completado"
    }
    
    return response