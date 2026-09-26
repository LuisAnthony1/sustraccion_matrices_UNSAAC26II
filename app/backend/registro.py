# registro de sustraccion de matrices - menu para elegir metodo
# unsaac - ingenieria informatica y de sistemas

import numpy as np

print("=================================================================")
print("   sustraccion de matrices: registro de metodos")
print("=================================================================")

# pedimos la cantidad de filas
while True:
    try:
        filas = int(input("ingrese la cantidad de filas: "))
        if filas > 0:
            break
        else:
            print("la cantidad de filas debe ser mayor a 0")
    except:
        print("ingrese un numero entero valido")

# pedimos la cantidad de columnas
while True:
    try:
        columnas = int(input("ingrese la cantidad de columnas: "))
        if columnas > 0:
            break
        else:
            print("la cantidad de columnas debe ser mayor a 0")
    except:
        print("ingrese un numero entero valido")

# pedimos los datos para la matriz a
print("\ningrese los elementos de la matriz a:")
matriz_a = []
for i in range(filas):
    fila = []
    for j in range(columnas):
        while True:
            try:
                valor = float(input(f"ingrese a[{i + 1}][{j + 1}]: "))
                if valor.is_integer():
                    valor = int(valor)
                fila.append(valor)
                break
            except:
                print("ingrese un numero valido")
    matriz_a.append(fila)

# pedimos los datos para la matriz b
print("\ningrese los elementos de la matriz b:")
matriz_b = []
for i in range(filas):
    fila = []
    for j in range(columnas):
        while True:
            try:
                valor = float(input(f"ingrese b[{i + 1}][{j + 1}]: "))
                if valor.is_integer():
                    valor = int(valor)
                fila.append(valor)
                break
            except:
                print("ingrese un numero valido")
    matriz_b.append(fila)

# mostramos el menu para elegir cual metodo usar
print("\nelija el metodo que desea usar:")
print("1. metodo 1: bucles for anidados")
print("2. metodo 2: comprension de listas")
print("3. metodo 3: vectorizacion con numpy")
print("4. probar los 3 metodos a la vez")

opcion = input("seleccione una opcion (1-4): ").strip()

# metodo 1 con bucles for
if opcion == "1":
    print("\ncalculando con metodo 1 (bucles for)...")
    matriz_c = []
    for i in range(filas):
        fila = []
        for j in range(columnas):
            resta = matriz_a[i][j] - matriz_b[i][j]
            fila.append(resta)
            print(f"c[{i + 1}][{j + 1}] = {matriz_a[i][j]} - {matriz_b[i][j]} = {resta}")
        matriz_c.append(fila)

    print("\nmatriz resultado c:")
    for i in range(filas):
        for j in range(columnas):
            print(matriz_c[i][j], end="\t")
        print()

# metodo 2 con comprension de listas
elif opcion == "2":
    print("\ncalculando con metodo 2 (comprension de listas)...")
    matriz_c = [
        [matriz_a[i][j] - matriz_b[i][j] for j in range(columnas)]
        for i in range(filas)
    ]

    print("\nmatriz resultado c:")
    for i in range(filas):
        for j in range(columnas):
            print(matriz_c[i][j], end="\t")
        print()

# metodo 3 con numpy
elif opcion == "3":
    print("\ncalculando con metodo 3 (numpy)...")
    arr_a = np.array(matriz_a, dtype=float)
    arr_b = np.array(matriz_b, dtype=float)
    arr_c = arr_a - arr_b

    print("\narreglo resultado c:")
    print(arr_c)

# probar los 3 metodos
elif opcion == "4":
    print("\nprobando los 3 metodos...")

    # 1. bucles
    c_bucles = []
    for i in range(filas):
        f = []
        for j in range(columnas):
            f.append(matriz_a[i][j] - matriz_b[i][j])
        c_bucles.append(f)

    # 2. comprension
    c_comprension = [
        [matriz_a[i][j] - matriz_b[i][j] for j in range(columnas)]
        for i in range(filas)
    ]

    # 3. numpy
    arr_a = np.array(matriz_a, dtype=float)
    arr_b = np.array(matriz_b, dtype=float)
    c_numpy = (arr_a - arr_b).tolist()

    print(f"resultado bucles:      {c_bucles}")
    print(f"resultado comprension: {c_comprension}")
    print(f"resultado numpy:       {c_numpy}")
    print(f"¿los 3 dieron lo mismo?: {c_bucles == c_comprension}")

else:
    print("opcion no valida")

print("=================================================================")
print("programa finalizado.")
