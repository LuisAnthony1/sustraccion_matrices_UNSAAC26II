# metodo 1: sustraccion de matrices usando bucles anidados for
# codigo en plano sin funciones def para ejecucion directa secuencial

# bucle principal permanente para permitir repetir el calculo
while True:
    # impresion del encabezado principal en consola
    print("=" * 65)
    print("   unsaac - ingenieria informatica y de sistemas")
    print("   sustraccion de matrices: metodo 1 (bucles anidados)")
    print("=" * 65)

    # validacion permanente de la cantidad de filas
    while True:
        try:
            # lectura de la cantidad de filas ingresada por el usuario
            filas = int(input("ingrese la cantidad de filas: ").strip())
            # comprobacion de que las filas sean mayores a cero
            if filas > 0:
                break
            print("  [!] la cantidad de filas debe ser mayor a cero.")
        except ValueError:
            print("  [!] entrada invalida. ingrese un numero entero.")

    # validacion permanente de la cantidad de columnas
    while True:
        try:
            # lectura de la cantidad de columnas ingresada por el usuario
            columnas = int(input("ingrese la cantidad de columnas: ").strip())
            # comprobacion de que las columnas sean mayores a cero
            if columnas > 0:
                break
            print("  [!] la cantidad de columnas debe ser mayor a cero.")
        except ValueError:
            print("  [!] entrada invalida. ingrese un numero entero.")

    # ingreso de elementos para la matriz a celda por celda
    print(f"\n=== ingrese los elementos para la matriz a ({filas}x{columnas}) ===")
    matriz_a = []
    # recorrido por cada fila de la matriz a
    for i in range(filas):
        fila = []
        # recorrido por cada columna de la fila actual
        for j in range(columnas):
            # bucle permanente para asegurar que el elemento sea un numero valido
            while True:
                try:
                    valor_str = input(f"  ingrese elemento a[{i + 1}][{j + 1}]: ").strip()
                    # conversion a float si tiene punto decimal o int si es entero
                    if "." in valor_str:
                        valor = float(valor_str)
                    else:
                        valor = int(valor_str)
                    fila.append(valor)
                    break
                except ValueError:
                    print("    [!] entrada invalida. ingrese un valor numerico.")
        matriz_a.append(fila)

    # ingreso de elementos para la matriz b celda por celda
    print(f"\n=== ingrese los elementos para la matriz b ({filas}x{columnas}) ===")
    matriz_b = []
    # recorrido por cada fila de la matriz b
    for i in range(filas):
        fila = []
        # recorrido por cada columna de la fila actual
        for j in range(columnas):
            # bucle permanente para asegurar que el elemento sea un numero valido
            while True:
                try:
                    valor_str = input(f"  ingrese elemento b[{i + 1}][{j + 1}]: ").strip()
                    # conversion a float si tiene punto decimal o int si es entero
                    if "." in valor_str:
                        valor = float(valor_str)
                    else:
                        valor = int(valor_str)
                    fila.append(valor)
                    break
                except ValueError:
                    print("    [!] entrada invalida. ingrese un valor numerico.")
        matriz_b.append(fila)

    # calculo de ancho dinamico para impresion compacta de las matrices ingresadas
    todos_los_valores = [str(val) for f in matriz_a + matriz_b for val in f]
    ancho_columna = max(max(len(v) for v in todos_los_valores), 2)

    # impresion compacta de la matriz a
    print(f"\nmatriz a (minuendo) ({filas}x{columnas}):")
    for f in matriz_a:
        fila_formato = [f"{str(v):>{ancho_columna}}" for v in f]
        print("  [ " + "  ".join(fila_formato) + " ]")

    # impresion compacta de la matriz b
    print(f"\nmatriz b (sustraendo) ({filas}x{columnas}):")
    for f in matriz_b:
        fila_formato = [f"{str(v):>{ancho_columna}}" for v in f]
        print("  [ " + "  ".join(fila_formato) + " ]")

    # proceso de sustraccion paso a paso usando bucles for anidados
    print("\n=== proceso paso a paso: c[i][j] = a[i][j] - b[i][j] ===")
    matriz_c = []
    # bucle for externo que recorre los indices de fila
    for i in range(filas):
        fila_resultado = []
        # bucle for interno que recorre los indices de columna
        for j in range(columnas):
            # obtencion de elementos correspondientes en a y b
            val_a = matriz_a[i][j]
            val_b = matriz_b[i][j]
            # calculo de la diferencia directa entre celdas
            resta = val_a - val_b
            fila_resultado.append(resta)
            # impresion explicativa del calculo de esta celda
            print(f"  celda [{i + 1}][{j + 1}]: a[{i + 1}][{j + 1}] ({val_a}) - b[{i + 1}][{j + 1}] ({val_b}) = {resta}")
        matriz_c.append(fila_resultado)

    # calculo del ancho maximo para la matriz c resultante
    ancho_c = max(max(len(str(v)) for f in matriz_c for v in f), 2)

    # impresion de la matriz c diferencia resultante
    print("\n=== matriz resultante c = a - b ===")
    print(f"matriz c ({filas}x{columnas}):")
    for f in matriz_c:
        fila_formato = [f"{str(v):>{ancho_c}}" for v in f]
        print("  [ " + "  ".join(fila_formato) + " ]")
    print("=" * 65 + "\n")

    # verificacion para continuar con otra operacion o terminar el programa
    continuar = input("¿desea realizar otra operacion? (s/n): ").strip().lower()
    if continuar not in ("s", "si", "sí", "y", "yes"):
        print("saliendo del programa...")
        break
    print("\n" + "=" * 65 + "\n")
