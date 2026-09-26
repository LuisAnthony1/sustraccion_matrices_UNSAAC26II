# modulo de componentes graficos reutilizables para matrices en tkinter
# contiene las funciones encargadas de construir poblar y leer casillas de entrada entry
import tkinter as tk

# funcion para dibujar la cuadricula de casillas de entrada de una matriz
def dibujar_entradas_matriz(
    contenedor,
    titulo,
    filas,
    columnas,
    columna_inicio=0,
    ancho_celda=6,
    color_titulo="#263238",
):
    # creacion de la etiqueta de titulo superior para la matriz
    etiqueta_titulo = tk.Label(
        contenedor,
        text=titulo,
        font=("Arial", 10, "bold"),
        fg=color_titulo,
        pady=4,
    )
    # posicionamiento de la etiqueta usando grid abarcando todas las columnas
    etiqueta_titulo.grid(
        row=0,
        column=columna_inicio,
        columnspan=columnas,
        pady=(0, 6),
    )

    # lista bidimensional que contendra las referencias a cada casilla entry
    cuadricula_entradas = []

    # iteracion sobre las filas para generar las casillas
    for indice_fila in range(filas):
        fila_entradas = []
        # iteracion sobre las columnas de la fila actual
        for indice_columna in range(columnas):
            # creacion de la casilla de texto entry para el elemento de la matriz
            casilla = tk.Entry(
                contenedor,
                width=ancho_celda,
                justify="center",
                font=("Consolas", 10),
                relief="solid",
                borderwidth=1,
            )
            # ubicacion de la casilla en la posicion correspondiente del grid
            casilla.grid(
                row=indice_fila + 1,
                column=columna_inicio + indice_columna,
                padx=3,
                pady=3,
            )
            # insercion del valor por defecto cero
            casilla.insert(0, "0")
            # agregamos la casilla a la fila actual
            fila_entradas.append(casilla)
        # agregamos la fila completa a la cuadricula
        cuadricula_entradas.append(fila_entradas)

    # retorno de la matriz de widgets entry
    return cuadricula_entradas

# funcion para extraer los valores numericos ingresados en las casillas
def extraer_matriz_numerica(cuadricula_entradas):
    # lista que almacenara los valores numericos procesados
    matriz_numerica = []
    # recorrido por cada fila de widgets entry
    for fila_widgets in cuadricula_entradas:
        fila_valores = []
        # recorrido por cada casilla de la fila
        for celda in fila_widgets:
            # obtencion del texto ingresado sin espacios en blanco
            texto_ingresado = celda.get().strip()
            try:
                # conversion del texto a numero flotante
                valor_flotante = float(texto_ingresado)
            except ValueError:
                # lanzamiento de excepcion si el texto no es numerico
                raise ValueError(
                    f"el valor '{texto_ingresado}' no es un numero valido."
                )
            # adicion del valor numerico a la fila
            fila_valores.append(valor_flotante)
        # adicion de la fila procesada a la matriz numerica
        matriz_numerica.append(fila_valores)

    # retorno de la matriz con valores flotantes
    return matriz_numerica

# funcion para formatear la matriz numerica en texto legible
def formatear_matriz_texto(matriz):
    # lista que almacenara las lineas de texto formateadas
    lineas = []
    # recorrido de cada fila de la matriz numerica
    for fila in matriz:
        # formateo de cada numero suprimiendo decimales innecesarios
        elementos_formateados = [f"{valor:g}" for valor in fila]
        # alineacion de los elementos en columnas de 7 caracteres
        lineas.append("   ".join(f"{item:>7}" for item in elementos_formateados))
    # union de todas las lineas separadas por saltos de linea
    return "\n".join(lineas)
