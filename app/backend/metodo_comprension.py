# sustraccion de matrices - metodo 2 con comprension de listas
# unsaac - ingenieria informatica y de sistemas

print("=================================================================")
print("   sustraccion de matrices: metodo 2 (comprension de listas)")
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

# mostramos la evaluacion fila por fila
print("\nevaluacion fila por fila:")
for i in range(filas):
    restas_fila = [f"{matriz_a[i][j]} - {matriz_b[i][j]}" for j in range(columnas)]
    resultado_fila = [matriz_a[i][j] - matriz_b[i][j] for j in range(columnas)]
    print(f"fila {i + 1}: {matriz_a[i]} - {matriz_b[i]}")
    print(f"       = [{', '.join(restas_fila)}]")
    print(f"      => {resultado_fila}")

# calculamos la matriz c usando comprension de listas
matriz_c = [
    [matriz_a[i][j] - matriz_b[i][j] for j in range(columnas)]
    for i in range(filas)
]

# mostramos la matriz resultante c
print("\nmatriz resultante c:")
for i in range(filas):
    for j in range(columnas):
        print(matriz_c[i][j], end="\t")
    print()

print("=================================================================")
print("programa finalizado.")
