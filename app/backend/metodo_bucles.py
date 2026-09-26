"""
Módulo que implementa el Método 1 de sustracción de matrices: Bucles anidados.
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

    # Calcular ancho dinámico compacto según el número más largo
    if filas > 0 and columnas > 0:
        ancho_max = max(len(formatear(val)) for fila in matriz for val in fila)
    else:
        ancho_max = 1

    ancho = max(ancho_max, 2)
    for fila in matriz:
        elementos = [f"{formatear(val):>{ancho}}" for val in fila]
        print("  [ " + "  ".join(elementos) + " ]")


def pedir_dimension_consola(nombre_dimension):
    """
    Solicita en un bucle permanente una dimensión (filas o columnas) hasta que
    el usuario ingrese un número entero estrictamente positivo (> 0).

    Parámetros:
        nombre_dimension (str): Nombre de la dimensión ('filas' o 'columnas').

    Retorna:
        int: Número entero positivo validado.
    """
    while True:
        try:
            entrada = input(f"Ingrese la cantidad de {nombre_dimension}: ").strip()
            valor = int(entrada)
            if valor > 0:
                return valor
            print(f"  [!] La cantidad de {nombre_dimension} debe ser mayor a cero.")
        except ValueError:
            print("  [!] Entrada inválida. Ingrese un número entero.")


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
                    # Convertir a int si es entero exacto, o float si tiene decimales
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


def restar_matrices_bucles(matriz_a, matriz_b):
    """
    Resta la matriz B a la matriz A utilizando bucles 'for' tradicionales anidados.
    
    Es el método más explícito y pedagógico: se visita celda por celda recorriendo
    la estructura fila por fila y columna por columna.
    Imprime en consola la traza pedagógica paso a paso del cómputo.

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
    print("\n=== PROCESO PASO A PASO: C[i][j] = A[i][j] - B[i][j] ===")

    matriz_resultado = []

    for indice_fila in range(filas_a):
        fila_actual = []
        for indice_columna in range(columnas_a):
            elemento_a = matriz_a[indice_fila][indice_columna]
            elemento_b = matriz_b[indice_fila][indice_columna]
            diferencia = elemento_a - elemento_b
            fila_actual.append(diferencia)
            print(
                f"  Celda [{indice_fila + 1}][{indice_columna + 1}]: "
                f"A[{indice_fila + 1}][{indice_columna + 1}] ({elemento_a}) - "
                f"B[{indice_fila + 1}][{indice_columna + 1}] ({elemento_b}) = {diferencia}"
            )
        matriz_resultado.append(fila_actual)

    print("\n=== MATRIZ RESULTANTE C = A - B ===")
    imprimir_matriz_consola(matriz_resultado, "Matriz C")
    print("=" * 65 + "\n")

    return matriz_resultado


def ejecutar_modo_consola():
    """
    Ejecuta el Método 1 de forma interactiva en la terminal en un bucle permanente,
    solicitando dimensiones y elementos al usuario con inputs validados.
    """
    print("=" * 65)
    print("   UNSAAC - INGENIERÍA INFORMÁTICA Y DE SISTEMAS")
    print("   SUSTRACCIÓN DE MATRICES: MÉTODO 1 (BUCLES ANIDADOS)")
    print("=" * 65)
    while True:
        try:
            filas = pedir_dimension_consola("filas")
            columnas = pedir_dimension_consola("columnas")

            matriz_a = pedir_matriz_consola("A", filas, columnas)
            matriz_b = pedir_matriz_consola("B", filas, columnas)

            restar_matrices_bucles(matriz_a, matriz_b)

            continuar = input("¿Desea realizar otra operación? (s/n): ").strip().lower()
            if continuar not in ("s", "si", "sí", "y", "yes"):
                print("Saliendo del programa...")
                break
            print("\n" + "=" * 65 + "\n")
        except KeyboardInterrupt:
            print("\n\nOperación cancelada por el usuario.")
            break


if __name__ == "__main__":
    ejecutar_modo_consola()
