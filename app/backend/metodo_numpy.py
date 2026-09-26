# metodo 3: sustraccion de matrices usando vectorizacion con numpy
# codigo en plano sin funciones def para ejecucion directa secuencial

# importacion de la biblioteca numpy para calculo matricial vectorizado
import numpy as np

# bucle principal permanente para permitir repetir el calculo
while True:
    # impresion del encabezado principal en consola
    print("=" * 65)
    print("   unsaac - ingenieria informatica y de sistemas")
    print("   sustraccion de matrices: metodo 3 (vectorizacion numpy)")
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

    # conversion de las listas estandar de python a arreglos ndarray de numpy
    arreglo_a = np.array(matriz_a, dtype=float)
    arreglo_b = np.array(matriz_b, dtype=float)

    # impresion informativa de las dimensiones y tipo de dato del arreglo
    print(f"\ndimensiones validadas: {arreglo_a.shape[0]} filas x {arreglo_a.shape[1]} columnas\n")
    print(f"tipo de datos interno: {arreglo_a.dtype}")

    # visualizacion de los arreglos en formato numpy
    print("\n=== arreglo a (minuendo en ndarray) ===")
    print(arreglo_a)
    print("\n=== arreglo b (sustraendo en ndarray) ===")
    print(arreglo_b)

    # operacion vectorizada ejecutada a bajo nivel en c compilado (simd y blas)
    print("\n=== operacion vectorizada (c compilado / blas) ===")
    print("  ejecutando expresion: arreglo_resultado = arreglo_a - arreglo_b")
    print("  (sin bucles for en python; operacion procesada en memoria contigua en c)")
    arreglo_resultado = arreglo_a - arreglo_b

    # visualizacion del arreglo resultante de la resta
    print("\n=== arreglo resultante c = a - b (ndarray) ===")
    print(arreglo_resultado)
    print("=" * 65 + "\n")

    # verificacion para continuar con otra operacion o terminar el programa
    continuar = input("¿desea realizar otra operacion? (s/n): ").strip().lower()
    if continuar not in ("s", "si", "sí", "y", "yes"):
        print("saliendo del programa...")
        break
    print("\n" + "=" * 65 + "\n")
