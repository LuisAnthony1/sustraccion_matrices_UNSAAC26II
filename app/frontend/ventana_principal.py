# interfaz grafica basica con tkinter para sustraccion de matrices
# unsaac - codigo basico para estudiantes
import tkinter as tk
from tkinter import messagebox
import numpy as np

# clase simple para la ventana de la aplicacion
class AplicacionRestaMatrices:
    def __init__(self, ventana):
        self.ventana = ventana
        self.ventana.title("sustraccion de matrices - unsaac")
        self.ventana.geometry("680x560")
        self.ventana.configure(bg="#f0f0f0")

        # variables para el tamano y el metodo
        self.var_tamano = tk.IntVar(value=2)
        self.var_metodo = tk.StringVar(value="bucles")

        # listas para guardar las casillas entry
        self.entradas_a = []
        self.entradas_b = []

        # titulo principal
        lbl_titulo = tk.Label(
            self.ventana,
            text="sustraccion de matrices (2x2 / 3x3)",
            font=("Arial", 14, "bold"),
            bg="#f0f0f0",
        )
        lbl_titulo.pack(pady=10)

        # marco para seleccionar tamano
        marco_tamano = tk.Frame(self.ventana, bg="#f0f0f0")
        marco_tamano.pack(pady=5)
        tk.Label(marco_tamano, text="tamano:", font=("Arial", 10, "bold"), bg="#f0f0f0").pack(side="left", padx=5)
        tk.Radiobutton(marco_tamano, text="2 x 2", variable=self.var_tamano, value=2, bg="#f0f0f0").pack(side="left")
        tk.Radiobutton(marco_tamano, text="3 x 3", variable=self.var_tamano, value=3, bg="#f0f0f0").pack(side="left")

        # marco para seleccionar metodo
        marco_metodo = tk.Frame(self.ventana, bg="#f0f0f0")
        marco_metodo.pack(pady=5)
        tk.Label(marco_metodo, text="metodo:", font=("Arial", 10, "bold"), bg="#f0f0f0").pack(side="left", padx=5)
        tk.Radiobutton(marco_metodo, text="1. bucles for", variable=self.var_metodo, value="bucles", bg="#f0f0f0").pack(side="left")
        tk.Radiobutton(marco_metodo, text="2. comprension", variable=self.var_metodo, value="comprension", bg="#f0f0f0").pack(side="left")
        tk.Radiobutton(marco_metodo, text="3. numpy", variable=self.var_metodo, value="numpy", bg="#f0f0f0").pack(side="left")

        # boton para crear casillas
        btn_crear = tk.Button(self.ventana, text="crear matrices", command=self.dibujar_entradas, bg="#2196f3", fg="white")
        btn_crear.pack(pady=5)

        # marco para colocar las matrices a y b
        self.marco_matrices = tk.Frame(self.ventana, bg="#f0f0f0")
        self.marco_matrices.pack(pady=10)

        # boton para calcular la resta
        btn_calcular = tk.Button(self.ventana, text="calcular resta (a - b)", command=self.calcular_resta, bg="#4caf50", fg="white", font=("Arial", 10, "bold"))
        btn_calcular.pack(pady=5)

        # marco para el resultado
        self.marco_resultado = tk.Frame(self.ventana, bg="#f0f0f0")
        self.marco_resultado.pack(pady=10)
        self.lbl_resultado = tk.Label(self.marco_resultado, text="", font=("Consolas", 12), bg="#f0f0f0", justify="left")
        self.lbl_resultado.pack()

        # dibujamos las entradas iniciales de 2x2
        self.dibujar_entradas()

    # funcion para dibujar las casillas de entrada en la ventana
    def dibujar_entradas(self):
        # borramos los widgets anteriores
        for w in self.marco_matrices.winfo_children():
            w.destroy()

        n = self.var_tamano.get()
        self.entradas_a = []
        self.entradas_b = []

        # cuadro para la matriz a
        frame_a = tk.Frame(self.marco_matrices, bg="#f0f0f0")
        frame_a.pack(side="left", padx=15)
        tk.Label(frame_a, text="matriz a", font=("Arial", 10, "bold"), bg="#f0f0f0").grid(row=0, columnspan=n, pady=4)

        for i in range(n):
            fila = []
            for j in range(n):
                c = tk.Entry(frame_a, width=6, justify="center")
                c.grid(row=i + 1, column=j, padx=2, pady=2)
                c.insert(0, "0")
                fila.append(c)
            self.entradas_a.append(fila)

        # signo menos en el medio
        tk.Label(self.marco_matrices, text="−", font=("Arial", 20, "bold"), bg="#f0f0f0").pack(side="left", padx=10)

        # cuadro para la matriz b
        frame_b = tk.Frame(self.marco_matrices, bg="#f0f0f0")
        frame_b.pack(side="left", padx=15)
        tk.Label(frame_b, text="matriz b", font=("Arial", 10, "bold"), bg="#f0f0f0").grid(row=0, columnspan=n, pady=4)

        for i in range(n):
            fila = []
            for j in range(n):
                c = tk.Entry(frame_b, width=6, justify="center")
                c.grid(row=i + 1, column=j, padx=2, pady=2)
                c.insert(0, "0")
                fila.append(c)
            self.entradas_b.append(fila)

    # funcion para leer las entradas y calcular la resta
    def calcular_resta(self):
        n = self.var_tamano.get()
        matriz_a = []
        matriz_b = []

        # leemos matriz a
        try:
            for i in range(n):
                fila = []
                for j in range(n):
                    fila.append(float(self.entradas_a[i][j].get()))
                matriz_a.append(fila)
        except:
            messagebox.showerror("error", "ingrese solo numeros en la matriz a")
            return

        # leemos matriz b
        try:
            for i in range(n):
                fila = []
                for j in range(n):
                    fila.append(float(self.entradas_b[i][j].get()))
                matriz_b.append(fila)
        except:
            messagebox.showerror("error", "ingrese solo numeros en la matriz b")
            return

        metodo = self.var_metodo.get()

        # calculamos segun el metodo seleccionado
        if metodo == "bucles":
            matriz_c = []
            for i in range(n):
                fila = []
                for j in range(n):
                    fila.append(matriz_a[i][j] - matriz_b[i][j])
                matriz_c.append(fila)
        elif metodo == "comprension":
            matriz_c = [
                [matriz_a[i][j] - matriz_b[i][j] for j in range(n)]
                for i in range(n)
            ]
        else: # numpy
            arr_a = np.array(matriz_a)
            arr_b = np.array(matriz_b)
            matriz_c = (arr_a - arr_b).tolist()

        # mostramos el resultado en el label
        texto = "matriz resultado c:\n"
        for i in range(n):
            for j in range(n):
                val = matriz_c[i][j]
                if val.is_integer():
                    val = int(val)
                texto += f"{val}\t"
            texto += "\n"

        self.lbl_resultado.config(text=texto)
