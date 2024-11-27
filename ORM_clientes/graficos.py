import matplotlib.pyplot as plt
from tkinter import Frame

def crear_grafico_ventas(master):
    frame = Frame(master)
    frame.pack(expand=1, fill="both")

    fig, ax = plt.subplots()
    ax.bar(["Enero", "Febrero", "Marzo"], [10, 15, 20])
    ax.set_title("Ventas Mensuales")
    ax.set_xlabel("Mes")
    ax.set_ylabel("Ventas")

    canvas = plt.FigureCanvasTkAgg(fig, master=frame)
    canvas.draw()
    canvas.get_tk_widget().pack(expand=1, fill="both")