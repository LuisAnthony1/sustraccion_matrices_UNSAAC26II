"""
Módulo de registro central de métodos de resta de matrices.
Centraliza las estrategias disponibles para permitir una selección limpia y dinámica,
e incluye un menú interactivo en consola para pruebas de backend.
"""
try:
    from app.backend.metodo_bucles import (
        restar_matrices_bucles,
        pedir_matriz_consola,
        imprimir_matriz_consola,
    )
    from app.backend.metodo_comprension import restar_matrices_comprension
    from app.backend.metodo_numpy import restar_matrices_numpy
except ImportError:
    from metodo_bucles import (
        restar_matrices_bucles,
        pedir_matriz_consola,
        imprimir_matriz_consola,
    )
    from metodo_comprension import restar_matrices_comprension
    from metodo_numpy import restar_matrices_numpy

# Diccionario principal que asocia el identificador de cada método con su función de cálculo
METODOS = {
    "bucles": restar_matrices_bucles,
    "comprension": restar_matrices_comprension,
    "numpy": restar_matrices_numpy,
}

# Etiquetas descriptivas para presentación en la interfaz de usuario
ETIQUETAS_METODOS = {
    "bucles": "1) Bucles Anidados (for)",
    "comprension": "2) Comprensión de Listas",
    "numpy": "3) Vectorización NumPy",
}


def obtener_funcion_metodo(clave_metodo):
    """
    Obtiene la función de resta asociada a la clave proporcionada.

    Parámetros:
        clave_metodo (str): Clave del método ('bucles', 'comprension', 'numpy').

    Retorna:
        callable: Función de resta correspondiente.

    Lanza:
        KeyError: Si la clave especificada no se encuentra registrada.
    """
    if clave_metodo not in METODOS:
        raise KeyError(
            f"El método '{clave_metodo}' no es válido. Opciones disponibles: {list(METODOS.keys())}"
        )
    return METODOS[clave_metodo]


def menu_consola_backend():
    """
    Menú interactivo en consola para ejecutar y comparar los métodos de backend
    con inputs directos del usuario (modo cachimbo / CLI).
    """
    print("\n" + "=" * 65)
    print("      UNSAAC - INGENIERÍA INFORMÁTICA Y DE SISTEMAS")
    print("      LABORATORIO DE SUSTRACCIÓN DE MATRICES (CLI BACKEND)")
    print("=" * 65)

    try:
        filas = int(input("Ingrese el número de filas: ").strip())
        columnas = int(input("Ingrese el número de columnas: ").strip())

        if filas <= 0 or columnas <= 0:
            print("[!] Las dimensiones deben ser números enteros mayores a cero.")
            return

        matriz_a = pedir_matriz_consola("A", filas, columnas)
        matriz_b = pedir_matriz_consola("B", filas, columnas)

        while True:
            print("\n=== SELECCIÓN DE MÉTODO ===")
            print("1. Método 1: Bucles Anidados (for tradicional)")
            print("2. Método 2: Comprensión de Listas (list comprehension)")
            print("3. Método 3: Vectorización NumPy")
            print("4. Ejecutar los 3 métodos comparativamente")
            print("5. Salir")

            opcion = input("Seleccione una opción (1-5): ").strip()

            if opcion == "1":
                restar_matrices_bucles(matriz_a, matriz_b)
            elif opcion == "2":
                restar_matrices_comprension(matriz_a, matriz_b)
            elif opcion == "3":
                restar_matrices_numpy(matriz_a, matriz_b)
            elif opcion == "4":
                print("\n" + "#" * 65)
                print(" EJECUTANDO COMPARATIVA DE LOS 3 MÉTODOS")
                print("#" * 65)
                r1 = restar_matrices_bucles(matriz_a, matriz_b)
                r2 = restar_matrices_comprension(matriz_a, matriz_b)
                r3 = restar_matrices_numpy(matriz_a, matriz_b)
                son_identicos = (r1 == r2 == r3)
                print(f"\n[Verificación] ¿Los 3 métodos producen el mismo resultado?: {son_identicos}")
            elif opcion == "5":
                print("Saliendo del modo consola...")
                break
            else:
                print("[!] Opción inválida. Elija entre 1 y 5.")
    except ValueError:
        print("[!] Entrada inválida. Ingrese valores numéricos.")
    except KeyboardInterrupt:
        print("\n\nOperación cancelada por el usuario.")


if __name__ == "__main__":
    menu_consola_backend()
