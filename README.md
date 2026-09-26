# Sustracción de Matrices en Python con Tkinter

Aplicación modular en Python para la **sustracción de matrices cuadradas** ($2 \times 2$, $3 \times 3$ y dimensiones arbitrarias $N \times N$) implementada mediante tres algoritmos distintos bajo una arquitectura desacoplada en **Backend** (lógica pura), **Frontend** (interfaz gráfica con Tkinter) y **Pruebas Automatizadas** (pruebas unitarias).

Proyecto basado en la guía técnica *Sustracción de Matrices — Python · Tkinter · Programación Estructurada*.

---

## 📐 Fundamento Matemático

La sustracción de dos matrices $A$ y $B$ únicamente es válida si ambas poseen exactamente la misma dimensión (igual cantidad de filas e igual cantidad de columnas). La matriz resultante $C = A - B$ se obtiene restando individualmente cada celda en la misma posición:

$$C_{i,j} = A_{i,j} - B_{i,j} \quad \forall \, i \in \{0, \dots, \text{filas}-1\}, \; j \in \{0, \dots, \text{columnas}-1\}$$

### Ejemplo numérico ($2 \times 2$):

$$A = \begin{pmatrix} 5 & 3 \\ 2 & 8 \end{pmatrix}, \quad B = \begin{pmatrix} 1 & 1 \\ 4 & 2 \end{pmatrix}$$

$$C = A - B = \begin{pmatrix} 5-1 & 3-1 \\ 2-4 & 8-2 \end{pmatrix} = \begin{pmatrix} 4 & 2 \\ -2 & 6 \end{pmatrix}$$

---

## 🏛️ Arquitectura del Proyecto

El código está estructurado siguiendo el principio de responsabilidad única y separación de capas:

```text
resta_matrices/
├── main.py                      ← Punto de entrada único (python main.py)
├── requirements.txt             ← Dependencias del proyecto (numpy)
├── README.md                    ← Documentación completa, instalación y ejecución
├── .gitignore                   ← Exclusiones de Git para Python y entornos
│
├── app/                         ← Paquete principal de la aplicación
│   ├── __init__.py
│   │
│   ├── backend/                 ← LÓGICA PURA (sin Tkinter, sin pantalla)
│   │   ├── __init__.py
│   │   ├── metodo_bucles.py         → restar_matrices_bucles()
│   │   ├── metodo_comprension.py    → restar_matrices_comprension()
│   │   ├── metodo_numpy.py          → restar_matrices_numpy()
│   │   └── registro.py              → Diccionario METODOS {clave: función}
│   │
│   └── frontend/                ← INTERFAZ DE USUARIO (Tkinter)
│       ├── __init__.py
│       ├── ventana_principal.py     → Clase AplicacionRestaMatrices
│       └── widgets_matriz.py        → Funciones que dibujan y leen los Entry de una matriz
│
└── tests/                       ← PRUEBAS AUTOMÁTICAS (sin interfaz gráfica)
    ├── __init__.py
    └── test_backend.py          ← Suite de pruebas unitarias con unittest
```

### Principios de Diseño:
- **Backend Puro**: Las funciones de cálculo matemático no importan `tkinter` ni interactúan con la pantalla; reciben listas estándar de Python y retornan listas estándar.
- **Frontend Modular**: La construcción de las casillas de entrada (`Entry`) y la lectura/validación de números está encapsulada en `widgets_matriz.py`, manteniendo limpia la clase `AplicacionRestaMatrices`.
- **Estrategia Desacoplada (`registro.py`)**: El diccionario `METODOS` asocia el identificador de cada algoritmo con su función real, permitiendo seleccionar dinámicamente el backend sin cadenas repetitivas de `if/elif`.
- **Totalmente en Español**: Toda la arquitectura, nombres de módulos, funciones, variables, mensajes de error y comentarios están escritos íntegramente en español.

---

## ⚙️ Comparativa de los 3 Métodos de Cálculo

| Criterio | Método 1: Bucles Anidados | Método 2: Comprensión de Listas | Método 3: Vectorización NumPy |
| :--- | :--- | :--- | :--- |
| **Módulo** | `metodo_bucles.py` | `metodo_comprension.py` | `metodo_numpy.py` |
| **Función** | `restar_matrices_bucles()` | `restar_matrices_comprension()` | `restar_matrices_numpy()` |
| **Líneas de código** | Varias (recorrido explícito) | Compacto (1 expresión) | Muy compacto |
| **Pedagogía** | Máxima: muestra el paso a paso | Sintaxis idiomática de Python | Concepto de vectorización profesional |
| **Dependencias** | Ninguna (Python puro) | Ninguna (Python puro) | Requiere biblioteca `numpy` |
| **Rendimiento** | Adecuado para matrices pequeñas | Similar a bucles, más óptimo | Altamente optimizado en C (para matrices grandes) |
| **Visualización del flujo** | Casilla por casilla con índices `i, j` | Flujo implícito en una línea | Delegado al motor compilado de NumPy |

