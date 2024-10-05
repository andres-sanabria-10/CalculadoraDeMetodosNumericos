import math

def calculo_raiz(a):
    b = math.sqrt(pow(a, 3))
    c = (pow(a, 2)) / 3.5
    return (-1) / (2 * (b + c - 4))

def calculo_error(a, b):
    return abs((a - b) / a)

def main():
    X0 = 1.5
    error = 1.0
    X0_nuevo = 0.0
    resultado = 0.0

    while error > 0.000001:
        X0_nuevo = calculo_raiz(X0)

        if X0_nuevo != 0.0:
            error = calculo_error(X0_nuevo, X0)

        X0 = X0_nuevo
        print(f"Su X0 ahora es: {X0}")
        print(f"Error: {error}")
        print("---------------------------------------------------------------")
        resultado = X0

    print(f"El resultado final es: {resultado}")

if __name__ == "__main__":
    main()
