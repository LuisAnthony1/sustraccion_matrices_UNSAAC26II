# Sustracción de Matrices en Python con Tkinter

Aplicación en Python para la **sustracción de matrices** de cualquier dimensión $m \times n$ (hasta $25 \times 25$ en la interfaz gráfica), implementada con **tres métodos distintos**:

1. **Bucles `for` anidados**: recorrido explícito, casilla por casilla.
2. **Comprensión de listas**: la misma lógica en una sola expresión.
3. **Vectorización con NumPy**: la resta se hace sobre el arreglo completo, en código compilado.

El proyecto tiene dos partes independientes:

- **Backend**: cuatro programas de consola, uno por método y un menú que los reúne.
- **Frontend**: una interfaz gráfica en Tkinter para editar las matrices, elegir el método y ver el resultado con su memoria de cálculo.

---

## 📐 Fundamento matemático

La resta $A - B$ solo está definida si ambas matrices tienen **la misma dimensión** (igual número de filas y de columnas). El resultado $C$ se obtiene restando las entradas que ocupan la misma posición:

$$C_{i,j} = A_{i,j} - B_{i,j} \quad \forall \, i \in \{1, \dots, m\}, \; j \in \{1, \dots, n\}$$

### Ejemplo ($2 \times 2$)

$$A = \begin{pmatrix} 5 & 3 \\ 2 & 8 \end{pmatrix}, \quad B = \begin{pmatrix} 1 & 1 \\ 4 & 2 \end{pmatrix}$$

$$C = A - B = \begin{pmatrix} 5-1 & 3-1 \\ 2-4 & 8-2 \end{pmatrix} = \begin{pmatrix} 4 & 2 \\ -2 & 6 \end{pmatrix}$$

---

## 🏛️ Estructura del proyecto

```text
sustraccion_matrices_UNSAAC26II/
├── main.py                      ← punto de entrada de la interfaz gráfica
├── requirements.txt             ← dependencia: numpy
├── README.md
│
└── app/
    ├── __init__.py
    │
    ├── backend/                 ← PROGRAMAS DE CONSOLA (se ejecutan por separado)
    │   ├── __init__.py
    │   ├── metodo_bucles.py         → Método 1: bucles for anidados, con el paso a paso
    │   ├── metodo_comprension.py    → Método 2: comprensión de listas
    │   ├── metodo_numpy.py          → Método 3: vectorización con NumPy
    │   └── registro.py              → menú: elegir un método o comparar los 3
    │
    └── frontend/                ← INTERFAZ GRÁFICA (Tkinter)
        ├── __init__.py              → reexporta la API pública del frontend
        ├── calculo.py               → algoritmos de resta y formato (sin Tkinter)
        ├── widgets_matriz.py        → componentes: CajaDesplazable, CuadriculaMatriz, crear_boton
        └── ventana_principal.py     → clase AplicacionRestaMatrices (ventana principal)
```

### Cómo se reparten las responsabilidades

| Módulo | Qué contiene | ¿Usa Tkinter? |
| :--- | :--- | :---: |
| `backend/metodo_*.py` | Programas de consola: piden los datos con `input()`, validan y muestran el resultado | No |
| `backend/registro.py` | Menú de consola para usar un método o comparar los tres | No |
| `frontend/calculo.py` | Funciones puras: `restar_matrices_bucles`, `restar_matrices_comprension`, `restar_matrices_numpy`, el diccionario `METODOS`, `calcular_resta_metodo` y `generar_paso_a_paso` | No |
| `frontend/widgets_matriz.py` | `CajaDesplazable` (lienzo con corchetes y barras de desplazamiento), `CuadriculaMatriz` (matriz editable), `EntradaCeldaMatriz`, `crear_boton` y la paleta de colores | Sí |
| `frontend/ventana_principal.py` | `AplicacionRestaMatrices`: organiza la ventana y responde a las acciones del usuario | Sí |

- **Los programas del backend son independientes**: cada uno se ejecuta por separado desde la consola y no los importa la interfaz gráfica.
- **Los cálculos de la interfaz están separados de lo visual**: `calculo.py` no importa Tkinter, así que sus funciones se pueden usar o probar sin abrir ventanas. Además, validan que las matrices no estén vacías y que tengan la misma dimensión (`ValueError` si no se cumple).
- **El método se elige con un diccionario**: `METODOS = {"bucles": ..., "comprension": ..., "numpy": ...}` relaciona el valor del botón de opción con la función que calcula, sin cadenas de `if/elif`.
- **Los componentes visuales se reutilizan**: las matrices A, B y C usan la misma `CajaDesplazable`, y todos los botones se crean con `crear_boton`.

---

## ⚙️ Comparativa de los 3 métodos

