# modulo de componentes graficos reutilizables para matrices en tkinter
# componentes minimalistas con cajas desplazables (boxes movibles) para matrices
import tkinter as tk

# reexportados para mantener compatibilidad con codigo que los importaba desde aqui
from app.frontend.calculo import (  # noqa: F401
    calcular_resta_metodo,
    formatear_matriz_texto,
    formatear_numero,
    generar_paso_a_paso,
)

# paleta de diseno minimalista, sobria y limpia
COLORES = {
    "fondo_ventana": "#f8fafc",      # Slate 50
    "fondo_tarjeta": "#ffffff",      # Blanco puro
    "borde_tarjeta": "#e2e8f0",      # Slate 200
    "texto_principal": "#0f172a",    # Slate 900
    "texto_secundario": "#475569",   # Slate 600
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


def calcular_ancho_celda(columnas):
    """Ancho en caracteres de cada casilla: mas estrecho cuando hay muchas columnas."""
    return 4 if columnas > 4 else 5


def crear_boton(contenedor, texto, comando, primario=False, fuente=None, padx=8, pady=1):
    """Crea un boton plano con efecto hover; primario (azul) o secundario (gris)."""
    tipo = "boton_primario" if primario else "boton_secundario"
    normal = COLORES[tipo]
    hover = COLORES[f"{tipo}_hover"]
    color_texto = COLORES[f"{tipo}_texto"]

    boton = tk.Button(
        contenedor,
        text=texto,
        font=fuente or (FUENTE_SANS, 8),
        bg=normal,
        fg=color_texto,
        activebackground=hover,
        activeforeground=color_texto,
        relief="flat",
        padx=padx,
        pady=pady,
        cursor="hand2",
        command=comando,
    )
    boton.color_normal = normal
    boton.color_hover = hover
    boton.bind("<Enter>", lambda _e: boton.config(bg=hover))
    boton.bind("<Leave>", lambda _e: boton.config(bg=normal))
    return boton


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

    def marcar_error(self):
        self.marco_borde.config(bg=COLORES["error_texto"])

    def obtener_texto(self):
        return self.entry.get().strip()

    def establecer_texto(self, texto):
        self.entry.delete(0, tk.END)
        self.entry.insert(0, str(texto))


class CajaDesplazable:
    """Caja con corchetes [ ] cuyo contenido se centra si cabe y se desplaza si no.

    Ocupa la fila `fila` (canvas) y `fila + 1` (barra horizontal) de la rejilla del
    contenedor, en las columnas 0 (canvas) y 1 (barra vertical). Los widgets de la
    matriz se colocan con grid dentro de `self.marco_grid`.
    """

    def __init__(self, contenedor, fila=0, bg=None):
        self.contenedor = contenedor
        self.fila = fila
        fondo = bg or COLORES["fondo_tarjeta"]

        contenedor.grid_rowconfigure(fila, weight=1)
        contenedor.grid_columnconfigure(0, weight=1)

        # canvas para viewport desplazable (box movible)
        self.canvas = tk.Canvas(contenedor, bg=fondo, highlightthickness=0, bd=0)
        self.canvas.grid(row=fila, column=0, sticky="nsew")

        # barras de desplazamiento: solo se muestran cuando el contenido no cabe
        self.hbar = tk.Scrollbar(contenedor, orient="horizontal", command=self.canvas.xview)
        self.vbar = tk.Scrollbar(contenedor, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(xscrollcommand=self.hbar.set, yscrollcommand=self.vbar.set)

        # marco algebraico interior montado en el canvas: [ grid ]
        self.marco_algebraico = tk.Frame(self.canvas, bg=fondo)
        self.win_id = self.canvas.create_window((0, 0), window=self.marco_algebraico, anchor="nw")

        self.lbl_corchete_izq = tk.Label(
            self.marco_algebraico,
            text="[",
            font=(FUENTE_MONO, 24, "normal"),
            bg=fondo,
            fg=COLORES["corchete_color"],
        )
        self.lbl_corchete_izq.pack(side="left", padx=(0, 2))

        self.marco_grid = tk.Frame(self.marco_algebraico, bg=fondo)
        self.marco_grid.pack(side="left")

        self.lbl_corchete_der = tk.Label(
            self.marco_algebraico,
            text="]",
            font=(FUENTE_MONO, 24, "normal"),
            bg=fondo,
            fg=COLORES["corchete_color"],
        )
        self.lbl_corchete_der.pack(side="left", padx=(2, 0))

        # eventos de reconfiguracion de tamano y desplazamiento
        self.canvas.bind("<Configure>", self.ajustar)
        self.marco_algebraico.bind("<Configure>", self.ajustar)

        for widget in (self.canvas, self.marco_algebraico, self.lbl_corchete_izq,
                       self.marco_grid, self.lbl_corchete_der):
            self.vincular_rueda_mouse(widget)

    def vincular_rueda_mouse(self, widget):
        """Permite mover el contenido con la rueda del raton (shift = horizontal)."""
        def pasos(event):
            # linux envia botones 4/5; windows multiplos de 120; macos valores pequenos
            if getattr(event, "num", None) == 4:
                return -1
            if getattr(event, "num", None) == 5:
                return 1
            if not event.delta:
                return 0
            return -int(event.delta / 120) or (-1 if event.delta > 0 else 1)

        def scroll_v(event):
            self.canvas.yview_scroll(pasos(event), "units")

        def scroll_h(event):
            self.canvas.xview_scroll(pasos(event), "units")

        widget.bind("<MouseWheel>", scroll_v)
        widget.bind("<Shift-MouseWheel>", scroll_h)
        widget.bind("<Button-4>", scroll_v)
        widget.bind("<Button-5>", scroll_v)
        widget.bind("<Shift-Button-4>", scroll_h)
        widget.bind("<Shift-Button-5>", scroll_h)

    def ajustar_corchetes(self, filas):
        """Escala los corchetes segun el numero de filas (entre 18 y 48 pt)."""
        tamano = max(18, min(48, 16 + (filas - 1) * 8))
        self.lbl_corchete_izq.config(font=(FUENTE_MONO, tamano, "normal"))
        self.lbl_corchete_der.config(font=(FUENTE_MONO, tamano, "normal"))

    def limpiar(self):
        """Destruye todos los widgets colocados dentro de la rejilla."""
        for widget in self.marco_grid.winfo_children():
            widget.destroy()

    def ajustar(self, _event=None):
        """Ajusta las barras de desplazamiento y centra el contenido si cabe completamente."""
        self.contenedor.update_idletasks()
        cw = self.marco_algebraico.winfo_reqwidth()
        ch = self.marco_algebraico.winfo_reqheight()
        can_w = self.canvas.winfo_width()
        can_h = self.canvas.winfo_height()

        if can_w <= 1 or can_h <= 1:
            return

        # scrollbar horizontal: se activa si el contenido es mas ancho que el viewport
        if cw > can_w:
            self.hbar.grid(row=self.fila + 1, column=0, sticky="ew")
            pos_x = 0
        else:
            self.hbar.grid_forget()
            self.canvas.xview_moveto(0)
            pos_x = max(0, (can_w - cw) // 2)

        # scrollbar vertical: se activa si el contenido es mas alto que el viewport
        if ch > can_h:
            self.vbar.grid(row=self.fila, column=1, sticky="ns")
            pos_y = 0
        else:
            self.vbar.grid_forget()
            self.canvas.yview_moveto(0)
            pos_y = max(0, (can_h - ch) // 2)

        self.canvas.coords(self.win_id, pos_x, pos_y)
        self.canvas.configure(
            scrollregion=(0, 0, max(can_w, cw + pos_x), max(can_h, ch + pos_y))
        )

    def asegurar_visibilidad(self, widget):
        """Desplaza la caja para que el widget indicado (dentro de marco_grid) sea visible."""
        self.contenedor.update_idletasks()
        can_w = self.canvas.winfo_width()
        can_h = self.canvas.winfo_height()
        if can_w <= 1 or can_h <= 1:
            return

        cx = widget.winfo_x() + self.marco_grid.winfo_x()
        cw = widget.winfo_width()
        cy = widget.winfo_y() + self.marco_grid.winfo_y()
        ch = widget.winfo_height()

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


class CuadriculaMatriz:
    """Matriz editable (A o B) dentro de una tarjeta con caja desplazable."""

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

        # cabecera
        self.lbl_titulo = tk.Label(
            self.tarjeta,
            text=self.titulo,
            font=(FUENTE_SANS, 10, "bold"),
            bg=COLORES["fondo_tarjeta"],
            fg=COLORES["texto_principal"],
        )
        self.lbl_titulo.grid(row=0, column=0, sticky="w", pady=(0, 4))

        # caja desplazable con corchetes en la fila 1 de la tarjeta
        self.caja = CajaDesplazable(self.tarjeta, fila=1)

        self.construir_celdas(filas, columnas)

    def construir_celdas(self, filas, columnas):
        """Reconstruye las casillas segun las filas y columnas indicadas, rellenas de 0."""
        self.filas = max(1, int(filas))
        self.columnas = max(1, int(columnas))

        self.caja.limpiar()
        self.celdas.clear()
        self.caja.ajustar_corchetes(self.filas)

        ancho_celda = calcular_ancho_celda(self.columnas)

        for i in range(self.filas):
            fila_widgets = []
            for j in range(self.columnas):
                celda = EntradaCeldaMatriz(
                    self.caja.marco_grid,
                    fila=i,
                    columna=j,
                    ancho=ancho_celda,
                    al_enfocar_cb=lambda c: self.caja.asegurar_visibilidad(c.marco_borde),
                )
                celda.marco_borde.grid(row=i, column=j, padx=2, pady=2)
                self._vincular_teclado(celda, i, j)
                self.caja.vincular_rueda_mouse(celda.entry)
                fila_widgets.append(celda)
            self.celdas.append(fila_widgets)

        self.caja.ajustar()

    def _vincular_teclado(self, celda, i, j):
        """Flechas mueven el foco de forma circular; enter avanza a la derecha."""
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
        """Lee las casillas como lista de listas de float; marca en rojo la invalida."""
        matriz = []
        for i, fila in enumerate(self.celdas):
            fila_num = []
            for j, celda in enumerate(fila):
                texto = celda.obtener_texto()
                try:
                    valor = float(texto)
                except ValueError:
                    celda.marcar_error()
                    celda.entry.focus_set()
                    raise ValueError(
                        f"En {self.titulo}, posición ({i + 1}, {j + 1}): '{texto}' no es un número válido."
                    ) from None
                fila_num.append(valor)
            matriz.append(fila_num)
        return matriz

    def establecer_matriz(self, datos):
        """Escribe una matriz numerica en las casillas (recorta si no coincide el tamano)."""
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
# Funciones de compatibilidad hacia atras (interfaz anterior sin CuadriculaMatriz)
# ---------------------------------------------------------------------------
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
    for i, fila_widgets in enumerate(cuadricula_entradas):
        fila_valores = []
        for j, celda in enumerate(fila_widgets):
            texto_ingresado = celda.get().strip()
            try:
                valor_flotante = float(texto_ingresado)
            except ValueError:
                raise ValueError(
                    f"Posición ({i + 1}, {j + 1}): '{texto_ingresado}' no es un número válido."
                ) from None
            fila_valores.append(valor_flotante)
        matriz_numerica.append(fila_valores)
    return matriz_numerica
