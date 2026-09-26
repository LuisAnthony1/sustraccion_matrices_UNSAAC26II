# registro unificado de metodos de sustraccion de matrices
# codigo en plano sin funciones def para ejecucion directa en consola
# unifica los 3 metodos (bucles, comprension, numpy) con seleccion interactiva

# importacion de numpy para el metodo 3 vectorizado
import numpy as np

# bucle principal permanente para permitir repetir el calculo
while True:
    # impresion del encabezado principal en consola
    print("=" * 65)
    print("   unsaac - ingenieria informatica y de sistemas")
    print("   laboratorio de sustraccion de matrices: registro unificado")
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

    # bucle del menu de seleccion de metodo para las matrices ingresadas
    while True:
        # visualizacion del menu de opciones disponibles
        print("\n=== seleccion de metodo ===")
        print("1. metodo 1: bucles anidados (for tradicional)")
        print("2. metodo 2: comprension de listas (list comprehension)")
        print("3. metodo 3: vectorizacion numpy")
        print("4. ejecutar los 3 metodos comparativamente")
        print("5. ingresar nuevas matrices")
        print("6. salir")

        opcion = input("seleccione una opcion (1-6): ").strip()

        # calculo de ancho para impresion compacta de las matrices ingresadas
        todos_los_valores = [str(val) for f in matriz_a + matriz_b for val in f]
        ancho_columna = max(max(len(v) for v in todos_los_valores), 2)

        # opcion 1: metodo de bucles for tradicionales
        if opcion == "1":
            print(f"\nmatriz a (minuendo) ({filas}x{columnas}):")
            for f in matriz_a:
                print("  [ " + "  ".join(f"{str(v):>{ancho_columna}}" for v in f) + " ]")

            print(f"\nmatriz b (sustraendo) ({filas}x{columnas}):")
            for f in matriz_b:
                print("  [ " + "  ".join(f"{str(v):>{ancho_columna}}" for v in f) + " ]")

            print("\n=== proceso paso a paso: c[i][j] = a[i][j] - b[i][j] ===")
            matriz_c = []
            for i in range(filas):
                fila_res = []
                for j in range(columnas):
                    va = matriz_a[i][j]
                    vb = matriz_b[i][j]
                    r = va - vb
                    fila_res.append(r)
                    print(f"  celda [{i + 1}][{j + 1}]: a[{i + 1}][{j + 1}] ({va}) - b[{i + 1}][{j + 1}] ({vb}) = {r}")
                matriz_c.append(fila_res)

            ancho_c = max(max(len(str(v)) for f in matriz_c for v in f), 2)
            print("\n=== matriz resultante c = a - b ===")
            print(f"matriz c ({filas}x{columnas}):")
            for f in matriz_c:
                print("  [ " + "  ".join(f"{str(v):>{ancho_c}}" for v in f) + " ]")
            print("=" * 65)

        # opcion 2: metodo de comprension de listas
        elif opcion == "2":
            print(f"\nmatriz a (minuendo) ({filas}x{columnas}):")
            for f in matriz_a:
                print("  [ " + "  ".join(f"{str(v):>{ancho_columna}}" for v in f) + " ]")

            print(f"\nmatriz b (sustraendo) ({filas}x{columnas}):")
            for f in matriz_b:
                print("  [ " + "  ".join(f"{str(v):>{ancho_columna}}" for v in f) + " ]")

            print("\n=== evaluacion fila por fila ===")
            ancho_indice = len(str(filas))
            for i in range(filas):
                prefijo = f"  fila [{i + 1:>{ancho_indice}}]: "
                long_p = len(prefijo)
                esp_ig = " " * (long_p - 2) + "= "
                esp_fl = " " * (long_p - 3) + "=> "

                fa_str = [str(matriz_a[i][j]) for j in range(columnas)]
                fb_str = [str(matriz_b[i][j]) for j in range(columnas)]
                fr_str = [f"{matriz_a[i][j]} - {matriz_b[i][j]}" for j in range(columnas)]
                fv_str = [str(matriz_a[i][j] - matriz_b[i][j]) for j in range(columnas)]

                print(f"{prefijo}[{', '.join(fa_str)}] - [{', '.join(fb_str)}]")
                print(f"{esp_ig}[{', '.join(fr_str)}]")
                print(f"{esp_fl}[{', '.join(fv_str)}]")

            matriz_c = [
                [matriz_a[i][j] - matriz_b[i][j] for j in range(columnas)]
                for i in range(filas)
            ]
            ancho_c = max(max(len(str(v)) for f in matriz_c for v in f), 2)
            print("\n=== matriz resultante c = a - b ===")
            print(f"matriz c ({filas}x{columnas}):")
            for f in matriz_c:
                print("  [ " + "  ".join(f"{str(v):>{ancho_c}}" for v in f) + " ]")
            print("=" * 65)

        # opcion 3: metodo de vectorizacion numpy
        elif opcion == "3":
            arreglo_a = np.array(matriz_a, dtype=float)
            arreglo_b = np.array(matriz_b, dtype=float)

            print(f"\ndimensiones validadas: {arreglo_a.shape[0]} filas x {arreglo_a.shape[1]} columnas\n")
            print(f"tipo de datos interno: {arreglo_a.dtype}")
            print("\n=== arreglo a (minuendo en ndarray) ===")
            print(arreglo_a)
            print("\n=== arreglo b (sustraendo en ndarray) ===")
            print(arreglo_b)
            print("\n=== operacion vectorizada (c compilado / blas) ===")
            print("  ejecutando expresion: arreglo_resultado = arreglo_a - arreglo_b")
            print("  (sin bucles for en python; operacion procesada en memoria contigua en c)")
            arreglo_resultado = arreglo_a - arreglo_b
            print("\n=== arreglo resultante c = a - b (ndarray) ===")
            print(arreglo_resultado)
            print("=" * 65)

        # opcion 4: comparativa de los 3 metodos
        elif opcion == "4":
            print("\n" + "#" * 65)
            print(" ejecutando comparativa de los 3 metodos")
            print("#" * 65)

            # calculo por bucles
            res_bucles = []
            for i in range(filas):
                fila_res = []
                for j in range(columnas):
                    fila_res.append(matriz_a[i][j] - matriz_b[i][j])
                res_bucles.append(fila_res)

            # calculo por comprension
            res_comprension = [
                [matriz_a[i][j] - matriz_b[i][j] for j in range(columnas)]
                for i in range(filas)
            ]

            # calculo por numpy
            arr_a = np.array(matriz_a, dtype=float)
            arr_b = np.array(matriz_b, dtype=float)
            res_numpy = (arr_a - arr_b).tolist()

            # verificacion de igualdad de resultados
            son_iguales = (res_bucles == res_comprension)
            print(f"\nresultado bucles:      {res_bucles}")
            print(f"resultado comprension: {res_comprension}")
            print(f"resultado numpy:       {res_numpy}")
            print(f"\n[verificacion] ¿los metodos producen el mismo resultado?: {son_iguales}")
            print("=" * 65)

        # opcion 5: volver a ingresar matrices
        elif opcion == "5":
            break

        # opcion 6: salir completamente del programa
        elif opcion == "6":
            print("saliendo del modo consola...")
            exit()

        else:
            print("[!] opcion invalida. elija entre 1 y 6.")
