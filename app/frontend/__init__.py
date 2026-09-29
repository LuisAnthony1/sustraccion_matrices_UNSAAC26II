# subpaquete frontend: interfaz grafica de usuario construida en tkinter
from app.frontend.ventana_principal import AplicacionRestaMatrices
from app.frontend.widgets_matriz import (
    PALETAS,
    CuadriculaMatriz,
    calcular_resta_metodo,
    dibujar_entradas_matriz,
    extraer_matriz_numerica,
    formatear_matriz_texto,
    formatear_numero,
    generar_paso_a_paso,
)

__all__ = [
    "AplicacionRestaMatrices",
    "CuadriculaMatriz",
    "PALETAS",
    "calcular_resta_metodo",
    "dibujar_entradas_matriz",
    "extraer_matriz_numerica",
    "formatear_matriz_texto",
    "formatear_numero",
    "generar_paso_a_paso",
]
