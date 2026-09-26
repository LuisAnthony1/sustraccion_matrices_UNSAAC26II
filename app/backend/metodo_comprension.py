"""
Módulo que implementa el Método 2 de sustracción de matrices: Comprensión de listas.
Lógica pura de backend sin dependencias de interfaz gráfica.
"""


def restar_matrices_comprension(matriz_a, matriz_b):
    """
    Resta la matriz B a la matriz A utilizando comprensión de listas (list comprehension).

    Efectúa la misma operación matemática que los bucles for tradicionales, pero
    sintetizada en una única expresión compacta e idiomática de Python.

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

    matriz_resultado = [
        [
            matriz_a[indice_fila][indice_columna] - matriz_b[indice_fila][indice_columna]
            for indice_columna in range(columnas_a)
        ]
        for indice_fila in range(filas_a)
    ]

    return matriz_resultado
