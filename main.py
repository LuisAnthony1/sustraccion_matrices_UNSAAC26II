# punto de entrada principal para la aplicacion de sustraccion de matrices
# ejecucion: python main.py

import tkinter as tk
from app.frontend.ventana_principal import AplicacionRestaMatrices

# funcion de inicio que crea la ventana principal y lanza el bucle de eventos
def main():
    # creacion de la ventana raiz de tkinter
    ventana = tk.Tk()
    # inicializacion de la aplicacion de interfaz grafica
    AplicacionRestaMatrices(ventana)
    # ejecucion del bucle principal de escucha de eventos
    ventana.mainloop()

# verificacion de ejecucion directa del archivo
if __name__ == "__main__":
    main()
