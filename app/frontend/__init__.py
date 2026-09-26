"""
Subpaquete frontend: contiene la interfaz gráfica de usuario construida en Tkinter.
"""
from app.frontend.ventana_principal import AplicacionRestaMatrices
from app.frontend.widgets_matriz import (
    dibujar_entradas_matriz,
    extraer_matriz_numerica,
    formatear_matriz_texto,
)

__all__ = [
    "AplicacionRestaMatrices",
    "dibujar_entradas_matriz",
    "extraer_matriz_numerica",
    "formatear_matriz_texto",
]
