"""
Módulo de registro central de métodos de resta de matrices.
Centraliza las estrategias disponibles para permitir una selección limpia y dinámica.
"""
from app.backend.metodo_bucles import restar_matrices_bucles
from app.backend.metodo_comprension import restar_matrices_comprension
from app.backend.metodo_numpy import restar_matrices_numpy

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
