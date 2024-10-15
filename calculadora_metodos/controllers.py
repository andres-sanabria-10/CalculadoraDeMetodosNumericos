import sympy as sp

def home_controller():
    return {"message": "hello world"}


# Controlador del método de la secante
def metodo_secante_controller(ecuacion_str, x0, x1, tolerancia, max_iter):
    aproximaciones = []
    iteraciones = []

    funcion_simb = sp.sympify(ecuacion_str)
    variable_simb = list(funcion_simb.free_symbols)[0] 
    funcion = sp.lambdify(variable_simb, funcion_simb, 'numpy')

    for i in range(max_iter):
        valor_funcion_x0 = funcion(x0)
        valor_funcion_x1 = funcion(x1)

        if valor_funcion_x1 == valor_funcion_x0:
            raise ValueError("La función tiene valores iguales en x0 y x1, no se puede continuar.")

        siguiente_valor = x1 - valor_funcion_x1 * (x1 - x0) / (valor_funcion_x1 - valor_funcion_x0)
        aproximaciones.append(siguiente_valor)

        iteraciones.append({
            'Iteración': i + 1,
            'x0': x0,
            'x1': x1,
            'Valor siguiente': siguiente_valor,
            'Error absoluto': abs(valor_funcion_x1),
        })

        # Verificar la convergencia
        if abs(valor_funcion_x1) < tolerancia:
            return siguiente_valor, iteraciones

        # Actualizar los valores para la siguiente iteración
        x0 = x1
        x1 = siguiente_valor

    return aproximaciones[-1], iteraciones
