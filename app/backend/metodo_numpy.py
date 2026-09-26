# sustraccion de matrices - metodo 3 con vectorizacion numpy
# unsaac - ingenieria informatica y de sistemas

import numpy as np

print("=================================================================")
print("   sustraccion de matrices: metodo 3 (vectorizacion numpy)")
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
                # si es entero lo guardamos como entero
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
                # si es entero lo guardamos como entero
                if valor.is_integer():
                    valor = int(valor)
                fila.append(valor)
                break
            except:
                print("ingrese un numero valido")
    matriz_b.append(fila)

# convertimos las listas a arreglos de numpy
arreglo_a = np.array(matriz_a, dtype=float)
arreglo_b = np.array(matriz_b, dtype=float)

# mostramos el arreglo a en numpy
print("\narreglo a (minuendo en numpy):")
print(arreglo_a)

# mostramos el arreglo b en numpy
print("\narreglo b (sustraendo en numpy):")
print(arreglo_b)

# hacemos la resta vectorizada directamente con el operador menos
print("\noperacion vectorizada: arreglo_a - arreglo_b")
arreglo_c = arreglo_a - arreglo_b

# mostramos el arreglo resultado
print("\narreglo resultante c:")
print(arreglo_c)

print("=================================================================")
print("programa finalizado.")
