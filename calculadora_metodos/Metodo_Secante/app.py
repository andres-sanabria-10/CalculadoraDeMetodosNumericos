from flask import Flask, request, jsonify
from flask_cors import CORS
import sympy as sp

app = Flask(__name__)
CORS(app)

def evaluar_funcion_segura(funcion_str, x):
    try:
        x_sym = sp.Symbol('x')
        expr = sp.sympify(funcion_str).subs(sp.Symbol('e'), sp.exp(1))  # Sustituir 'e' por exp(1)
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
        expr = sp.sympify(funcion_str).subs(sp.Symbol('e'), sp.exp(1))  # Convierte la cadena en una expresión simbólica
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

        campos_requeridos = ['punto_inicial_a', 'punto_inicial_b', 'tolerancia', 'funcion']
        for campo in campos_requeridos:
            if campo not in data:
                return jsonify({
                    'error': f'Falta el campo {campo}.',
                    'mensaje': f'Por favor, incluya el campo {campo} en la solicitud.'
                }), 400

        try:
            punto_inicial_a = float(data['punto_inicial_a'])
            punto_inicial_b = float(data['punto_inicial_b'])
            tolerancia = float(data['tolerancia'])
        except (ValueError, TypeError):
            return jsonify({
                'error': 'Los valores de punto_inicial_a, punto_inicial_b y tolerancia deben ser numéricos.',
                'mensaje': 'Los valores de punto_inicial_a, punto_inicial_b y tolerancia deben ser numéricos.'
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
        x_siguiente = None

        for iteracion in range(1, max_iteraciones + 1):
            try:
                fx0 = evaluar_funcion_segura(funcion, punto_inicial_a)
                fx1 = evaluar_funcion_segura(funcion, punto_inicial_b)
                function_calls += 2
            except ValueError as e:
                return jsonify({
                    'error': 'Error al evaluar la función.',
                    'mensaje': str(e)
                }), 400

            if fx1 == fx0:
                return jsonify({
                    'error': f'División por cero: f(punto_inicial_a) = f(punto_inicial_b) en la iteración {iteracion}.',
                    'mensaje': f'División por cero: f(punto_inicial_a) = f(punto_inicial_b) en la iteración {iteracion}.'
                }), 400

            x_siguiente = punto_inicial_b - fx1 * (punto_inicial_b - punto_inicial_a) / (fx1 - fx0)
            if abs(x_siguiente) > 1e10:
                return jsonify({
                    'error': f'El valor de x_siguiente se volvió demasiado grande en la iteración {iteracion}.',
                    'mensaje': 'Esto puede indicar divergencia. Intente con valores iniciales diferentes.'
                }), 400

            error = abs((x_siguiente - punto_inicial_b) / x_siguiente) * 100 if x_siguiente != 0 else float('inf')

            iteraciones.append({
                'iteracion': iteracion,
                'punto_a': punto_inicial_a,
                'punto_b': punto_inicial_b,
                'x_siguiente': x_siguiente,
                'error': error
            })

            if error < tolerancia:
                converged = True
                break

            punto_inicial_a, punto_inicial_b = punto_inicial_b, x_siguiente

        if not converged:
            return jsonify({
                'error': 'No se alcanzó la convergencia.',
                'mensaje': f'El método alcanzó el límite de {max_iteraciones} iteraciones sin cumplir con la tolerancia especificada.',
                'iteraciones': iteraciones,
                'function_calls': function_calls
            }), 400

        return jsonify({
            'converged': True,
            'iteraciones': iteraciones,
            'resultado_final': x_siguiente,
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
