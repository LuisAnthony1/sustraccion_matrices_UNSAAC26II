"""
Módulo de componentes gráficos reutilizables para matrices en Tkinter.
Contiene las funciones encargadas de construir, poblar y leer casillas de entrada (Entry).
"""
import tkinter as tk


def dibujar_entradas_matriz(
    contenedor,
    titulo,
    filas,
    columnas,
    columna_inicio=0,
    ancho_celda=6,
    color_titulo="#263238",
):
    """
    Dibuja dinámicamente una cuadrícula de casillas (Entry) para representar una matriz.

    Parámetros:
        contenedor (tk.Widget): Marco contenedor donde se ubicarán los elementos.
        titulo (str): Encabezado superior descriptivo (por ejemplo, 'Matriz A').
        filas (int): Número de filas de la matriz.
        columnas (int): Número de columnas de la matriz.
        columna_inicio (int): Columna inicial en el grid del contenedor.
        ancho_celda (int): Ancho en caracteres de cada Entry.
        color_titulo (str): Color hexadecimal para la fuente del título.

    Retorna:
        list[list[tk.Entry]]: Matriz bidimensional de referencias a los Entry creados.
    """
    etiqueta_titulo = tk.Label(
        contenedor,
        text=titulo,
        font=("Arial", 10, "bold"),
        fg=color_titulo,
        pady=4,
    )
    etiqueta_titulo.grid(
        row=0,
        column=columna_inicio,
        columnspan=columnas,
        pady=(0, 6),
    )

    cuadricula_entradas = []

    for indice_fila in range(filas):
        fila_entradas = []
        for indice_columna in range(columnas):
            casilla = tk.Entry(
                contenedor,
                width=ancho_celda,
                justify="center",
                font=("Consolas", 10),
                relief="solid",
                borderwidth=1,
            )
            casilla.grid(
                row=indice_fila + 1,
                column=columna_inicio + indice_columna,
                padx=3,
                pady=3,
            )
            casilla.insert(0, "0")
            fila_entradas.append(casilla)
        cuadricula_entradas.append(fila_entradas)

    return cuadricula_entradas


def extraer_matriz_numerica(cuadricula_entradas):
    """
    Extrae los valores numéricos ingresados en una cuadrícula bidimensional de widgets Entry.

    Parámetros:
        cuadricula_entradas (list[list[tk.Entry]]): Matriz de widgets Entry.

    Retorna:
        list[list[float]]: Matriz con los números convertidos a punto flotante.

    Lanza:
        ValueError: Si alguna celda contiene un texto que no puede convertirse a número.
    """
    matriz_numerica = []
    for fila_widgets in cuadricula_entradas:
        fila_valores = []
        for celda in fila_widgets:
            texto_ingresado = celda.get().strip()
            try:
                valor_flotante = float(texto_ingresado)
            except ValueError:
                raise ValueError(
                    f"El valor '{texto_ingresado}' no es un número válido."
                )
            fila_valores.append(valor_flotante)
        matriz_numerica.append(fila_valores)

    return matriz_numerica


def formatear_matriz_texto(matriz):
    """
    Convierte una matriz numérica en una representación de texto alineada y legible.

    Parámetros:
        matriz (list[list[float|int]]): Matriz con valores numéricos.

    Retorna:
        str: Cadena formateada por filas.
    """
    lineas = []
    for fila in matriz:
        elementos_formateados = [f"{valor:g}" for valor in fila]
        lineas.append("   ".join(f"{item:>7}" for item in elementos_formateados))
    return "\n".join(lineas)
