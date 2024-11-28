from flask import Flask, request, jsonify
from flask_cors import CORS
import sympy as sp
app = Flask(__name__)
CORS(app)

def evaluar_funcion_segura(funcion_str, x):
    try:
        x_sym = sp.Symbol('x')
        expr = sp.sympify(funcion_str)
        resultado = expr.subs(x_sym, x)
        if sp.im(resultado) != 0:  # Verifica si el resultado tiene una parte imaginaria
            raise ValueError("La función generó un número complejo.")
        if abs(resultado) > 1e10:  # Umbral para detectar valores extremadamente grandes
            raise ValueError("La función generó un valor demasiado grande.")
        return float(resultado)
    except Exception as e:
        raise ValueError(f"Error al evaluar la función: {str(e)}")

def validar_funcion(funcion_str):
    try:
        expr = sp.sympify(funcion_str)  # Convierte la cadena en una expresión simbólica
        variables = expr.free_symbols   # Obtiene las variables simbólicas libres
        if len(variables) != 1 or str(next(iter(variables))) != 'x':
            raise ValueError("La función debe contener exactamente una variable, y debe ser 'x'.")
        return True
    except sp.SympifyError as e:  # Errores relacionados con la conversión de sympy
        raise ValueError("La función proporcionada no es una expresión válida.")
    except ValueError as e: 
        raise e  


@app.route('/secante', methods=['POST'])
def metodo_secante():
    try:
        data = request.get_json()

        if not data:
            return jsonify({
                'error': 'No se recibió ninguna entrada.',
                'mensaje': 'Debe enviar los datos requeridos en formato JSON.'
            }), 400

        campos_requeridos = ['x0', 'x1', 'tolerancia', 'funcion']
        for campo in campos_requeridos:
            if campo not in data:
                return jsonify({
                    'error': f'Falta el campo {campo}.',
                    'mensaje': f'Por favor, incluya el campo {campo} en la solicitud.'
                }), 400

        try:
            x0 = float(data['x0'])
            x1 = float(data['x1'])
            tolerancia = float(data['tolerancia'])
        except (ValueError, TypeError):
            return jsonify({
                'error': 'Los valores de x0, x1 y tolerancia deben ser numéricos.',
                'mensaje': 'Los valores de x0, x1 y tolerancia deben ser numéricos.'
            }), 400

        if tolerancia <= 0:
            return jsonify({
                'error': 'La tolerancia debe ser un valor positivo.',
                'mensaje': 'Ingrese un valor de tolerancia mayor que 0.'
            }), 400

        funcion = data['funcion']

        try:
            validar_funcion(funcion)  # Validar que la función solo contiene la variable 'x'
        except ValueError as e:
            return jsonify({
                'error': 'Validación fallida.',
                'mensaje': str(e)  
            }), 400

        max_iteraciones = data.get('max_iteraciones', 100)

        iteraciones = []
        function_calls = 0
        converged = False
        x2 = None

        for iteracion in range(1, max_iteraciones + 1):
            try:
                fx0 = evaluar_funcion_segura(funcion, x0)
                fx1 = evaluar_funcion_segura(funcion, x1)
                function_calls += 2
            except ValueError as e:
                return jsonify({
                    'error': 'Error al evaluar la función.',
                    'mensaje': str(e)
                }), 400

            if fx1 == fx0:
                return jsonify({
                    'error': f'División por cero: f(x0) = f(x1) en la iteración {iteracion}.',
                    'mensaje':f'División por cero: f(x0) = f(x1) en la iteración {iteracion}.'
                }), 400

            x2 = x1 - fx1 * (x1 - x0) / (fx1 - fx0)
            if abs(x2) > 1e10:
                return jsonify({
                    'error': f'El valor de x2 se volvió demasiado grande en la iteración {iteracion}.',
                    'mensaje': 'Esto puede indicar divergencia. Intente con valores iniciales diferentes.'
                }), 400

            error = abs((x2 - x1) / x2) * 100 if x2 != 0 else float('inf')

            iteraciones.append({
                'iteracion': iteracion,
                'x0': x0,
                'x1': x1,
                'x2': x2,
                'error': error
            })

            if error < tolerancia:
                converged = True
                break

            x0, x1 = x1, x2

        if not converged:
            return jsonify({
                'error': 'No se alcanzó la convergencia.',
                'mensaje': f'El método alcanzó el límite de {max_iteraciones} iteraciones sin cumplir con la tolerancia especificada.',
                'iteraciones': iteraciones,
                'function_calls': function_calls
            }), 400

        return jsonify({
            'converged': True,
            'function_calls': function_calls,
            'iteraciones': iteraciones,
            'resultado_final': x2,
            'numero_iteraciones': len(iteraciones),
            'mensaje': f'El método convergió exitosamente en {len(iteraciones)} iteraciones.'
        })

    except Exception as e:
        return jsonify({
            'error': 'Ocurrió un error inesperado.',
            'mensaje': str(e)
        }), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5400)
