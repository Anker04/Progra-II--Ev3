from database import engine
from models import Base
import tkinter as tk
from tkinter import PhotoImage
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
        img = PhotoImage(file=grafico)  # Cargar cada gráfico generado
        label = tk.Label(ventana, image=img)    
        label.grid(row=0, column=i)
        label.image = img  # Guardar referencia a la imagen para que no se borre

    # Iniciar el loop de la interfaz
    ventana.mainloop()

if __name__ == "__main__":
    # Crear las tablas en la base de datos
    print("Creando tablas en la base de datos...")
    Base.metadata.create_all(bind=engine)
    print("Tablas creadas exitosamente.")
    
    # Mostrar los gráficos
    mostrar_graficos()
