# interfaz grafica minimalista y limpia para sustraccion de matrices
# con soporte para dimensiones complejas mediante cajas desplazables (boxes movibles)
import ctypes
import tkinter as tk
from tkinter import messagebox

from app.frontend.widgets_matriz import (
    COLORES,
    FUENTE_MONO,
    FUENTE_SANS,
    CuadriculaMatriz,
    calcular_resta_metodo,
    formatear_numero,
    generar_paso_a_paso,
)


class AplicacionRestaMatrices:
    """Ventana principal minimalista para la sustraccion de matrices."""

    def __init__(self, ventana):
        self.ventana = ventana
        self._habilitar_alta_definicion()

        self.ventana.title("Sustracción de matrices")
        self.ventana.configure(bg=COLORES["fondo_ventana"])
        self.ventana.geometry("900x700")
        self.ventana.minsize(760, 600)
        self._centrar_ventana(900, 700)

        # variables reactivas
        self.var_filas = tk.StringVar(value="3")
        self.var_columnas = tk.StringVar(value="3")
        self.var_metodo = tk.StringVar(value="bucles")

        self.ultimo_resultado = None

        self._construir_interfaz()

    def _habilitar_alta_definicion(self):
        try:
            ctypes.windll.shcore.SetProcessDpiAwareness(1)
        except Exception:
            pass

    def _centrar_ventana(self, ancho, alto):
        self.ventana.update_idletasks()
        sw = self.ventana.winfo_screenwidth()
        sh = self.ventana.winfo_screenheight()
        px = max(0, (sw - ancho) // 2)
        py = max(0, (sh - alto) // 2)
        self.ventana.geometry(f"{ancho}x{alto}+{px}+{py}")

    def _construir_interfaz(self):
        self.contenedor = tk.Frame(self.ventana, bg=COLORES["fondo_ventana"])
        self.contenedor.pack(fill="both", expand=True, padx=18, pady=14)

        # 1. titulo simple
        self.lbl_titulo = tk.Label(
            self.contenedor,
            text="Sustracción de matrices",
            font=(FUENTE_SANS, 15, "bold"),
            bg=COLORES["fondo_ventana"],
            fg=COLORES["texto_principal"],
        )
        self.lbl_titulo.pack(anchor="w", pady=(0, 10))

        # 2. barra de dimension y metodo
        self.tarjeta_control = tk.Frame(
            self.contenedor,
            bg=COLORES["fondo_tarjeta"],
            highlightbackground=COLORES["borde_tarjeta"],
            highlightthickness=1,
            padx=14,
            pady=10,
        )
        self.tarjeta_control.pack(fill="x", pady=(0, 10))

        # seccion dimension
        marco_dim = tk.Frame(self.tarjeta_control, bg=COLORES["fondo_tarjeta"])
        marco_dim.pack(side="left", padx=(0, 24))

        tk.Label(
            marco_dim,
            text="Dimensión:",
            font=(FUENTE_SANS, 9, "bold"),
            bg=COLORES["fondo_tarjeta"],
            fg=COLORES["texto_principal"],
        ).pack(side="left", padx=(0, 6))

        self.entry_filas = tk.Entry(
            marco_dim,
            textvariable=self.var_filas,
            width=3,
            justify="center",
            font=(FUENTE_MONO, 10),
            relief="solid",
            borderwidth=1,
            highlightthickness=0,
        )
        self.entry_filas.pack(side="left")
        self.entry_filas.bind("<Return>", lambda _e: self.actualizar_dimensiones())

        tk.Label(
            marco_dim,
            text="×",
            font=(FUENTE_SANS, 10),
            bg=COLORES["fondo_tarjeta"],
            fg=COLORES["texto_secundario"],
        ).pack(side="left", padx=4)

        self.entry_cols = tk.Entry(
            marco_dim,
            textvariable=self.var_columnas,
            width=3,
            justify="center",
            font=(FUENTE_MONO, 10),
            relief="solid",
            borderwidth=1,
            highlightthickness=0,
        )
        self.entry_cols.pack(side="left")
        self.entry_cols.bind("<Return>", lambda _e: self.actualizar_dimensiones())

        btn_generar = tk.Button(
            marco_dim,
            text="Generar",
            font=(FUENTE_SANS, 8, "bold"),
            bg=COLORES["boton_secundario"],
            fg=COLORES["boton_secundario_texto"],
            activebackground=COLORES["boton_secundario_hover"],
            activeforeground=COLORES["boton_secundario_texto"],
            relief="flat",
            padx=8,
            pady=2,
            cursor="hand2",
            command=self.actualizar_dimensiones,
        )
        btn_generar.pack(side="left", padx=(8, 0))
        self._hover(btn_generar, COLORES["boton_secundario"], COLORES["boton_secundario_hover"])

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

        # 3. panel de matrices A y B con distribucion simetrica 50% / 50%
        self.marco_matrices = tk.Frame(self.contenedor, bg=COLORES["fondo_ventana"])
        self.marco_matrices.pack(fill="both", expand=True, pady=(0, 10))

        self.marco_matrices.grid_rowconfigure(0, weight=1)
        self.marco_matrices.grid_columnconfigure(0, weight=1, uniform="matrices")
        self.marco_matrices.grid_columnconfigure(1, weight=0)
        self.marco_matrices.grid_columnconfigure(2, weight=1, uniform="matrices")

        # matriz a
        self.matriz_a = CuadriculaMatriz(
            self.marco_matrices,
            titulo="Matriz A",
            filas=int(self.var_filas.get()),
            columnas=int(self.var_columnas.get()),
        )
        self.matriz_a.tarjeta.grid(row=0, column=0, sticky="nsew", padx=(0, 4))

        # operador menos
        self.lbl_menos = tk.Label(
            self.marco_matrices,
            text="−",
            font=(FUENTE_SANS, 20, "bold"),
            bg=COLORES["fondo_ventana"],
            fg=COLORES["texto_secundario"],
        )
        self.lbl_menos.grid(row=0, column=1, padx=6)

        # matriz b
        self.matriz_b = CuadriculaMatriz(
            self.marco_matrices,
            titulo="Matriz B",
            filas=int(self.var_filas.get()),
            columnas=int(self.var_columnas.get()),
        )
        self.matriz_b.tarjeta.grid(row=0, column=2, sticky="nsew", padx=(4, 0))

        # 4. boton de calcular minimalista
        self.btn_calcular = tk.Button(
            self.contenedor,
            text="Calcular sustracción (A − B)",
            font=(FUENTE_SANS, 10, "bold"),
            bg=COLORES["boton_primario"],
            fg=COLORES["boton_primario_texto"],
            activebackground=COLORES["boton_primario_hover"],
            activeforeground=COLORES["boton_primario_texto"],
            relief="flat",
            padx=16,
            pady=6,
            cursor="hand2",
            command=self.calcular_resta,
        )
        self.btn_calcular.pack(fill="x", pady=(0, 10))
        self._hover(self.btn_calcular, COLORES["boton_primario"], COLORES["boton_primario_hover"])

        # 5. panel de resultado: Matriz C y flujo de memoria con cajas desplazables
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

        # izq: columna Matriz C con caja desplazable
        col_matriz = tk.Frame(cuerpo_res, bg=COLORES["fondo_tarjeta"])
        col_matriz.grid(row=0, column=0, sticky="nsew", padx=(0, 6))

        col_matriz.grid_rowconfigure(1, weight=1)
        col_matriz.grid_columnconfigure(0, weight=1)

        cabecera_matriz = tk.Frame(col_matriz, bg=COLORES["fondo_tarjeta"])
        cabecera_matriz.grid(row=0, column=0, sticky="ew", pady=(0, 4))

        tk.Label(
            cabecera_matriz,
            text="Matriz C",
            font=(FUENTE_SANS, 10, "bold"),
            bg=COLORES["fondo_tarjeta"],
            fg=COLORES["texto_principal"],
        ).pack(side="left")

        self.btn_copiar_matriz = tk.Button(
            cabecera_matriz,
            text="Copiar",
            font=(FUENTE_SANS, 8),
            bg=COLORES["boton_secundario"],
            fg=COLORES["boton_secundario_texto"],
            activebackground=COLORES["boton_secundario_hover"],
            activeforeground=COLORES["boton_secundario_texto"],
            relief="flat",
            padx=8,
            pady=1,
            cursor="hand2",
            command=self.copiar_matriz,
        )
        self.btn_copiar_matriz.pack(side="right")
        self._hover(self.btn_copiar_matriz, COLORES["boton_secundario"], COLORES["boton_secundario_hover"])

        # canvas para matriz C (box movible)
        self.canvas_c = tk.Canvas(
            col_matriz,
            bg=COLORES["fondo_tarjeta"],
            highlightthickness=0,
            bd=0,
        )
        self.canvas_c.grid(row=1, column=0, sticky="nsew")

        self.hbar_c = tk.Scrollbar(
            col_matriz, orient="horizontal", command=self.canvas_c.xview
        )
        self.vbar_c = tk.Scrollbar(
            col_matriz, orient="vertical", command=self.canvas_c.yview
        )
        self.canvas_c.configure(
            xscrollcommand=self.hbar_c.set, yscrollcommand=self.vbar_c.set
        )

        self.marco_algebraico_c = tk.Frame(self.canvas_c, bg=COLORES["fondo_tarjeta"])
        self.win_id_c = self.canvas_c.create_window(
            (0, 0), window=self.marco_algebraico_c, anchor="nw"
        )

        self.lbl_res_corchete_izq = tk.Label(
            self.marco_algebraico_c,
            text="[",
            font=(FUENTE_MONO, 24, "normal"),
            bg=COLORES["fondo_tarjeta"],
            fg=COLORES["corchete_color"],
        )
        self.lbl_res_corchete_izq.pack(side="left", padx=(0, 2))

        self.grid_c = tk.Frame(self.marco_algebraico_c, bg=COLORES["fondo_tarjeta"])
        self.grid_c.pack(side="left")

        self.lbl_res_corchete_der = tk.Label(
            self.marco_algebraico_c,
            text="]",
            font=(FUENTE_MONO, 24, "normal"),
            bg=COLORES["fondo_tarjeta"],
            fg=COLORES["corchete_color"],
        )
        self.lbl_res_corchete_der.pack(side="left", padx=(2, 0))

        self.canvas_c.bind("<Configure>", self._al_redimensionar_canvas_c)
        self.marco_algebraico_c.bind("<Configure>", self._al_redimensionar_canvas_c)

        # der: columna Memoria de calculo con scrollbar vertical
        col_memoria = tk.Frame(
            cuerpo_res,
            bg=COLORES["resultado_fondo"],
            padx=10,
            pady=6,
        )
        col_memoria.grid(row=0, column=1, sticky="nsew", padx=(6, 0))

        cabecera_memoria = tk.Frame(col_memoria, bg=COLORES["resultado_fondo"])
        cabecera_memoria.pack(fill="x", pady=(0, 4))

        tk.Label(
            cabecera_memoria,
            text="Memoria de cálculo:",
            font=(FUENTE_SANS, 9, "bold"),
            bg=COLORES["resultado_fondo"],
            fg=COLORES["texto_secundario"],
        ).pack(side="left")

        self.btn_copiar_memoria = tk.Button(
            cabecera_memoria,
            text="Copiar",
            font=(FUENTE_SANS, 8),
            bg=COLORES["boton_secundario"],
            fg=COLORES["boton_secundario_texto"],
            activebackground=COLORES["boton_secundario_hover"],
            activeforeground=COLORES["boton_secundario_texto"],
            relief="flat",
            padx=8,
            pady=1,
            cursor="hand2",
            command=self.copiar_memoria,
        )
        self.btn_copiar_memoria.pack(side="right")
        self._hover(self.btn_copiar_memoria, COLORES["boton_secundario"], COLORES["boton_secundario_hover"])

        # contenedor para texto y barra de desplazamiento vertical de memoria
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

        self.texto_memoria.insert("1.0", "Presione 'Calcular sustracción'.")
        self.texto_memoria.config(state="disabled")

        # calculo inicial
        self.calcular_resta()

    def _al_redimensionar_canvas_c(self, _event=None):
        """Ajusta las barras de desplazamiento para la Matriz C y centra si cabe."""
        self.tarjeta_resultado.update_idletasks()
        cw = self.marco_algebraico_c.winfo_reqwidth()
        ch = self.marco_algebraico_c.winfo_reqheight()
        can_w = self.canvas_c.winfo_width()
        can_h = self.canvas_c.winfo_height()

        if can_w <= 1 or can_h <= 1:
            return

        if cw > can_w:
            self.hbar_c.grid(row=2, column=0, sticky="ew")
            pos_x = 0
        else:
            self.hbar_c.grid_forget()
            self.canvas_c.xview_moveto(0)
            pos_x = max(0, (can_w - cw) // 2)

        if ch > can_h:
            self.vbar_c.grid(row=1, column=1, sticky="ns")
            pos_y = 0
        else:
            self.vbar_c.grid_forget()
            self.canvas_c.yview_moveto(0)
            pos_y = max(0, (can_h - ch) // 2)

        self.canvas_c.coords(self.win_id_c, pos_x, pos_y)
        self.canvas_c.configure(
            scrollregion=(0, 0, max(can_w, cw + pos_x), max(can_h, ch + pos_y))
        )

    def actualizar_dimensiones(self):
        """Ajusta las dimensiones de las matrices segun los campos de entrada."""
        try:
            texto_f = self.var_filas.get().strip()
            texto_c = self.var_columnas.get().strip()

            filas = int(texto_f)
            columnas = int(texto_c) if texto_c else filas

            if filas <= 0 or columnas <= 0:
                raise ValueError("Las dimensiones deben ser mayores a 0.")
            if filas > 25 or columnas > 25:
                raise ValueError("La dimensión máxima admitida es 25.")

            self.var_filas.set(str(filas))
            self.var_columnas.set(str(columnas))

            self.matriz_a.construir_celdas(filas, columnas)
            self.matriz_b.construir_celdas(filas, columnas)

            self.calcular_resta()
        except ValueError as err:
            messagebox.showerror("Error de dimensión", str(err), parent=self.ventana)

    def calcular_resta(self):
        """Lee casillas, resta A - B y muestra la matriz C con su memoria de calculo."""
        try:
            datos_a = self.matriz_a.extraer_matriz()
            datos_b = self.matriz_b.extraer_matriz()
        except ValueError as err:
            messagebox.showerror("Dato no numérico", str(err), parent=self.ventana)
            return

        metodo = self.var_metodo.get()
        matriz_c = calcular_resta_metodo(datos_a, datos_b, metodo)
        self.ultimo_resultado = matriz_c

        # renderizar celdas de C
        for w in self.grid_c.winfo_children():
            w.destroy()

        filas = len(matriz_c)
        columnas = len(matriz_c[0])

        tamano_corchete = max(18, min(48, 16 + (filas - 1) * 8))
        self.lbl_res_corchete_izq.config(font=(FUENTE_MONO, tamano_corchete, "normal"))
        self.lbl_res_corchete_der.config(font=(FUENTE_MONO, tamano_corchete, "normal"))

        ancho_celda = 4 if columnas > 4 else 5

        for i in range(filas):
            for j in range(columnas):
                valor_str = formatear_numero(matriz_c[i][j])
                lbl = tk.Label(
                    self.grid_c,
                    text=valor_str,
                    width=ancho_celda,
                    font=(FUENTE_MONO, 10, "bold"),
                    bg=COLORES["celda_resultado_fondo"],
                    fg=COLORES["celda_resultado_texto"],
                    highlightbackground=COLORES["celda_resultado_borde"],
                    highlightthickness=1,
                    pady=3,
                )
                lbl.grid(row=i, column=j, padx=2, pady=2)

        self._al_redimensionar_canvas_c()

        # actualizar memoria y flujo
        lineas_memoria = generar_paso_a_paso(datos_a, datos_b, matriz_c)
        self.texto_memoria.config(state="normal")
        self.texto_memoria.delete("1.0", tk.END)
        self.texto_memoria.insert("1.0", "\n".join(lineas_memoria))
        self.texto_memoria.config(state="disabled")

    def copiar_matriz(self):
        """Copia la matriz C formateada al portapapeles con confirmacion visual."""
        if not self.ultimo_resultado:
            return
        lineas = ["\t".join(formatear_numero(v) for v in fila) for fila in self.ultimo_resultado]
        self.ventana.clipboard_clear()
        self.ventana.clipboard_append("\n".join(lineas))

        self.btn_copiar_matriz.config(text="✓ Copiado", bg=COLORES["boton_secundario_hover"])
        self.ventana.after(
            1200,
            lambda: self.btn_copiar_matriz.config(
                text="Copiar", bg=COLORES["boton_secundario"]
            ),
        )

    def copiar_memoria(self):
        """Copia el texto completo de la memoria de calculo al portapapeles."""
        texto = self.texto_memoria.get("1.0", tk.END).strip()
        if not texto or texto.startswith("Presione"):
            return
        self.ventana.clipboard_clear()
        self.ventana.clipboard_append(texto)

        self.btn_copiar_memoria.config(text="✓ Copiado", bg=COLORES["boton_secundario_hover"])
        self.ventana.after(
            1200,
            lambda: self.btn_copiar_memoria.config(
                text="Copiar", bg=COLORES["boton_secundario"]
            ),
        )

    def copiar_resultado(self):
        """Metodo de compatibilidad para copiar matriz C."""
        self.copiar_matriz()

    def _hover(self, boton, normal, hover):
        boton.bind("<Enter>", lambda _e: boton.config(bg=hover))
        boton.bind("<Leave>", lambda _e: boton.config(bg=normal))


if __name__ == "__main__":
    raiz = tk.Tk()
    app = AplicacionRestaMatrices(raiz)
    raiz.mainloop()