| Criterio | Método 1: Bucles anidados | Método 2: Comprensión de listas | Método 3: NumPy |
| :--- | :--- | :--- | :--- |
| **Programa de consola** | `metodo_bucles.py` | `metodo_comprension.py` | `metodo_numpy.py` |
| **Función en la interfaz** | `restar_matrices_bucles()` | `restar_matrices_comprension()` | `restar_matrices_numpy()` |
| **Estilo** | Imperativo: recorrido explícito | Declarativo: una expresión | Vectorizado: `A - B` sobre el arreglo |
| **Dependencias** | Ninguna | Ninguna | `numpy` |
| **Complejidad** | $\Theta(m \cdot n)$ | $\Theta(m \cdot n)$ | $\Theta(m \cdot n)$ |
| **Rendimiento** | Adecuado para matrices pequeñas | Un poco más rápido que los bucles | El más rápido en matrices grandes, si los datos se mantienen como `ndarray` |
| **Valor didáctico** | Muestra cada paso con sus índices `i, j` | Sintaxis idiomática de Python | Concepto de vectorización |

> En la interfaz (hasta $25 \times 25$) los tres métodos tardan menos de 0,1 ms, así que elegir uno u otro tiene un fin didáctico.

---

## 📋 Requisitos

- **Python** 3.8 o superior.
- **Tkinter**: viene incluido con Python en Windows y macOS. En Debian/Ubuntu: `sudo apt-get install python3-tk`.
- **NumPy** `>= 1.20.0` (lo usan el Método 3 y la interfaz).

---

## 🚀 Instalación

```bash
git clone https://github.com/LuisAnthony1/sustraccion_matrices_UNSAAC26II.git
cd sustraccion_matrices_UNSAAC26II
```

Crear y activar un entorno virtual (recomendado):

- **Windows (PowerShell / CMD):**

  ```powershell
  python -m venv venv
  .\venv\Scripts\activate
  ```

- **Linux / macOS:**

  ```bash
  python3 -m venv venv
  source venv/bin/activate
  ```

Instalar dependencias:

```bash
pip install -r requirements.txt
```

---

## 🖥️ Uso de la interfaz gráfica

```bash
python main.py
```

1. **Dimensión**: escribe las filas y las columnas (de 1 a 25) y pulsa **Generar** o `Enter`. Si dejas vacías las columnas, se genera una matriz cuadrada. También se admiten matrices rectangulares, por ejemplo $2 \times 5$.
2. **Método**: elige `1. Bucles for`, `2. Comprensión` o `3. NumPy`.
3. **Datos**: escribe los valores de la **Matriz A** (minuendo) y de la **Matriz B** (sustraendo). Se aceptan enteros, decimales, negativos y notación científica (`1e3`).
   - Las flechas `↑ ↓ ← →` mueven el cursor entre casillas (al llegar al borde pasa al lado opuesto) y `Enter` avanza a la derecha.
   - La rueda del ratón desplaza las matrices grandes; con `Shift` + rueda se desplaza en horizontal.
4. **Calcular**: pulsa **Calcular sustracción (A − B)**. Se muestran:
   - la **Matriz C** resultante;
   - la **memoria de cálculo**, con una línea por casilla, por ejemplo `C[2,1] = 2 - (-4) = 6`.
5. **Copiar**: el botón *Copiar* de la Matriz C la copia separada por tabulaciones, lista para pegar en Excel o Google Sheets. El de la memoria copia todo el paso a paso.

**Validaciones**: si una casilla no contiene un número, se marca en rojo y aparece un mensaje con la matriz y la posición del error. Si la dimensión no es un entero entre 1 y 25, se muestra un mensaje explicando el problema.

---

## ⌨️ Uso de los programas de consola

Cada programa pide las dimensiones y los valores de A y B, y vuelve a preguntar si el dato no es válido:

```bash
python app/backend/metodo_bucles.py        # Método 1, muestra c[i][j] = a - b paso a paso
python app/backend/metodo_comprension.py   # Método 2, muestra la evaluación fila por fila
python app/backend/metodo_numpy.py         # Método 3, muestra los arreglos de NumPy
python app/backend/registro.py             # menú: elegir un método (1-3) o comparar los 3 (4)
```

La opción **4** de `registro.py` ejecuta los tres métodos sobre los mismos datos e indica si los tres resultados coinciden.

---

## 🧪 Verificación rápida sin interfaz

Las funciones de `app/frontend/calculo.py` no usan Tkinter y se pueden probar directamente:

```python
from app.frontend.calculo import METODOS, calcular_resta_metodo, generar_paso_a_paso

A = [[5, 3], [2, 8]]
B = [[1, 1], [4, 2]]

for metodo in METODOS:
    print(metodo, calcular_resta_metodo(A, B, metodo))
# bucles       [[4, 2], [-2, 6]]
# comprension  [[4, 2], [-2, 6]]
# numpy        [[4.0, 2.0], [-2.0, 6.0]]

print(generar_paso_a_paso(A, B, calcular_resta_metodo(A, B, "bucles")))
# ['C[1,1] = 5 - 1 = 4', 'C[1,2] = 3 - 1 = 2', 'C[2,1] = 2 - 4 = -2', 'C[2,2] = 8 - 2 = 6']
```

---

## 📄 Licencia y créditos

Proyecto desarrollado con fines educativos (UNSAAC, semestre 2026-II) para el aprendizaje del álgebra lineal computacional y del diseño estructurado en Python.
