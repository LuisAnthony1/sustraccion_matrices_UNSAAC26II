"""
Módulo que implementa el Método 2 de sustracción de matrices: Comprensión de listas.
Lógica pura de backend con soporte pedagógico de salidas e inputs por consola.
"""


def imprimir_matriz_consola(matriz, nombre="Matriz"):
    """
    Imprime una matriz con formato visual compacto y alineado en consola.

    Parámetros:
        matriz (list[list[float|int]]): Matriz a imprimir.
        nombre (str): Nombre o etiqueta de la matriz.
    """
    filas = len(matriz)
    columnas = len(matriz[0]) if filas > 0 else 0
    print(f"{nombre} ({filas}x{columnas}):")

    def formatear(val):
        if isinstance(val, float):
            return f"{val:.2f}".rstrip("0").rstrip(".") if val.is_integer() else f"{val:.2f}"
        return str(val)

    if filas > 0 and columnas > 0:
        ancho_max = max(len(formatear(val)) for fila in matriz for val in fila)
    else:
        ancho_max = 1

    ancho = max(ancho_max, 2)
    for fila in matriz:
        elementos = [f"{formatear(val):>{ancho}}" for val in fila]
        print("  [ " + "  ".join(elementos) + " ]")


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
    print(f"\n=== Ingrese los elementos para la Matriz {nombre} ({filas}x{columnas}) ===")
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
                    print("    [!] Entrada inválida. Ingrese un valor numérico.")
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
    print(f"\nDimensiones validadas: {filas_a} filas x {columnas_a} columnas\n")
    imprimir_matriz_consola(matriz_a, "Matriz A (Minuendo)")
    print()
    imprimir_matriz_consola(matriz_b, "Matriz B (Sustraendo)")
    print("\n=== EVALUACIÓN FILA POR FILA ===")

    ancho_fila = len(str(filas_a))
    for i in range(filas_a):
        prefijo = f"  Fila [{i + 1:>{ancho_fila}}]: "
        longitud_prefijo = len(prefijo)
        espacio_igual = " " * (longitud_prefijo - 2) + "= "
        espacio_flecha = " " * (longitud_prefijo - 3) + "=> "

        fila_a_str = [str(matriz_a[i][j]) for j in range(columnas_a)]
        fila_b_str = [str(matriz_b[i][j]) for j in range(columnas_a)]
        restas_str = [f"{matriz_a[i][j]} - {matriz_b[i][j]}" for j in range(columnas_a)]
        valores_res = [str(matriz_a[i][j] - matriz_b[i][j]) for j in range(columnas_a)]

        print(f"{prefijo}[{', '.join(fila_a_str)}] - [{', '.join(fila_b_str)}]")
        print(f"{espacio_igual}[{', '.join(restas_str)}]")
        print(f"{espacio_flecha}[{', '.join(valores_res)}]")

    matriz_resultado = [
        [
            matriz_a[indice_fila][indice_columna] - matriz_b[indice_fila][indice_columna]
            for indice_columna in range(columnas_a)
        ]
        for indice_fila in range(filas_a)
    ]

    print("\n=== MATRIZ RESULTANTE C = A - B ===")
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
