# modulo de componentes graficos reutilizables para matrices en tkinter
# componentes minimalistas con cajas desplazables (boxes movibles) para matrices
import tkinter as tk
import numpy as np

# paleta de diseno minimalista, sobria y limpia
COLORES = {
    "fondo_ventana": "#f8fafc",      # Slate 50
    "fondo_tarjeta": "#ffffff",      # Blanco puro
    "borde_tarjeta": "#e2e8f0",      # Slate 200
    "borde_activo": "#2563eb",       # Azul 600
    "texto_principal": "#0f172a",    # Slate 900
    "texto_secundario": "#475569",   # Slate 600
    "texto_atenuado": "#94a3b8",     # Slate 400
    "boton_primario": "#2563eb",     # Azul 600
    "boton_primario_hover": "#1d4ed8",
    "boton_primario_texto": "#ffffff",
    "boton_secundario": "#f1f5f9",   # Slate 100
    "boton_secundario_hover": "#e2e8f0",
    "boton_secundario_texto": "#334155",
    "entrada_fondo": "#ffffff",
    "entrada_texto": "#0f172a",
    "entrada_borde": "#cbd5e1",      # Slate 300
    "entrada_borde_foco": "#2563eb",
    "resultado_fondo": "#f8fafc",
    "celda_resultado_fondo": "#f1f5f9",
    "celda_resultado_borde": "#cbd5e1",
    "celda_resultado_texto": "#0f172a",
    "corchete_color": "#64748b",
    "error_texto": "#dc2626",
}
PALETAS = {"claro": COLORES}

FUENTE_SANS = "Segoe UI"
FUENTE_MONO = "Consolas"


def formatear_numero(valor):
    """Formatea numeros para mostrar enteros limpios o decimales reducidos."""
    if isinstance(valor, (int, float)):
        if float(valor).is_integer():
            return str(int(valor))
        return f"{valor:.4g}"
    return str(valor)


class EntradaCeldaMatriz:
    """Casilla individual de entrada numerica con borde sutil y notificacion de foco."""

    def __init__(self, contenedor, fila, columna, ancho=4, al_enfocar_cb=None):
        self.fila = fila
        self.columna = columna
        self.al_enfocar_cb = al_enfocar_cb

        self.marco_borde = tk.Frame(
            contenedor,
            bg=COLORES["entrada_borde"],
            padx=1,
            pady=1,
        )

        self.entry = tk.Entry(
            self.marco_borde,
            width=ancho,
            justify="center",
            font=(FUENTE_MONO, 10, "bold"),
            relief="flat",
            bg=COLORES["entrada_fondo"],
            fg=COLORES["entrada_texto"],
            insertbackground=COLORES["texto_principal"],
        )
        self.entry.pack(fill="both", expand=True, ipady=3)
        self.entry.insert(0, "0")

        self.entry.bind("<FocusIn>", self._al_enfocar)
        self.entry.bind("<FocusOut>", self._al_desenfocar)

    def _al_enfocar(self, _event=None):
        self.marco_borde.config(bg=COLORES["entrada_borde_foco"])
        self.entry.select_range(0, tk.END)
        if self.al_enfocar_cb:
            self.al_enfocar_cb(self)

    def _al_desenfocar(self, _event=None):
        self.marco_borde.config(bg=COLORES["entrada_borde"])

    def obtener_texto(self):
        return self.entry.get().strip()

    def establecer_texto(self, texto):
        self.entry.delete(0, tk.END)
        self.entry.insert(0, str(texto))


