"""
Subpaquete backend: contiene la lógica pura de cálculo matricial sin dependencias de GUI.
"""
from app.backend.metodo_bucles import restar_matrices_bucles
from app.backend.metodo_comprension import restar_matrices_comprension
from app.backend.metodo_numpy import restar_matrices_numpy
from app.backend.registro import METODOS, ETIQUETAS_METODOS, obtener_funcion_metodo

__all__ = [
    "restar_matrices_bucles",
    "restar_matrices_comprension",
    "restar_matrices_numpy",
    "METODOS",
    "ETIQUETAS_METODOS",
    "obtener_funcion_metodo",
]