---

## 📋 Requisitos Previos

- **Python**: Versión 3.8 o superior (compatible con Python 3.10, 3.11, 3.12, 3.13, 3.14+).
- **Tkinter**: Incluido de manera predeterminada en las instalaciones estándar de Python para Windows y macOS. *(En distribuciones Linux tipo Debian/Ubuntu, instalar con: `sudo apt-get install python3-tk`)*.
- **NumPy**: Biblioteca para el Método 3 (`numpy>=1.20.0`).

---

## 🚀 Instalación y Puesta en Marcha

### 1. Clonar o acceder al repositorio
Abre una terminal en la carpeta del proyecto:
```bash
cd sustraccion_matrices_USAAC26II
```

### 2. Crear y activar un entorno virtual (recomendado)

- **En Windows (PowerShell / CMD):**
  ```powershell
  python -m venv venv
  .\venv\Scripts\activate
  ```

- **En Linux / macOS:**
  ```bash
  python3 -m venv venv
  source venv/bin/activate
  ```

### 3. Instalar dependencias
Instala la biblioteca NumPy desde el archivo de requerimientos:
```bash
pip install -r requirements.txt
```

---

## 🖥️ Cómo Ejecutar la Aplicación

Para iniciar la interfaz gráfica de usuario, ejecuta el punto de entrada único:

```bash
python main.py
```

### Guía de Uso en Pantalla:
1. **Elegir el tamaño de la matriz**:
   - Selecciona `2 × 2` o `3 × 3`.
   - O bien marca `N × N (Personalizado)` e ingresa un número entero positivo en la casilla adyacente (por ejemplo: `4`, `5`).
2. **Seleccionar el método de sustracción**:
   - `1) Bucles Anidados (for)`
   - `2) Comprensión de Listas`
   - `3) Vectorización NumPy`
3. **Generar cuadrícula**:
   - Haz clic en **Generar Cuadrícula de Matrices**.
4. **Ingresar valores numéricos**:
   - Escribe los números correspondientes a la **Matriz A** (minuendo) y la **Matriz B** (sustraendo).
   - O haz clic en **Cargar Valores de Ejemplo** para poblar las matrices con datos de prueba automáticamente.
5. **Calcular la resta**:
   - Presiona **Calcular Sustracción (A − B)**.
   - En el panel inferior se presentará la **Matriz Diferencia Resultante** debidamente alineada y el método específico utilizado para calcularla.

---

## 🧪 Pruebas Unitarias Automatizadas

Las pruebas unitarias validan la precisión matemática de los tres algoritmos, la coherencia de resultados entre ellos y el manejo de excepciones, **sin necesidad de abrir ventanas gráficas**:

Para ejecutar la suite completa de pruebas:

```bash
python -m unittest discover tests
```

O directamente sobre el archivo de pruebas:

```bash
python tests/test_backend.py
```

### Casos cubiertos en la suite:
- ✅ **Caso base $2 \times 2$**: Comprueba el resultado con los valores del manual ($A - B = [[4, 2], [-2, 6]]$) en los tres métodos.
- ✅ **Caso $3 \times 3$**: Comprueba operaciones sobre matrices $3 \times 3$.
- ✅ **Caso $N \times N$ arbitrario**: Comprueba equivalencia matemática idéntica entre los tres métodos en matrices $4 \times 4$.
- ✅ **Números negativos y decimales flotantes**: Valida la precisión con valores reales y signos negativos.
- ✅ **Validación de errores por dimensiones incompatibles**: Comprueba que dimensiones no coincidentes lancen `ValueError`.
- ✅ **Validación de matrices vacías**: Lanza `ValueError` adecuadamente.
- ✅ **Integridad del registro**: Verifica que el diccionario `METODOS` despache las funciones esperadas y controle claves inválidas.

---

## 📄 Licencia y Créditos

Desarrollado con fines educativos y de ingeniería de software para el aprendizaje de álgebra lineal computacional y diseño estructurado en Python.
