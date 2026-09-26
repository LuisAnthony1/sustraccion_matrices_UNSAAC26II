# sustraccion de matrices - metodo 1 con bucles for
# unsaac - codigo basico para consola

print("=================================================================")
print("   sustraccion de matrices: metodo 1 (bucles anidados)")
print("=================================================================")

# pedimos la cantidad de filas con condicion
filas = 0
while filas <= 0:
    try:
        filas = int(input("ingrese la cantidad de filas: "))
        if filas <= 0:
            print("la cantidad de filas debe ser mayor a 0")
    except:
        print("error, ingrese un numero entero")

# pedimos la cantidad de columnas con condicion
columnas = 0
while columnas <= 0:
    try:
        columnas = int(input("ingrese la cantidad de columnas: "))
        if columnas <= 0:
            print("la cantidad de columnas debe ser mayor a 0")
    except:
        print("error, ingrese un numero entero")

# pedimos los elementos de la matriz a
print("\ningrese los elementos de la matriz a:")
matriz_a = []
for i in range(filas):
    fila = []
    for j in range(columnas):
        # condicion para repetir solo si el valor ingresado no es float
        es_valido = False
        while es_valido == False:
            try:
                valor = float(input(f"ingrese a[{i + 1}][{j + 1}]: "))
                es_valido = True
            except:
                print("error, ingrese un numero valido")
        fila.append(valor)
    matriz_a.append(fila)

# pedimos los elementos de la matriz b
print("\ningrese los elementos de la matriz b:")
matriz_b = []
for i in range(filas):
    fila = []
    for j in range(columnas):
        # condicion para repetir solo si el valor ingresado no es float
        es_valido = False
        while es_valido == False:
            try:
                valor = float(input(f"ingrese b[{i + 1}][{j + 1}]: "))
                es_valido = True
            except:
                print("error, ingrese un numero valido")
        fila.append(valor)
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

# calculamos la resta con bucles for anidados
print("\nproceso paso a paso (c = a - b):")
matriz_c = []
for i in range(filas):
    fila_resultado = []
    for j in range(columnas):
        # restamos elemento por elemento
        resta = matriz_a[i][j] - matriz_b[i][j]
        fila_resultado.append(resta)
        # mostramos la operacion de la celda
        print(f"c[{i + 1}][{j + 1}] = {matriz_a[i][j]} - {matriz_b[i][j]} = {resta}")
    matriz_c.append(fila_resultado)

# mostramos la matriz resultado c
print("\nmatriz resultante c:")
for i in range(filas):
    for j in range(columnas):
        print(matriz_c[i][j], end="\t")
    print()

print("=================================================================")
print("programa finalizado.")
