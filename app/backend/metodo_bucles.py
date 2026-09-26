# sustraccion de matrices - metodo 1 con bucles for
# unsaac - ingenieria informatica y de sistemas

print("=================================================================")
print("   sustraccion de matrices: metodo 1 (bucles anidados)")
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

# mostramos la matriz a
print("\nmatriz a (minuendo):")
for i in range(filas):
    for j in range(columnas):
        print(matriz_a[i][j], end="\t")
    print()

# mostramos la matriz b
print("\nmatriz b (sustraendo):")
for i in range(filas):
    for j in range(columnas):
        print(matriz_b[i][j], end="\t")
    print()

# hacemos la resta paso a paso celda por celda con bucles for
print("\nproceso paso a paso (c = a - b):")
matriz_c = []
for i in range(filas):
    fila_resultado = []
    for j in range(columnas):
        # restamos celda por celda
        resta = matriz_a[i][j] - matriz_b[i][j]
        fila_resultado.append(resta)
        # mostramos la operacion de esta celda
        print(f"c[{i + 1}][{j + 1}] = {matriz_a[i][j]} - {matriz_b[i][j]} = {resta}")
    matriz_c.append(fila_resultado)

# mostramos la matriz resultante c
print("\nmatriz resultante c:")
for i in range(filas):
    for j in range(columnas):
        print(matriz_c[i][j], end="\t")
    print()

print("=================================================================")
print("programa finalizado.")
