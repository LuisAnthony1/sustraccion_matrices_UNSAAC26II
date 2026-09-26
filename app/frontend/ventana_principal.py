"""
Módulo de la ventana principal de la aplicación en Tkinter.
Contiene la clase AplicacionRestaMatrices que orquesta la interfaz de usuario,
la captura de entradas y la invocación de la lógica de backend.
"""
import tkinter as tk
from tkinter import messagebox

from app.backend.registro import METODOS, ETIQUETAS_METODOS, obtener_funcion_metodo
from app.frontend.widgets_matriz import (
    dibujar_entradas_matriz,
    extraer_matriz_numerica,
    formatear_matriz_texto,
)


class AplicacionRestaMatrices:
    """
    Controlador de la interfaz gráfica para la sustracción de matrices.
    Permite seleccionar dimensiones (2x2, 3x3, NxN), método de cómputo,
    ingresar valores numéricos y visualizar la matriz diferencia resultante.
    """

    def __init__(self, ventana_raiz):
        """
        Inicializa la ventana principal y los componentes visuales.

        Parámetros:
            ventana_raiz (tk.Tk): Ventana raíz de Tkinter.
        """
        self.ventana_raiz = ventana_raiz
        self.ventana_raiz.title("Sustracción de Matrices — 2×2 / 3×3 / N×N (3 Métodos)")
        self.ventana_raiz.resizable(True, True)
        self.ventana_raiz.configure(bg="#f4f6f8")

        # Variables de estado enlazadas a los controles
        self.variable_tamano = tk.IntVar(value=2)
        self.variable_metodo = tk.StringVar(value="bucles")
        self.tamano_actual = 2

        self.entradas_matriz_a = []
        self.entradas_matriz_b = []

        # Contenedores principales organizados verticalmente
        self.marco_cabecera = tk.Frame(ventana_raiz, bg="#263238", padx=14, pady=10)
        self.marco_cabecera.pack(fill="x")

        self.marco_menu = tk.Frame(ventana_raiz, bg="#ffffff", padx=16, pady=12, relief="ridge", bd=1)
        self.marco_menu.pack(fill="x", padx=16, pady=10)

        self.marco_matrices = tk.Frame(ventana_raiz, bg="#ffffff", padx=16, pady=12, relief="ridge", bd=1)
        self.marco_matrices.pack(fill="both", expand=True, padx=16, pady=(0, 10))

        self.marco_acciones = tk.Frame(ventana_raiz, bg="#f4f6f8", padx=16, pady=4)
        self.marco_acciones.pack(fill="x", padx=16)

        self.marco_resultado = tk.Frame(ventana_raiz, bg="#ffffff", padx=16, pady=12, relief="ridge", bd=1)
        self.marco_resultado.pack(fill="x", padx=16, pady=10)

        # Construcción inicial
        self._construir_cabecera()
        self._construir_menu()
        self._dibujar_campos()

    def _construir_cabecera(self):
        """Dibuja el título superior y subtítulo informativo."""
        etiqueta_titulo = tk.Label(
            self.marco_cabecera,
            text="Sustracción de Matrices en Python",
            font=("Arial", 14, "bold"),
            fg="#ffffff",
            bg="#263238",
        )
        etiqueta_titulo.pack(anchor="w")

        etiqueta_subtitulo = tk.Label(
            self.marco_cabecera,
            text="Cálculo matricial con 3 algoritmos: Bucles For, Comprensión de Listas y Vectorización NumPy",
            font=("Arial", 9),
            fg="#b0bec5",
            bg="#263238",
        )
        etiqueta_subtitulo.pack(anchor="w")

    def _construir_menu(self):
        """Construye los paneles de selección de tamaño y método de cálculo."""
        # --- Sección de Tamaño ---
        etiqueta_tamano = tk.Label(
            self.marco_menu,
            text="1. Tamaño de Matriz:",
            font=("Arial", 10, "bold"),
            bg="#ffffff",
            fg="#1a237e",
        )
        etiqueta_tamano.grid(row=0, column=0, sticky="w", padx=(0, 10), pady=4)

        tk.Radiobutton(
            self.marco_menu,
            text="2 × 2",
            variable=self.variable_tamano,
            value=2,
            bg="#ffffff",
            font=("Arial", 9),
        ).grid(row=0, column=1, padx=6)

        tk.Radiobutton(
            self.marco_menu,
            text="3 × 3",
            variable=self.variable_tamano,
            value=3,
            bg="#ffffff",
            font=("Arial", 9),
        ).grid(row=0, column=2, padx=6)

        tk.Radiobutton(
            self.marco_menu,
            text="N × N (Personalizado):",
            variable=self.variable_tamano,
            value=-1,
            bg="#ffffff",
            font=("Arial", 9),
        ).grid(row=0, column=3, padx=6)

        self.entrada_tamano_personalizado = tk.Entry(
            self.marco_menu,
            width=5,
            justify="center",
            font=("Consolas", 10),
            relief="solid",
            bd=1,
        )
        self.entrada_tamano_personalizado.grid(row=0, column=4, padx=4)

        # --- Sección de Método ---
        etiqueta_metodo = tk.Label(
            self.marco_menu,
            text="2. Método de Cálculo:",
            font=("Arial", 10, "bold"),
            bg="#ffffff",
            fg="#1a237e",
        )
        etiqueta_metodo.grid(row=1, column=0, sticky="w", padx=(0, 10), pady=(10, 4))

        tk.Radiobutton(
            self.marco_menu,
            text=ETIQUETAS_METODOS["bucles"],
            variable=self.variable_metodo,
            value="bucles",
            bg="#ffffff",
            font=("Arial", 9),
        ).grid(row=1, column=1, columnspan=2, sticky="w", padx=6)

        tk.Radiobutton(
            self.marco_menu,
            text=ETIQUETAS_METODOS["comprension"],
            variable=self.variable_metodo,
            value="comprension",
            bg="#ffffff",
            font=("Arial", 9),
        ).grid(row=1, column=3, columnspan=2, sticky="w", padx=6)

        tk.Radiobutton(
            self.marco_menu,
            text=ETIQUETAS_METODOS["numpy"],
            variable=self.variable_metodo,
            value="numpy",
            bg="#ffffff",
            font=("Arial", 9),
        ).grid(row=2, column=1, columnspan=2, sticky="w", padx=6, pady=(0, 4))

        # Botón para regenerar cuadrícula
        boton_generar = tk.Button(
            self.marco_menu,
            text="Generar Cuadrícula de Matrices",
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

    def _obtener_tamano_n(self):
        """
        Lee y valida la dimensión N solicitada por el usuario.

        Retorna:
            int | None: La dimensión N si es válida, o None si ocurrió un error.
        """
        seleccion = self.variable_tamano.get()
        if seleccion == -1:
            texto_valor = self.entrada_tamano_personalizado.get().strip()
            if not texto_valor.isdigit() or int(texto_valor) < 1:
                messagebox.showerror(
                    "Error de Dimensión",
                    "Por favor, ingresa un número entero positivo para N (por ejemplo, 4 o 5).",
                )
                return None
            n_entero = int(texto_valor)
            if n_entero > 10:
                messagebox.showwarning(
                    "Dimensión Grande",
                    "Para una óptima visualización en pantalla, se recomienda un valor de N ≤ 10.",
                )
            return n_entero
        return seleccion

    def _dibujar_campos(self):
        """Limpia y construye las cuadrículas de entrada para las matrices A y B."""
        for widget in self.marco_matrices.winfo_children():
            widget.destroy()

        dimension = self._obtener_tamano_n()
        if dimension is None:
            return

        self.tamano_actual = dimension

        # Submarcos interiores para Matriz A, Operador y Matriz B
        submarco_a = tk.Frame(self.marco_matrices, bg="#ffffff")
        submarco_a.pack(side="left", padx=14, pady=6, anchor="n")

        submarco_operador = tk.Frame(self.marco_matrices, bg="#ffffff")
        submarco_operador.pack(side="left", padx=8, pady=30, anchor="center")

        etiqueta_operador = tk.Label(
            submarco_operador,
            text="−",
            font=("Arial", 24, "bold"),
            fg="#d32f2f",
            bg="#ffffff",
        )
        etiqueta_operador.pack()

        submarco_b = tk.Frame(self.marco_matrices, bg="#ffffff")
        submarco_b.pack(side="left", padx=14, pady=6, anchor="n")

        # Dibujar casillas a través del módulo de widgets
        self.entradas_matriz_a = dibujar_entradas_matriz(
            contenedor=submarco_a,
            titulo="Matriz Minuendo (A)",
            filas=dimension,
            columnas=dimension,
            color_titulo="#1565c0",
        )

        self.entradas_matriz_b = dibujar_entradas_matriz(
            contenedor=submarco_b,
            titulo="Matriz Sustraendo (B)",
            filas=dimension,
            columnas=dimension,
            color_titulo="#2e7d32",
        )

        self._construir_botones_acciones()

    def _construir_botones_acciones(self):
        """Construye los botones de acción para calcular o limpiar."""
        for widget in self.marco_acciones.winfo_children():
            widget.destroy()

        boton_calcular = tk.Button(
            self.marco_acciones,
            text="Calcular Sustracción (A − B)",
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

        boton_ejemplo = tk.Button(
            self.marco_acciones,
            text="Cargar Valores de Ejemplo",
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

    def _cargar_valores_ejemplo(self):
        """Llena las casillas de entrada con valores de demostración."""
        dimension = self.tamano_actual

        if dimension == 2:
            # Ejemplo exacto de la guía técnica:
            # A = [[5, 3], [2, 8]], B = [[1, 1], [4, 2]]
            valores_a = [[5, 3], [2, 8]]
            valores_b = [[1, 1], [4, 2]]
        elif dimension == 3:
            valores_a = [[8, 5, 3], [4, 9, 2], [7, 6, 1]]
            valores_b = [[2, 1, 1], [3, 4, 2], [1, 2, 0]]
        else:
            valores_a = [[(i + 1) * 2 + j for j in range(dimension)] for i in range(dimension)]
            valores_b = [[(i + 1) + j for j in range(dimension)] for i in range(dimension)]

        for i in range(dimension):
            for j in range(dimension):
                self.entradas_matriz_a[i][j].delete(0, tk.END)
                self.entradas_matriz_a[i][j].insert(0, str(valores_a[i][j]))

                self.entradas_matriz_b[i][j].delete(0, tk.END)
                self.entradas_matriz_b[i][j].insert(0, str(valores_b[i][j]))

    def _calcular_resta(self):
        """Extrae los valores numéricos, llama al backend correspondiente y presenta el resultado."""
        try:
            matriz_a = extraer_matriz_numerica(self.entradas_matriz_a)
            matriz_b = extraer_matriz_numerica(self.entradas_matriz_b)
        except ValueError as error_valor:
            messagebox.showerror(
                "Error en Entradas",
                f"Error al leer las matrices:\n{error_valor}\n\nAsegúrate de ingresar solo números.",
            )
            return

        clave_metodo = self.variable_metodo.get()
        try:
            funcion_resta = obtener_funcion_metodo(clave_metodo)
            matriz_resultado = funcion_resta(matriz_a, matriz_b)
        except Exception as error_calculo:
            messagebox.showerror(
                "Error de Cálculo",
                f"Ocurrió un error al calcular la resta con el método seleccionado:\n{error_calculo}",
            )
            return

        self._mostrar_resultado(matriz_resultado, clave_metodo)

    def _mostrar_resultado(self, matriz_resultado, clave_metodo):
        """Muestra en pantalla la matriz diferencia formateada."""
        for widget in self.marco_resultado.winfo_children():
            widget.destroy()

        nombre_descriptivo = ETIQUETAS_METODOS.get(clave_metodo, clave_metodo)

        etiqueta_titulo_res = tk.Label(
            self.marco_resultado,
            text=f"Matriz Diferencia Resultante  (C = A − B)",
            font=("Arial", 11, "bold"),
            fg="#1b5e20",
            bg="#ffffff",
        )
        etiqueta_titulo_res.pack(anchor="w", pady=(0, 4))

        etiqueta_metodo_usado = tk.Label(
            self.marco_resultado,
            text=f"Método ejecutado: {nombre_descriptivo}",
            font=("Arial", 9, "italic"),
            fg="#546e7a",
            bg="#ffffff",
        )
        etiqueta_metodo_usado.pack(anchor="w", pady=(0, 8))

        texto_matriz = formatear_matriz_texto(matriz_resultado)

        marco_caja_texto = tk.Frame(self.marco_resultado, bg="#eceff1", padx=12, pady=10, relief="sunken", bd=1)
        marco_caja_texto.pack(anchor="w")

        etiqueta_matriz = tk.Label(
            marco_caja_texto,
            text=texto_matriz,
            font=("Consolas", 12, "bold"),
            fg="#212121",
            bg="#eceff1",
            justify="left",
        )
        etiqueta_matriz.pack()
