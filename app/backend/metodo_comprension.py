"""
Módulo que implementa el Método 2 de sustracción de matrices: Comprensión de listas.
Lógica pura de backend con soporte pedagógico de salidas e inputs por consola.
"""


def imprimir_matriz_consola(matriz, nombre="Matriz"):
    """
    Imprime una matriz con formato visual claro y alineado en consola.

    Parámetros:
        matriz (list[list[float|int]]): Matriz a imprimir.
        nombre (str): Nombre o etiqueta de la matriz.
    """
    filas = len(matriz)
    columnas = len(matriz[0]) if filas > 0 else 0
    print(f"{nombre} ({filas}x{columnas}):")
    for fila in matriz:
        elementos = [f"{val:8.2f}" if isinstance(val, float) else f"{val:8}" for val in fila]
        print("  [ " + " ".join(elementos) + " ]")


def pedir_matriz_consola(nombre, filas, columnas):
    """
    Solicita al usuario ingresar los elementos de una matriz celda por celda por consola,
    con validación de tipos paso a paso (modo interactivo / cachimbo).

    Parámetros:
        nombre (str): Nombre identificador de la matriz ('A' o 'B').
        filas (int): Cantidad de filas.
        columnas (int): Cantidad de columnas.

    Retorna:
        list[list[float|int]]: Matriz construida con las entradas del usuario.
    """
    print(f"\n--- Ingrese los elementos para la Matriz {nombre} ({filas}x{columnas}) ---")
    matriz = []
    for i in range(filas):
        fila = []
        for j in range(columnas):
            while True:
                try:
                    valor_str = input(f"  Ingrese elemento {nombre}[{i + 1}][{j + 1}]: ").strip()
                    if "." in valor_str:
                        valor = float(valor_str)
                    else:
                        valor = int(valor_str)
                    fila.append(valor)
                    break
                except ValueError:
                    print("    [!] Entrada inválida. Ingrese un valor numérico (ej. 5 o 3.14).")
        matriz.append(fila)
    return matriz


def restar_matrices_comprension(matriz_a, matriz_b):
    """
    Resta la matriz B a la matriz A utilizando comprensión de listas (list comprehension).

    Efectúa la misma operación matemática que los bucles for tradicionales, pero
    sintetizada en una única expresión compacta e idiomática de Python.
    Imprime en consola la traza pedagógica del cómputo.

    Parámetros:
        matriz_a (list[list[float|int]]): Matriz minuendo (A).
        matriz_b (list[list[float|int]]): Matriz sustraendo (B). Debe tener las
                                         mismas dimensiones que la matriz A.

    Retorna:
        list[list[float]]: Nueva matriz con la diferencia resultante (A - B).

    Lanza:
        ValueError: Si las matrices están vacías o no poseen las mismas dimensiones.
    """
    if not matriz_a or not matriz_b:
        raise ValueError("Las matrices no pueden estar vacías.")

    filas_a = len(matriz_a)
    columnas_a = len(matriz_a[0])
    filas_b = len(matriz_b)
    columnas_b = len(matriz_b[0])

    if filas_a != filas_b or columnas_a != columnas_b:
        raise ValueError(
            f"Dimensiones incompatibles: Matriz A ({filas_a}x{columnas_a}) "
            f"vs Matriz B ({filas_b}x{columnas_b})."
        )

    # --- SALIDAS EN CONSOLA (TRAZA PEDAGÓGICA) ---
    print("\n" + "=" * 65)
    print(" >>> [BACKEND - MÉTODO 2: COMPRENSIÓN DE LISTAS] <<<")
    print("=" * 65)
    print(f"Dimensiones validadas: {filas_a} filas x {columnas_a} columnas")
    print()
    imprimir_matriz_consola(matriz_a, "Matriz A (Minuendo)")
    print()
    imprimir_matriz_consola(matriz_b, "Matriz B (Sustraendo)")
    print("\n--- EXPRESIÓN DE COMPRENSIÓN EVALUADA ---")
    print("  Resultado = [")
    print("      [matriz_a[i][j] - matriz_b[i][j] for j in range(columnas)]")
    print("      for i in range(filas)")
    print("  ]")
    print("\n--- EVALUACIÓN FILA POR FILA ---")

    for i in range(filas_a):
        fila_a_str = [str(matriz_a[i][j]) for j in range(columnas_a)]
        fila_b_str = [str(matriz_b[i][j]) for j in range(columnas_a)]
        restas_str = [f"{matriz_a[i][j]} - {matriz_b[i][j]}" for j in range(columnas_a)]
        valores_res = [matriz_a[i][j] - matriz_b[i][j] for j in range(columnas_a)]
        print(f"  Fila [{i + 1}]: [{', '.join(fila_a_str)}] - [{', '.join(fila_b_str)}]")
        print(f"           = [{', '.join(restas_str)}]")
        print(f"           => {valores_res}")

    matriz_resultado = [
        [
            matriz_a[indice_fila][indice_columna] - matriz_b[indice_fila][indice_columna]
            for indice_columna in range(columnas_a)
        ]
        for indice_fila in range(filas_a)
    ]

    print("\n--- MATRIZ RESULTANTE C = A - B ---")
    imprimir_matriz_consola(matriz_resultado, "Matriz C")
    print("=" * 65 + "\n")

    return matriz_resultado


def ejecutar_modo_consola():
    """
    Ejecuta el Método 2 de forma interactiva en la terminal,
    solicitando dimensiones y elementos al usuario con inputs por consola.
    """
    print("=" * 65)
    print("   UNSAAC - INGENIERÍA INFORMÁTICA Y DE SISTEMAS")
    print("   SUSTRACCIÓN DE MATRICES: MÉTODO 2 (COMPRENSIÓN DE LISTAS)")
    print("=" * 65)
    try:
        filas = int(input("Ingrese la cantidad de filas: ").strip())
        columnas = int(input("Ingrese la cantidad de columnas: ").strip())

        if filas <= 0 or columnas <= 0:
            print("[!] Las dimensiones deben ser números enteros mayores a cero.")
            return

        matriz_a = pedir_matriz_consola("A", filas, columnas)
        matriz_b = pedir_matriz_consola("B", filas, columnas)

        resultado = restar_matrices_comprension(matriz_a, matriz_b)
        return resultado
    except ValueError:
        print("[!] Error: Debe ingresar números enteros válidos para las dimensiones.")
    except KeyboardInterrupt:
        print("\n\nOperación cancelada por el usuario.")


if __name__ == "__main__":
    ejecutar_modo_consola()
