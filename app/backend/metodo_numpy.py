"""
Módulo que implementa el Método 3 de sustracción de matrices: Vectorización con NumPy.
Lógica pura de backend con soporte pedagógico de salidas e inputs por consola.
"""
import numpy as np


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


def restar_matrices_numpy(matriz_a, matriz_b):
    """
    Resta la matriz B a la matriz A mediante vectorización utilizando la biblioteca NumPy.

    En lugar de iterar explícitamente a través de bucles en el intérprete de Python,
    las matrices se transforman en arreglos multidimensionales (numpy.ndarray) y se
    aplica la sobrecarga del operador de resta (-), delegando el cómputo a código C compilado
    y altamente optimizado.
    Imprime en consola la traza pedagógica del cómputo.

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

    # --- SALIDAS EN CONSOLA (TRAZA PEDAGÓGICA) ---
    print(f"\nDimensiones validadas: {arreglo_a.shape[0]} filas x {arreglo_a.shape[1]} columnas\n")
    print(f"Tipo de datos interno: {arreglo_a.dtype}")
    print("\n=== Arreglo A (Minuendo en ndarray) ===")
    print(arreglo_a)
    print("\n=== Arreglo B (Sustraendo en ndarray) ===")
    print(arreglo_b)
    print("\n=== OPERACIÓN VECTORIZADA (C compilado / BLAS) ===")
    print("  Ejecutando expresión: arreglo_resultado = arreglo_a - arreglo_b")
    print("  (Sin bucles for en Python; operación procesada en memoria contigua en C)")

    arreglo_resultado = arreglo_a - arreglo_b

    print("\n=== ARREGLO RESULTANTE C = A - B (ndarray) ===")
    print(arreglo_resultado)
    matriz_lista = arreglo_resultado.tolist()
    print("=" * 65 + "\n")

    return matriz_lista


def ejecutar_modo_consola():
    """
    Ejecuta el Método 3 de forma interactiva en la terminal en un bucle permanente,
    solicitando dimensiones y elementos al usuario con inputs validados.
    """
    print("=" * 65)
    print("   UNSAAC - INGENIERÍA INFORMÁTICA Y DE SISTEMAS")
    print("   SUSTRACCIÓN DE MATRICES: MÉTODO 3 (VECTORIZACIÓN NUMPY)")
    print("=" * 65)
    while True:
        try:
            filas = pedir_dimension_consola("filas")
            columnas = pedir_dimension_consola("columnas")

            matriz_a = pedir_matriz_consola("A", filas, columnas)
            matriz_b = pedir_matriz_consola("B", filas, columnas)

            restar_matrices_numpy(matriz_a, matriz_b)

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
