"""
Módulo que implementa el Método 3 de sustracción de matrices: Vectorización con NumPy.
Lógica pura de backend sin dependencias de interfaz gráfica.
"""
import numpy as np


def restar_matrices_numpy(matriz_a, matriz_b):
    """
    Resta la matriz B a la matriz A mediante vectorización utilizando la biblioteca NumPy.

    En lugar de iterar explícitamente a través de bucles en el intérprete de Python,
    las matrices se transforman en arreglos multidimensionales (numpy.ndarray) y se
    aplica la sobrecarga del operador de resta (-), delegando el cómputo a código C compilado
    y altamente optimizado.

    Parámetros:
        matriz_a (list[list[float|int]]): Matriz minuendo (A).
        matriz_b (list[list[float|int]]): Matriz sustraendo (B). Debe tener las
                                         mismas dimensiones que la matriz A.

    Retorna:
        list[list[float]]: Matriz con la diferencia (A - B) convertida de nuevo
                           a listas anidadas estándar de Python.

    Lanza:
        ValueError: Si las matrices están vacías o no poseen las mismas dimensiones.
    """
    if not matriz_a or not matriz_b:
        raise ValueError("Las matrices no pueden estar vacías.")

    arreglo_a = np.array(matriz_a, dtype=float)
    arreglo_b = np.array(matriz_b, dtype=float)

    if arreglo_a.shape != arreglo_b.shape:
        raise ValueError(
            f"Dimensiones incompatibles: Matriz A {arreglo_a.shape} "
            f"vs Matriz B {arreglo_b.shape}."
        )

    arreglo_resultado = arreglo_a - arreglo_b

    return arreglo_resultado.tolist()
