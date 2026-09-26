"""
Punto de entrada principal para la aplicación de Sustracción de Matrices.

Ejecución:
    python main.py
"""
import tkinter as tk
from app.frontend.ventana_principal import AplicacionRestaMatrices


def main():
    """Función de inicio que crea la ventana principal y lanza el bucle de eventos."""
    ventana = tk.Tk()
    AplicacionRestaMatrices(ventana)
    ventana.mainloop()


if __name__ == "__main__":
    main()