class CuadriculaMatriz:
    """Gestiona una matriz dentro de una caja desplazable (box movible / scrollable)."""

    def __init__(self, contenedor, titulo, filas=3, columnas=3):
        self.contenedor = contenedor
        self.titulo = titulo
        self.filas = filas
        self.columnas = columnas
        self.celdas = []

        # tarjeta exterior
        self.tarjeta = tk.Frame(
            contenedor,
            bg=COLORES["fondo_tarjeta"],
            highlightbackground=COLORES["borde_tarjeta"],
            highlightthickness=1,
            padx=10,
            pady=8,
        )

        # configuracion de filas y columnas de la tarjeta para grid
        self.tarjeta.grid_rowconfigure(1, weight=1)
        self.tarjeta.grid_columnconfigure(0, weight=1)

        # cabecera
        self.lbl_titulo = tk.Label(
            self.tarjeta,
            text=self.titulo,
            font=(FUENTE_SANS, 10, "bold"),
            bg=COLORES["fondo_tarjeta"],
            fg=COLORES["texto_principal"],
        )
        self.lbl_titulo.grid(row=0, column=0, sticky="w", pady=(0, 4))

        # canvas para viewport desplazable (box movible)
        self.canvas = tk.Canvas(
            self.tarjeta,
            bg=COLORES["fondo_tarjeta"],
            highlightthickness=0,
            bd=0,
        )
        self.canvas.grid(row=1, column=0, sticky="nsew")

        # barras de desplazamiento horizontal y vertical
        self.hbar = tk.Scrollbar(
            self.tarjeta, orient="horizontal", command=self.canvas.xview
        )
        self.vbar = tk.Scrollbar(
            self.tarjeta, orient="vertical", command=self.canvas.yview
        )
        self.canvas.configure(
            xscrollcommand=self.hbar.set, yscrollcommand=self.vbar.set
        )

        # marco algebraico interior montado en el canvas
        self.marco_algebraico = tk.Frame(self.canvas, bg=COLORES["fondo_tarjeta"])
        self.win_id = self.canvas.create_window(
            (0, 0), window=self.marco_algebraico, anchor="nw"
        )

        self.lbl_corchete_izq = tk.Label(
            self.marco_algebraico,
            text="[",
            font=(FUENTE_MONO, 24, "normal"),
            bg=COLORES["fondo_tarjeta"],
            fg=COLORES["corchete_color"],
        )
        self.lbl_corchete_izq.pack(side="left", padx=(0, 2))

        self.marco_grid = tk.Frame(self.marco_algebraico, bg=COLORES["fondo_tarjeta"])
        self.marco_grid.pack(side="left")

        self.lbl_corchete_der = tk.Label(
            self.marco_algebraico,
            text="]",
            font=(FUENTE_MONO, 24, "normal"),
            bg=COLORES["fondo_tarjeta"],
            fg=COLORES["corchete_color"],
        )
        self.lbl_corchete_der.pack(side="left", padx=(2, 0))

        # eventos de reconfiguracion de tamano y desplazamiento
        self.canvas.bind("<Configure>", self._al_redimensionar_canvas)
        self.marco_algebraico.bind("<Configure>", self._al_redimensionar_canvas)

        # soporte para rueda del mouse
        self._vincular_rueda_mouse(self.canvas)
        self._vincular_rueda_mouse(self.marco_algebraico)

        self.construir_celdas(filas, columnas)

    def _vincular_rueda_mouse(self, widget):
        """Permite mover el contenido de la caja con la rueda del raton."""
        def _scroll_v(event):
            self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

        def _scroll_h(event):
            self.canvas.xview_scroll(int(-1 * (event.delta / 120)), "units")

        widget.bind("<MouseWheel>", _scroll_v)
        widget.bind("<Shift-MouseWheel>", _scroll_h)

    def _al_redimensionar_canvas(self, _event=None):
        """Ajusta las barras de desplazamiento y centra el contenido si cabe completamente."""
        self.tarjeta.update_idletasks()
        cw = self.marco_algebraico.winfo_reqwidth()
        ch = self.marco_algebraico.winfo_reqheight()
        can_w = self.canvas.winfo_width()
        can_h = self.canvas.winfo_height()

        if can_w <= 1 or can_h <= 1:
            return

        # scrollbar horizontal: se activa si el contenido es mas ancho que el viewport
        if cw > can_w:
            self.hbar.grid(row=2, column=0, sticky="ew")
            pos_x = 0
        else:
            self.hbar.grid_forget()
            self.canvas.xview_moveto(0)
            pos_x = max(0, (can_w - cw) // 2)

        # scrollbar vertical: se activa si el contenido es mas alto que el viewport
        if ch > can_h:
            self.vbar.grid(row=1, column=1, sticky="ns")
            pos_y = 0
        else:
            self.vbar.grid_forget()
            self.canvas.yview_moveto(0)
            pos_y = max(0, (can_h - ch) // 2)

        self.canvas.coords(self.win_id, pos_x, pos_y)
        self.canvas.configure(
            scrollregion=(0, 0, max(can_w, cw + pos_x), max(can_h, ch + pos_y))
        )

    def construir_celdas(self, filas, columnas):
        """Reconstruye las casillas segun las filas y columnas indicadas, rellenas de 0."""
        self.filas = max(1, int(filas))
        self.columnas = max(1, int(columnas))

        for fila in self.celdas:
            for celda in fila:
                celda.marco_borde.destroy()
        self.celdas.clear()

        tamano_corchete = max(18, min(48, 16 + (self.filas - 1) * 8))
        self.lbl_corchete_izq.config(font=(FUENTE_MONO, tamano_corchete, "normal"))
        self.lbl_corchete_der.config(font=(FUENTE_MONO, tamano_corchete, "normal"))

        ancho_celda = 4 if self.columnas > 4 else 5

        for i in range(self.filas):
            fila_widgets = []
            for j in range(self.columnas):
                celda = EntradaCeldaMatriz(
                    self.marco_grid,
                    fila=i,
                    columna=j,
                    ancho=ancho_celda,
                    al_enfocar_cb=self._asegurar_visibilidad,
                )
                celda.marco_borde.grid(row=i, column=j, padx=2, pady=2)
                self._vincular_teclado(celda, i, j)
                self._vincular_rueda_mouse(celda.entry)
                fila_widgets.append(celda)
            self.celdas.append(fila_widgets)

        self._al_redimensionar_canvas()

    def _asegurar_visibilidad(self, celda):
        """Desplaza la caja automaticamente para mantener visible la celda enfocada."""
        self.tarjeta.update_idletasks()
        can_w = self.canvas.winfo_width()
        can_h = self.canvas.winfo_height()
        if can_w <= 1 or can_h <= 1:
            return

        cx = celda.marco_borde.winfo_x() + self.marco_grid.winfo_x()
        cw = celda.marco_borde.winfo_width()
        cy = celda.marco_borde.winfo_y() + self.marco_grid.winfo_y()
        ch = celda.marco_borde.winfo_height()

        bbox = self.canvas.bbox("all")
        if not bbox:
            return
        total_w = bbox[2]
        total_h = bbox[3]

        if total_w > can_w:
            x0 = self.canvas.xview()[0] * total_w
            x1 = self.canvas.xview()[1] * total_w
            if cx < x0:
                self.canvas.xview_moveto(max(0, cx - 10) / total_w)
            elif cx + cw > x1:
                self.canvas.xview_moveto(min(1.0, (cx + cw + 10 - can_w) / total_w))

        if total_h > can_h:
            y0 = self.canvas.yview()[0] * total_h
            y1 = self.canvas.yview()[1] * total_h
            if cy < y0:
                self.canvas.yview_moveto(max(0, cy - 10) / total_h)
            elif cy + ch > y1:
                self.canvas.yview_moveto(min(1.0, (cy + ch + 10 - can_h) / total_h))

    def _vincular_teclado(self, celda, i, j):
        def mover(di, dj):
            ni = (i + di) % self.filas
            nj = (j + dj) % self.columnas
            self.celdas[ni][nj].entry.focus_set()

        celda.entry.bind("<Up>", lambda _e: mover(-1, 0))
        celda.entry.bind("<Down>", lambda _e: mover(1, 0))
        celda.entry.bind("<Left>", lambda _e: mover(0, -1))
        celda.entry.bind("<Right>", lambda _e: mover(0, 1))
        celda.entry.bind("<Return>", lambda _e: mover(0, 1))

    def extraer_matriz(self):
        matriz = []
        for i, fila in enumerate(self.celdas):
            fila_num = []
            for j, celda in enumerate(fila):
                texto = celda.obtener_texto()
                try:
                    valor = float(texto)
                except ValueError:
                    celda.marco_borde.config(bg=COLORES["error_texto"])
                    celda.entry.focus_set()
                    raise ValueError(
                        f"En {self.titulo}, posición ({i + 1}, {j + 1}): '{texto}' no es un número válido."
                    )
                fila_num.append(valor)
            matriz.append(fila_num)
        return matriz

    def establecer_matriz(self, datos):
        filas = min(len(datos), self.filas)
        for i in range(filas):
            cols = min(len(datos[i]), self.columnas)
            for j in range(cols):
                self.celdas[i][j].establecer_texto(formatear_numero(datos[i][j]))

    def limpiar(self, valor="0"):
        for fila in self.celdas:
            for celda in fila:
                celda.establecer_texto(valor)


# ---------------------------------------------------------------------------
# Algoritmos de calculo
# ---------------------------------------------------------------------------
def restar_matrices_bucles_frontend(matriz_a, matriz_b):
    filas = len(matriz_a)
    columnas = len(matriz_a[0])
    resultado = []
    for i in range(filas):
        fila = []
        for j in range(columnas):
            fila.append(matriz_a[i][j] - matriz_b[i][j])
        resultado.append(fila)
    return resultado


def restar_matrices_comprension_frontend(matriz_a, matriz_b):
    filas = len(matriz_a)
    columnas = len(matriz_a[0])
    return [
        [matriz_a[i][j] - matriz_b[i][j] for j in range(columnas)]
        for i in range(filas)
    ]


def restar_matrices_numpy_frontend(matriz_a, matriz_b):
    arreglo_a = np.array(matriz_a, dtype=float)
    arreglo_b = np.array(matriz_b, dtype=float)
    return (arreglo_a - arreglo_b).tolist()


def calcular_resta_metodo(matriz_a, matriz_b, metodo):
    if metodo == "comprension":
        return restar_matrices_comprension_frontend(matriz_a, matriz_b)
    elif metodo == "numpy":
        return restar_matrices_numpy_frontend(matriz_a, matriz_b)
    return restar_matrices_bucles_frontend(matriz_a, matriz_b)


def generar_paso_a_paso(matriz_a, matriz_b, matriz_c):
    filas = len(matriz_a)
    cols = len(matriz_a[0])
    lineas = []
    for i in range(filas):
        for j in range(cols):
            val_a = formatear_numero(matriz_a[i][j])
            val_b = formatear_numero(matriz_b[i][j])
            val_c = formatear_numero(matriz_c[i][j])
            signo_b = f"({val_b})" if matriz_b[i][j] < 0 else val_b
            lineas.append(f"C[{i + 1},{j + 1}] = {val_a} - {signo_b} = {val_c}")
    return lineas


# Funciones de compatibilidad hacia atras
def dibujar_entradas_matriz(
    contenedor,
    titulo,
    filas,
    columnas,
    columna_inicio=0,
    ancho_celda=6,
    color_titulo="#263238",
):
    etiqueta_titulo = tk.Label(
        contenedor,
        text=titulo,
        font=(FUENTE_SANS, 10, "bold"),
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
                font=(FUENTE_MONO, 10),
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
    matriz_numerica = []
    for fila_widgets in cuadricula_entradas:
        fila_valores = []
        for celda in fila_widgets:
            texto_ingresado = celda.get().strip()
            try:
                valor_flotante = float(texto_ingresado)
            except ValueError:
                raise ValueError(
                    f"el valor '{texto_ingresado}' no es un numero valido."
                )
            fila_valores.append(valor_flotante)
        matriz_numerica.append(fila_valores)
    return matriz_numerica


def formatear_matriz_texto(matriz):
    lineas = []
    for fila in matriz:
        elementos_formateados = [formatear_numero(valor) for valor in fila]
        lineas.append("   ".join(f"{item:>7}" for item in elementos_formateados))
    return "\n".join(lineas)
