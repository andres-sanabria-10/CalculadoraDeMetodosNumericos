import sympy as sp

def home_controller():
    return {"message": "hello world"}

def metodo_newton_controller(ecuacion_str, x_inicial, tolerancia, max_iter):
    aproximaciones = []
    iteraciones = []
    aproximaciones.append(x_inicial)
    iteracion = 0

    funcion_simb = sp.sympify(ecuacion_str)

    variable_simb = list(funcion_simb.free_symbols)[0] 

    derivada_simb = sp.diff(funcion_simb, variable_simb)
    segunda_derivada_simb = sp.diff(derivada_simb, variable_simb)

    funcion = sp.lambdify(variable_simb, funcion_simb, 'numpy')
    derivada = sp.lambdify(variable_simb, derivada_simb, 'numpy')
    segunda_derivada = sp.lambdify(variable_simb, segunda_derivada_simb, 'numpy')

    while iteracion < max_iter:
        valor_actual = aproximaciones[-1]
        valor_funcion = funcion(valor_actual)
        valor_derivada = derivada(valor_actual)
        valor_segunda_derivada = segunda_derivada(valor_actual)

        if valor_derivada == 0:
            raise ValueError("La derivada es cero, no se puede continuar.")

        siguiente_valor = valor_actual - (valor_funcion / valor_derivada)
        aproximaciones.append(siguiente_valor)

        error = (siguiente_valor - valor_actual) / siguiente_valor
        x_abs = abs(siguiente_valor - valor_actual)
        g_prima = abs(((valor_derivada**2) - (valor_funcion * valor_segunda_derivada)) / (valor_derivada**2))

        iteraciones.append({
            'Iteración': iteracion + 1,
            'Valor actual': valor_actual,
            'Valor siguiente': siguiente_valor,
            'Error absoluto': x_abs,
            'g\'': g_prima,
            'Error relativo': error
        })

        if abs(error) < tolerancia:
            return siguiente_valor, iteraciones

        iteracion += 1

    return aproximaciones[-1], iteraciones
