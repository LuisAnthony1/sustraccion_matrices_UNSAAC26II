# interfaz grafica minimalista y limpia para sustraccion de matrices
# con soporte para dimensiones complejas mediante cajas desplazables (boxes movibles)
import ctypes
import tkinter as tk
from tkinter import messagebox

from app.frontend.calculo import (
    calcular_resta_metodo,
    formatear_numero,
    generar_paso_a_paso,
    matriz_a_tsv,
)
from app.frontend.widgets_matriz import (
    COLORES,
    FUENTE_MONO,
    FUENTE_SANS,
    CajaDesplazable,
    CuadriculaMatriz,
    calcular_ancho_celda,
    crear_boton,
)

DIMENSION_MAXIMA = 25
TEXTO_INICIAL_MEMORIA = "Presione 'Calcular sustracción'."


class AplicacionRestaMatrices:
    """Ventana principal minimalista para la sustraccion de matrices."""

    def __init__(self, ventana):
        self.ventana = ventana
        self._habilitar_alta_definicion()

        self.ventana.title("Sustracción de matrices")
        self.ventana.configure(bg=COLORES["fondo_ventana"])
        self.ventana.minsize(760, 600)
        self._centrar_ventana(900, 700)

        # variables reactivas
        self.var_filas = tk.StringVar(value="3")
        self.var_columnas = tk.StringVar(value="3")
        self.var_metodo = tk.StringVar(value="bucles")

        self.ultimo_resultado = None

        self._construir_interfaz()

    def _habilitar_alta_definicion(self):
        # solo existe en windows 8.1+; en otros sistemas se ignora
        try:
            ctypes.windll.shcore.SetProcessDpiAwareness(1)
        except (AttributeError, OSError):
            pass

    def _centrar_ventana(self, ancho, alto):
        self.ventana.update_idletasks()
        sw = self.ventana.winfo_screenwidth()
        sh = self.ventana.winfo_screenheight()
        px = max(0, (sw - ancho) // 2)
        py = max(0, (sh - alto) // 2)
        self.ventana.geometry(f"{ancho}x{alto}+{px}+{py}")

    def _crear_entrada_dimension(self, contenedor, variable):
        entrada = tk.Entry(
            contenedor,
            textvariable=variable,
            width=3,
            justify="center",
            font=(FUENTE_MONO, 10),
            relief="solid",
            borderwidth=1,
            highlightthickness=0,
        )
        entrada.pack(side="left")
        entrada.bind("<Return>", lambda _e: self.actualizar_dimensiones())
        return entrada

    def _construir_interfaz(self):
        self.contenedor = tk.Frame(self.ventana, bg=COLORES["fondo_ventana"])
        self.contenedor.pack(fill="both", expand=True, padx=18, pady=14)

        self._construir_titulo()
        self._construir_barra_control()
        self._construir_panel_matrices()

        # boton de calcular a todo el ancho
        self.btn_calcular = crear_boton(
            self.contenedor,
            "Calcular sustracción (A − B)",
            self.calcular_resta,
            primario=True,
            fuente=(FUENTE_SANS, 10, "bold"),
            padx=16,
            pady=6,
        )
        self.btn_calcular.pack(fill="x", pady=(0, 10))

        self._construir_panel_resultado()

        # calculo inicial
        self.calcular_resta()

    def _construir_titulo(self):
        self.lbl_titulo = tk.Label(
            self.contenedor,
            text="Sustracción de matrices",
            font=(FUENTE_SANS, 15, "bold"),
            bg=COLORES["fondo_ventana"],
            fg=COLORES["texto_principal"],
        )
        self.lbl_titulo.pack(anchor="w", pady=(0, 10))

    def _construir_barra_control(self):
        self.tarjeta_control = tk.Frame(
            self.contenedor,
            bg=COLORES["fondo_tarjeta"],
            highlightbackground=COLORES["borde_tarjeta"],
            highlightthickness=1,
            padx=14,
            pady=10,
        )
        self.tarjeta_control.pack(fill="x", pady=(0, 10))

        # seccion dimension: [filas] x [columnas] (Generar)
        marco_dim = tk.Frame(self.tarjeta_control, bg=COLORES["fondo_tarjeta"])
        marco_dim.pack(side="left", padx=(0, 24))

        tk.Label(
            marco_dim,
            text="Dimensión:",
            font=(FUENTE_SANS, 9, "bold"),
            bg=COLORES["fondo_tarjeta"],
            fg=COLORES["texto_principal"],
        ).pack(side="left", padx=(0, 6))

        self.entry_filas = self._crear_entrada_dimension(marco_dim, self.var_filas)

        tk.Label(
            marco_dim,
            text="×",
            font=(FUENTE_SANS, 10),
            bg=COLORES["fondo_tarjeta"],
            fg=COLORES["texto_secundario"],
        ).pack(side="left", padx=4)

        self.entry_cols = self._crear_entrada_dimension(marco_dim, self.var_columnas)

        btn_generar = crear_boton(
            marco_dim,
            "Generar",
            self.actualizar_dimensiones,
            fuente=(FUENTE_SANS, 8, "bold"),
            pady=2,
        )
        btn_generar.pack(side="left", padx=(8, 0))

        # seccion metodo
        marco_metodo = tk.Frame(self.tarjeta_control, bg=COLORES["fondo_tarjeta"])
        marco_metodo.pack(side="left")

        tk.Label(
            marco_metodo,
            text="Método:",
            font=(FUENTE_SANS, 9, "bold"),
            bg=COLORES["fondo_tarjeta"],
            fg=COLORES["texto_principal"],
        ).pack(side="left", padx=(0, 6))

        metodos = [
            ("1. Bucles for", "bucles"),
            ("2. Comprensión", "comprension"),
            ("3. NumPy", "numpy"),
        ]
        for etiqueta, valor in metodos:
            rb = tk.Radiobutton(
                marco_metodo,
                text=etiqueta,
                variable=self.var_metodo,
                value=valor,
                font=(FUENTE_SANS, 9),
                bg=COLORES["fondo_tarjeta"],
                fg=COLORES["texto_principal"],
                activebackground=COLORES["fondo_tarjeta"],
                activeforeground=COLORES["texto_principal"],
                selectcolor=COLORES["fondo_tarjeta"],
                highlightthickness=0,
                cursor="hand2",
            )
            rb.pack(side="left", padx=4)

    def _construir_panel_matrices(self):
        # panel de matrices A y B con distribucion simetrica 50% / 50%
        self.marco_matrices = tk.Frame(self.contenedor, bg=COLORES["fondo_ventana"])
        self.marco_matrices.pack(fill="both", expand=True, pady=(0, 10))

        self.marco_matrices.grid_rowconfigure(0, weight=1)
        self.marco_matrices.grid_columnconfigure(0, weight=1, uniform="matrices")
        self.marco_matrices.grid_columnconfigure(1, weight=0)
        self.marco_matrices.grid_columnconfigure(2, weight=1, uniform="matrices")

        filas = int(self.var_filas.get())
        columnas = int(self.var_columnas.get())

        # matriz a (minuendo)
        self.matriz_a = CuadriculaMatriz(self.marco_matrices, "Matriz A", filas, columnas)
        self.matriz_a.tarjeta.grid(row=0, column=0, sticky="nsew", padx=(0, 4))

        # operador menos (signo matematico U+2212)
        self.lbl_menos = tk.Label(
            self.marco_matrices,
            text="−",
            font=(FUENTE_SANS, 20, "bold"),
            bg=COLORES["fondo_ventana"],
            fg=COLORES["texto_secundario"],
        )
        self.lbl_menos.grid(row=0, column=1, padx=6)

        # matriz b (sustraendo)
        self.matriz_b = CuadriculaMatriz(self.marco_matrices, "Matriz B", filas, columnas)
        self.matriz_b.tarjeta.grid(row=0, column=2, sticky="nsew", padx=(4, 0))

    def _construir_cabecera(self, contenedor, titulo, comando_copiar, bg, fuente, color):
        """Fila con un titulo a la izquierda y un boton 'Copiar' a la derecha."""
        cabecera = tk.Frame(contenedor, bg=bg)
        tk.Label(cabecera, text=titulo, font=fuente, bg=bg, fg=color).pack(side="left")
        boton = crear_boton(cabecera, "Copiar", comando_copiar)
        boton.pack(side="right")
        return cabecera, boton

    def _construir_panel_resultado(self):
        # panel de resultado: matriz C (izquierda) y memoria de calculo (derecha)
        self.tarjeta_resultado = tk.Frame(
            self.contenedor,
            bg=COLORES["fondo_tarjeta"],
            highlightbackground=COLORES["borde_tarjeta"],
            highlightthickness=1,
            padx=14,
            pady=10,
        )
        self.tarjeta_resultado.pack(fill="both", expand=True)

        cuerpo_res = tk.Frame(self.tarjeta_resultado, bg=COLORES["fondo_tarjeta"])
        cuerpo_res.pack(fill="both", expand=True)

        cuerpo_res.grid_rowconfigure(0, weight=1)
        cuerpo_res.grid_columnconfigure(0, weight=1, uniform="resultado")
        cuerpo_res.grid_columnconfigure(1, weight=1, uniform="resultado")

        # izq: columna matriz C con la misma caja desplazable que A y B
        col_matriz = tk.Frame(cuerpo_res, bg=COLORES["fondo_tarjeta"])
        col_matriz.grid(row=0, column=0, sticky="nsew", padx=(0, 6))

        cabecera_matriz, self.btn_copiar_matriz = self._construir_cabecera(
            col_matriz,
            "Matriz C",
            self.copiar_matriz,
            bg=COLORES["fondo_tarjeta"],
            fuente=(FUENTE_SANS, 10, "bold"),
            color=COLORES["texto_principal"],
        )
        cabecera_matriz.grid(row=0, column=0, sticky="ew", pady=(0, 4))

        self.caja_c = CajaDesplazable(col_matriz, fila=1)

        # der: columna memoria de calculo con scrollbar vertical
        col_memoria = tk.Frame(
            cuerpo_res,
            bg=COLORES["resultado_fondo"],
            padx=10,
            pady=6,
        )
        col_memoria.grid(row=0, column=1, sticky="nsew", padx=(6, 0))

        cabecera_memoria, self.btn_copiar_memoria = self._construir_cabecera(
            col_memoria,
            "Memoria de cálculo:",
            self.copiar_memoria,
            bg=COLORES["resultado_fondo"],
            fuente=(FUENTE_SANS, 9, "bold"),
            color=COLORES["texto_secundario"],
        )
        cabecera_memoria.pack(fill="x", pady=(0, 4))

        marco_txt_memoria = tk.Frame(col_memoria, bg=COLORES["resultado_fondo"])
        marco_txt_memoria.pack(fill="both", expand=True)

        vbar_memoria = tk.Scrollbar(marco_txt_memoria, orient="vertical")
        vbar_memoria.pack(side="right", fill="y")

        self.texto_memoria = tk.Text(
            marco_txt_memoria,
            font=(FUENTE_MONO, 9),
            bg=COLORES["resultado_fondo"],
            fg=COLORES["texto_principal"],
            relief="flat",
            wrap="none",
            height=5,
            width=28,
            yscrollcommand=vbar_memoria.set,
        )
        self.texto_memoria.pack(side="left", fill="both", expand=True)
        vbar_memoria.config(command=self.texto_memoria.yview)

        self._escribir_memoria(TEXTO_INICIAL_MEMORIA)

    def _escribir_memoria(self, texto):
        """Reemplaza el contenido de la memoria de calculo (de solo lectura)."""
        self.texto_memoria.config(state="normal")
        self.texto_memoria.delete("1.0", tk.END)
        self.texto_memoria.insert("1.0", texto)
        self.texto_memoria.config(state="disabled")

    def _leer_dimensiones(self):
        """Valida los campos de dimension; columnas vacio equivale a matriz cuadrada."""
        texto_f = self.var_filas.get().strip()
        texto_c = self.var_columnas.get().strip() or texto_f
        try:
            filas = int(texto_f)
            columnas = int(texto_c)
        except ValueError:
            raise ValueError("Las dimensiones deben ser números enteros.") from None

        if filas <= 0 or columnas <= 0:
            raise ValueError("Las dimensiones deben ser mayores a 0.")
        if filas > DIMENSION_MAXIMA or columnas > DIMENSION_MAXIMA:
            raise ValueError(f"La dimensión máxima admitida es {DIMENSION_MAXIMA}.")
        return filas, columnas

    def actualizar_dimensiones(self):
        """Ajusta las dimensiones de las matrices segun los campos de entrada."""
        try:
            filas, columnas = self._leer_dimensiones()
        except ValueError as err:
            messagebox.showerror("Error de dimensión", str(err), parent=self.ventana)
            return

        self.var_filas.set(str(filas))
        self.var_columnas.set(str(columnas))

        # a y b siempre con la misma dimension: condicion para poder restar
        self.matriz_a.construir_celdas(filas, columnas)
        self.matriz_b.construir_celdas(filas, columnas)

        self.calcular_resta()

    def calcular_resta(self):
        """Lee casillas, resta A - B y muestra la matriz C con su memoria de calculo."""
        try:
            datos_a = self.matriz_a.extraer_matriz()
            datos_b = self.matriz_b.extraer_matriz()
        except ValueError as err:
            messagebox.showerror("Dato no numérico", str(err), parent=self.ventana)
            return

        matriz_c = calcular_resta_metodo(datos_a, datos_b, self.var_metodo.get())
        self.ultimo_resultado = matriz_c

        self._mostrar_matriz_c(matriz_c)
        self._escribir_memoria("\n".join(generar_paso_a_paso(datos_a, datos_b, matriz_c)))

    def _mostrar_matriz_c(self, matriz_c):
        """Dibuja la matriz resultado como celdas de solo lectura."""
        self.caja_c.limpiar()

        filas = len(matriz_c)
        columnas = len(matriz_c[0])
        self.caja_c.ajustar_corchetes(filas)
        ancho_celda = calcular_ancho_celda(columnas)

        for i in range(filas):
            for j in range(columnas):
                lbl = tk.Label(
                    self.caja_c.marco_grid,
                    text=formatear_numero(matriz_c[i][j]),
                    width=ancho_celda,
                    font=(FUENTE_MONO, 10, "bold"),
                    bg=COLORES["celda_resultado_fondo"],
                    fg=COLORES["celda_resultado_texto"],
                    highlightbackground=COLORES["celda_resultado_borde"],
                    highlightthickness=1,
                    pady=3,
                )
                lbl.grid(row=i, column=j, padx=2, pady=2)
                self.caja_c.vincular_rueda_mouse(lbl)

        self.caja_c.ajustar()

    def _copiar_al_portapapeles(self, texto, boton):
        """Copia texto al portapapeles y confirma en el boton durante 1.2 s."""
        self.ventana.clipboard_clear()
        self.ventana.clipboard_append(texto)

        boton.config(text="✓ Copiado", bg=boton.color_hover)
        self.ventana.after(1200, lambda: boton.config(text="Copiar", bg=boton.color_normal))

    def copiar_matriz(self):
        """Copia la matriz C separada por tabulaciones (se pega en excel celda a celda)."""
        if not self.ultimo_resultado:
            return
        self._copiar_al_portapapeles(matriz_a_tsv(self.ultimo_resultado), self.btn_copiar_matriz)

    def copiar_memoria(self):
        """Copia el texto completo de la memoria de calculo al portapapeles."""
        texto = self.texto_memoria.get("1.0", tk.END).strip()
        if not texto or texto == TEXTO_INICIAL_MEMORIA:
            return
        self._copiar_al_portapapeles(texto, self.btn_copiar_memoria)

    def copiar_resultado(self):
        """Metodo de compatibilidad para copiar matriz C."""
        self.copiar_matriz()


if __name__ == "__main__":
    raiz = tk.Tk()
    app = AplicacionRestaMatrices(raiz)
    raiz.mainloop()
