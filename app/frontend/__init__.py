# subpaquete frontend: interfaz grafica de usuario construida en tkinter
from app.frontend.calculo import (
    METODOS,
    calcular_resta_metodo,
    formatear_matriz_texto,
    formatear_numero,
    generar_paso_a_paso,
)
from app.frontend.ventana_principal import AplicacionRestaMatrices
from app.frontend.widgets_matriz import (
    PALETAS,
    CajaDesplazable,
    CuadriculaMatriz,
    dibujar_entradas_matriz,
    extraer_matriz_numerica,
)

__all__ = [
    "AplicacionRestaMatrices",
    "CajaDesplazable",
    "CuadriculaMatriz",
    "METODOS",
    "PALETAS",
    "calcular_resta_metodo",
    "dibujar_entradas_matriz",
    "extraer_matriz_numerica",
    "formatear_matriz_texto",
    "formatear_numero",
    "generar_paso_a_paso",
]
