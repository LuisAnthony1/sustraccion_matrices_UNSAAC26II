# modulo de la ventana principal de la aplicacion en tkinter
# orquesta la interfaz de usuario la captura de entradas y la ejecucion matricial
import tkinter as tk
from tkinter import messagebox
import numpy as np

# importacion de funciones auxiliares graficas
from app.frontend.widgets_matriz import (
    dibujar_entradas_matriz,
    extraer_matriz_numerica,
    formatear_matriz_texto,
)

# etiquetas descriptivas de los metodos de calculo
etiquetas_metodos = {
    "bucles": "1) bucles anidados (for)",
    "comprension": "2) comprension de listas",
    "numpy": "3) vectorizacion numpy",
}

# clase controladora de la interfaz grafica
class AplicacionRestaMatrices:
    # constructor que inicializa la ventana y los contenedores
    def __init__(self, ventana_raiz):
        # referencia a la ventana principal
        self.ventana_raiz = ventana_raiz
        self.ventana_raiz.title("sustraccion de matrices — 2×2 / 3×3 / n×n (3 metodos)")
        self.ventana_raiz.resizable(True, True)
        self.ventana_raiz.configure(bg="#f4f6f8")

        # variables de control para tamano y metodo seleccionado
        self.variable_tamano = tk.IntVar(value=2)
        self.variable_metodo = tk.StringVar(value="bucles")
        self.tamano_actual = 2

        # listas para almacenar las referencias a las casillas de entrada
        self.entradas_matriz_a = []
        self.entradas_matriz_b = []

        # marco superior para la cabecera
        self.marco_cabecera = tk.Frame(ventana_raiz, bg="#263238", padx=14, pady=10)
        self.marco_cabecera.pack(fill="x")

        # marco para los controles de seleccion de tamano y metodo
        self.marco_menu = tk.Frame(ventana_raiz, bg="#ffffff", padx=16, pady=12, relief="ridge", bd=1)
        self.marco_menu.pack(fill="x", padx=16, pady=10)

        # marco para mostrar las cuadriculas de entrada de matrices
        self.marco_matrices = tk.Frame(ventana_raiz, bg="#ffffff", padx=16, pady=12, relief="ridge", bd=1)
        self.marco_matrices.pack(fill="both", expand=True, padx=16, pady=(0, 10))

        # marco para los botones de accion
        self.marco_acciones = tk.Frame(ventana_raiz, bg="#f4f6f8", padx=16, pady=4)
        self.marco_acciones.pack(fill="x", padx=16)

        # marco inferior para visualizar el resultado de la operacion
        self.marco_resultado = tk.Frame(ventana_raiz, bg="#ffffff", padx=16, pady=12, relief="ridge", bd=1)
        self.marco_resultado.pack(fill="x", padx=16, pady=10)

        # llamadas para la construccion de componentes visuales iniciales
        self._construir_cabecera()
        self._construir_menu()
        self._dibujar_campos()

    # metodo para construir el encabezado visual superior
    def _construir_cabecera(self):
        # etiqueta con el titulo principal
        etiqueta_titulo = tk.Label(
            self.marco_cabecera,
            text="sustraccion de matrices en python",
            font=("Arial", 14, "bold"),
            fg="#ffffff",
            bg="#263238",
        )
        etiqueta_titulo.pack(anchor="w")

        # etiqueta con el subtitulo explicativo
        etiqueta_subtitulo = tk.Label(
            self.marco_cabecera,
            text="calculo matricial con 3 algoritmos: bucles for, comprension de listas y vectorizacion numpy",
            font=("Arial", 9),
            fg="#b0bec5",
            bg="#263238",
        )
        etiqueta_subtitulo.pack(anchor="w")

    # metodo para construir los paneles de seleccion de dimension y metodo
    def _construir_menu(self):
        # seccion de seleccion de tamano
        etiqueta_tamano = tk.Label(
            self.marco_menu,
            text="1. tamano de matriz:",
            font=("Arial", 10, "bold"),
            bg="#ffffff",
            fg="#1a237e",
        )
        etiqueta_tamano.grid(row=0, column=0, sticky="w", padx=(0, 10), pady=4)

        # boton de opcion para matriz 2x2
        tk.Radiobutton(
            self.marco_menu,
            text="2 × 2",
            variable=self.variable_tamano,
            value=2,
            bg="#ffffff",
            font=("Arial", 9),
        ).grid(row=0, column=1, padx=6)

        # boton de opcion para matriz 3x3
        tk.Radiobutton(
            self.marco_menu,
            text="3 × 3",
            variable=self.variable_tamano,
            value=3,
            bg="#ffffff",
            font=("Arial", 9),
        ).grid(row=0, column=2, padx=6)

        # boton de opcion para matriz nxn personalizada
        tk.Radiobutton(
            self.marco_menu,
            text="n × n (personalizado):",
            variable=self.variable_tamano,
            value=-1,
            bg="#ffffff",
            font=("Arial", 9),
        ).grid(row=0, column=3, padx=6)

        # casilla de texto para ingresar n personalizado
        self.entrada_tamano_personalizado = tk.Entry(
            self.marco_menu,
            width=5,
            justify="center",
            font=("Consolas", 10),
            relief="solid",
            bd=1,
        )
        self.entrada_tamano_personalizado.grid(row=0, column=4, padx=4)

        # seccion de seleccion de metodo de calculo
        etiqueta_metodo = tk.Label(
            self.marco_menu,
            text="2. metodo de calculo:",
            font=("Arial", 10, "bold"),
            bg="#ffffff",
            fg="#1a237e",
        )
        etiqueta_metodo.grid(row=1, column=0, sticky="w", padx=(0, 10), pady=(10, 4))

        # boton de opcion para metodo 1 bucles
        tk.Radiobutton(
            self.marco_menu,
            text=etiquetas_metodos["bucles"],
            variable=self.variable_metodo,
            value="bucles",
            bg="#ffffff",
            font=("Arial", 9),
        ).grid(row=1, column=1, columnspan=2, sticky="w", padx=6)

        # boton de opcion para metodo 2 comprension
        tk.Radiobutton(
            self.marco_menu,
            text=etiquetas_metodos["comprension"],
            variable=self.variable_metodo,
            value="comprension",
            bg="#ffffff",
            font=("Arial", 9),
        ).grid(row=1, column=3, columnspan=2, sticky="w", padx=6)

        # boton de opcion para metodo 3 numpy
        tk.Radiobutton(
            self.marco_menu,
            text=etiquetas_metodos["numpy"],
            variable=self.variable_metodo,
            value="numpy",
            bg="#ffffff",
            font=("Arial", 9),
        ).grid(row=2, column=1, columnspan=2, sticky="w", padx=6, pady=(0, 4))

        # boton para regenerar las cuadriculas segun el tamano seleccionado
        boton_generar = tk.Button(
            self.marco_menu,
            text="generar cuadricula de matrices",
            bg="#0277bd",
            fg="#ffffff",
            activebackground="#01579b",
            activeforeground="#ffffff",
            font=("Arial", 9, "bold"),
            relief="flat",
            padx=12,
            pady=4,
            command=self._dibujar_campos,
            cursor="hand2",
        )
        boton_generar.grid(row=2, column=3, columnspan=2, sticky="e", pady=(4, 4))

    # metodo para obtener y validar la dimension n
    def _obtener_tamano_n(self):
        seleccion = self.variable_tamano.get()
        if seleccion == -1:
            texto_valor = self.entrada_tamano_personalizado.get().strip()
            # validacion de que la entrada contenga digitos y sea mayor a cero
            if not texto_valor.isdigit() or int(texto_valor) < 1:
                messagebox.showerror(
                    "error de dimension",
                    "por favor, ingresa un numero entero positivo para n (por ejemplo, 4 o 5).",
                )
                return None
            n_entero = int(texto_valor)
            if n_entero > 10:
                messagebox.showwarning(
                    "dimension grande",
                    "para una optima visualizacion en pantalla, se recomienda un valor de n ≤ 10.",
                )
            return n_entero
        return seleccion

    # metodo para dibujar las cuadriculas de entrada de matrices a y b
    def _dibujar_campos(self):
        # limpieza de widgets previos en el marco de matrices
        for widget in self.marco_matrices.winfo_children():
            widget.destroy()

        dimension = self._obtener_tamano_n()
        if dimension is None:
            return

        self.tamano_actual = dimension

        # marco para la matriz a
        submarco_a = tk.Frame(self.marco_matrices, bg="#ffffff")
        submarco_a.pack(side="left", padx=14, pady=6, anchor="n")

        # marco para el signo operador de resta
        submarco_operador = tk.Frame(self.marco_matrices, bg="#ffffff")
        submarco_operador.pack(side="left", padx=8, pady=30, anchor="center")

        # etiqueta con el signo menos
        etiqueta_operador = tk.Label(
            submarco_operador,
            text="−",
            font=("Arial", 24, "bold"),
            fg="#d32f2f",
            bg="#ffffff",
        )
        etiqueta_operador.pack()

        # marco para la matriz b
        submarco_b = tk.Frame(self.marco_matrices, bg="#ffffff")
        submarco_b.pack(side="left", padx=14, pady=6, anchor="n")

        # dibujo de casillas para la matriz a
        self.entradas_matriz_a = dibujar_entradas_matriz(
            contenedor=submarco_a,
            titulo="matriz minuendo (a)",
            filas=dimension,
            columnas=dimension,
            color_titulo="#1565c0",
        )

        # dibujo de casillas para la matriz b
        self.entradas_matriz_b = dibujar_entradas_matriz(
            contenedor=submarco_b,
            titulo="matriz sustraendo (b)",
            filas=dimension,
            columnas=dimension,
            color_titulo="#2e7d32",
        )

        # construccion de los botones de calculo y ejemplo
        self._construir_botones_acciones()

    # metodo para construir los botones de calcular y cargar ejemplo
    def _construir_botones_acciones(self):
        for widget in self.marco_acciones.winfo_children():
            widget.destroy()

        # boton para ejecutar el calculo de la resta
        boton_calcular = tk.Button(
            self.marco_acciones,
            text="calcular sustraccion (a − b)",
            bg="#2e7d32",
            fg="#ffffff",
            activebackground="#1b5e20",
            activeforeground="#ffffff",
            font=("Arial", 11, "bold"),
            relief="flat",
            padx=18,
            pady=6,
            command=self._calcular_resta,
            cursor="hand2",
        )
        boton_calcular.pack(side="left", padx=(0, 10))

        # boton para cargar valores de ejemplo
        boton_ejemplo = tk.Button(
            self.marco_acciones,
            text="cargar valores de ejemplo",
            bg="#455a64",
            fg="#ffffff",
            activebackground="#263238",
            activeforeground="#ffffff",
            font=("Arial", 9),
            relief="flat",
            padx=12,
            pady=6,
            command=self._cargar_valores_ejemplo,
            cursor="hand2",
        )
        boton_ejemplo.pack(side="left", padx=6)

    # metodo para llenar las entradas con datos de prueba
    def _cargar_valores_ejemplo(self):
        dimension = self.tamano_actual

        if dimension == 2:
            valores_a = [[5, 3], [2, 8]]
            valores_b = [[1, 1], [4, 2]]
        elif dimension == 3:
            valores_a = [[8, 5, 3], [4, 9, 2], [7, 6, 1]]
            valores_b = [[2, 1, 1], [3, 4, 2], [1, 2, 0]]
        else:
            valores_a = [[(i + 1) * 2 + j for j in range(dimension)] for i in range(dimension)]
            valores_b = [[(i + 1) + j for j in range(dimension)] for i in range(dimension)]

        # rellenado de las casillas con los valores de ejemplo
        for i in range(dimension):
            for j in range(dimension):
                self.entradas_matriz_a[i][j].delete(0, tk.END)
                self.entradas_matriz_a[i][j].insert(0, str(valores_a[i][j]))

                self.entradas_matriz_b[i][j].delete(0, tk.END)
                self.entradas_matriz_b[i][j].insert(0, str(valores_b[i][j]))

    # metodo para calcular la resta segun el metodo seleccionado
    def _calcular_resta(self):
        try:
            matriz_a = extraer_matriz_numerica(self.entradas_matriz_a)
            matriz_b = extraer_matriz_numerica(self.entradas_matriz_b)
        except ValueError as error_valor:
            messagebox.showerror(
                "error en entradas",
                f"error al leer las matrices:\n{error_valor}\n\nasegurate de ingresar solo numeros.",
            )
            return

        clave_metodo = self.variable_metodo.get()
        try:
            # calculo directo segun el metodo seleccionado
            if clave_metodo == "bucles":
                matriz_resultado = []
                for i in range(len(matriz_a)):
                    fila = []
                    for j in range(len(matriz_a[0])):
                        fila.append(matriz_a[i][j] - matriz_b[i][j])
                    matriz_resultado.append(fila)
            elif clave_metodo == "comprension":
                matriz_resultado = [
                    [matriz_a[i][j] - matriz_b[i][j] for j in range(len(matriz_a[0]))]
                    for i in range(len(matriz_a))
                ]
            else:
                arr_a = np.array(matriz_a, dtype=float)
                arr_b = np.array(matriz_b, dtype=float)
                matriz_resultado = (arr_a - arr_b).tolist()

        except Exception as error_calculo:
            messagebox.showerror(
                "error de calculo",
                f"ocurrio un error al calcular la resta:\n{error_calculo}",
            )
            return

        # visualizacion del resultado en pantalla
        self._mostrar_resultado(matriz_resultado, clave_metodo)

    # metodo para presentar la matriz diferencia resultante
    def _mostrar_resultado(self, matriz_resultado, clave_metodo):
        # limpieza de resultados anteriores
        for widget in self.marco_resultado.winfo_children():
            widget.destroy()

        nombre_descriptivo = etiquetas_metodos.get(clave_metodo, clave_metodo)

        # etiqueta de titulo del resultado
        etiqueta_titulo_res = tk.Label(
            self.marco_resultado,
            text="matriz diferencia resultante (c = a − b)",
            font=("Arial", 11, "bold"),
            fg="#1b5e20",
            bg="#ffffff",
        )
        etiqueta_titulo_res.pack(anchor="w", pady=(0, 4))

        # etiqueta indicando el metodo ejecutado
        etiqueta_metodo_usado = tk.Label(
            self.marco_resultado,
            text=f"metodo ejecutado: {nombre_descriptivo}",
            font=("Arial", 9, "italic"),
            fg="#546e7a",
            bg="#ffffff",
        )
        etiqueta_metodo_usado.pack(anchor="w", pady=(0, 8))

        texto_matriz = formatear_matriz_texto(matriz_resultado)

        # contenedor para la caja de texto de la matriz
        marco_caja_texto = tk.Frame(self.marco_resultado, bg="#eceff1", padx=12, pady=10, relief="sunken", bd=1)
        marco_caja_texto.pack(anchor="w")

        # etiqueta con la matriz resultante formateada en fuente monoespaciada
        etiqueta_matriz = tk.Label(
            marco_caja_texto,
            text=texto_matriz,
            font=("Consolas", 12, "bold"),
            fg="#212121",
            bg="#eceff1",
            justify="left",
        )
        etiqueta_matriz.pack()
