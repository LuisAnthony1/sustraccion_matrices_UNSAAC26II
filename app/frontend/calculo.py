# modulo de calculo del frontend: algoritmos de sustraccion y formato de resultados
# funciones puras (sin tkinter) que la interfaz grafica usa para calcular c = a - b
import numpy as np


def formatear_numero(valor):
    """Formatea numeros para mostrar enteros limpios o decimales reducidos."""
    if isinstance(valor, (int, float)):
        if float(valor).is_integer():
            return str(int(valor))
        return f"{valor:.4g}"
    return str(valor)


def validar_dimensiones(matriz_a, matriz_b):
    """Comprueba que a y b no esten vacias y tengan la misma dimension."""
    if not matriz_a or not matriz_a[0]:
        raise ValueError("Las matrices no pueden estar vacías.")
    filas = len(matriz_a)
    columnas = len(matriz_a[0])
    if len(matriz_b) != filas or any(len(fila) != columnas for fila in matriz_a + matriz_b):
        raise ValueError("Las matrices A y B deben tener la misma dimensión.")
    return filas, columnas


# metodo 1: bucles for anidados
def restar_matrices_bucles(matriz_a, matriz_b):
    filas, columnas = validar_dimensiones(matriz_a, matriz_b)
    resultado = []
    for i in range(filas):
        fila = []
        for j in range(columnas):
            fila.append(matriz_a[i][j] - matriz_b[i][j])
        resultado.append(fila)
    return resultado


# metodo 2: comprension de listas
def restar_matrices_comprension(matriz_a, matriz_b):
    filas, columnas = validar_dimensiones(matriz_a, matriz_b)
    return [
        [matriz_a[i][j] - matriz_b[i][j] for j in range(columnas)]
        for i in range(filas)
    ]


# metodo 3: vectorizacion con numpy
def restar_matrices_numpy(matriz_a, matriz_b):
    validar_dimensiones(matriz_a, matriz_b)
    arreglo_a = np.array(matriz_a, dtype=float)
    arreglo_b = np.array(matriz_b, dtype=float)
    return (arreglo_a - arreglo_b).tolist()


# registro de metodos: clave del radiobutton -> funcion de calculo
METODOS = {
    "bucles": restar_matrices_bucles,
    "comprension": restar_matrices_comprension,
    "numpy": restar_matrices_numpy,
}


def calcular_resta_metodo(matriz_a, matriz_b, metodo):
    """Resta a - b con el metodo indicado; usa bucles si la clave no existe."""
    funcion = METODOS.get(metodo, restar_matrices_bucles)
    return funcion(matriz_a, matriz_b)


def generar_paso_a_paso(matriz_a, matriz_b, matriz_c):
    """Devuelve una linea 'C[i,j] = a - b = c' por cada posicion de la matriz."""
    lineas = []
    for i, fila_c in enumerate(matriz_c):
        for j, valor_c in enumerate(fila_c):
            val_a = formatear_numero(matriz_a[i][j])
            val_b = formatear_numero(matriz_b[i][j])
            signo_b = f"({val_b})" if matriz_b[i][j] < 0 else val_b
            lineas.append(f"C[{i + 1},{j + 1}] = {val_a} - {signo_b} = {formatear_numero(valor_c)}")
    return lineas


def formatear_matriz_texto(matriz, separador="   ", ancho=7):
    """Convierte una matriz en texto con columnas alineadas a la derecha."""
    return "\n".join(
        separador.join(f"{formatear_numero(valor):>{ancho}}" for valor in fila)
        for fila in matriz
    )


def matriz_a_tsv(matriz):
    """Convierte una matriz en texto separado por tabulaciones (pegable en excel)."""
    return "\n".join("\t".join(formatear_numero(valor) for valor in fila) for fila in matriz)
