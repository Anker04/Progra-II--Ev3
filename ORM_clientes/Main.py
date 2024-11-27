from database import engine
from models import Base
import tkinter as tk
from PIL import Image, ImageTk  # Usamos Pillow para manejar imágenes .png
from graficos import obtener_graficos

def mostrar_graficos():
    """
    Función para mostrar los gráficos generados en una ventana de Tkinter.
    """
    # Llamamos a la función de obtener gráficos
    graficos = obtener_graficos()

    # Crear ventana de tkinter
    ventana = tk.Tk()
    ventana.title("Gráficos del Restaurante")

    # Mostrar los gráficos en la ventana
    for i, grafico in enumerate(graficos):
        # Abrir la imagen generada con Pillow
        imagen = Image.open(grafico)
        imagen_tk = ImageTk.PhotoImage(imagen)  # Convertirla a formato que Tkinter pueda mostrar

        # Crear un Label para cada imagen y mostrarla
        label = tk.Label(ventana, image=imagen_tk)    
        label.grid(row=0, column=i, padx=10, pady=10)  # Acomodar las imágenes en una fila
        label.image = imagen_tk  # Guardar referencia a la imagen para que no se borre

    # Iniciar el loop de la interfaz
    ventana.mainloop()

def crear_tablas():
    """
    Crear las tablas en la base de datos.
    """
    print("Creando tablas en la base de datos...")
    Base.metadata.create_all(bind=engine)
    print("Tablas creadas exitosamente.")

if __name__ == "__main__":
    # Primero, crear las tablas en la base de datos
    crear_tablas()

    # Luego, mostrar los gráficos
    mostrar_graficos()
