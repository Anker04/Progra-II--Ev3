import customtkinter as ctk
from tkinter import ttk, messagebox
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from models import Cliente, Ingrediente, Menu, Pedido
from crud.cliente_crud import Cliente_crud
from crud.ingrediente_crud import crear_ingrediente, obtener_ingredientes, actualizar_ingrediente, eliminar_ingrediente
from crud.menu_crud import crear_menu, obtener_menus, actualizar_menu, eliminar_menu
from crud.pedido_crud import crear_pedido, obtener_pedidos, eliminar_pedido
from datetime import datetime

# Configuración de la base de datos
DATABASE_URL = "sqlite:///restaurant.db" 
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
session = Session()

# Configuración inicial de la interfaz
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("green")

class GestionRestauranteApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Gestión de Restaurante")
        self.geometry("800x600")
        self.resizable(False, False)

        # Tabview principal
        self.tab_view = ctk.CTkTabview(self, width=780, height=550)
        self.tab_view.pack(pady=20, padx=10)

        # Crear pestañas
        self.create_clientes_tab()
        self.create_ingredientes_tab()
        self.create_menu_tab()
        self.create_pedidos_tab()

    def create_clientes_tab(self):
        tab = self.tab_view.add("Clientes")

        # Campos de entrada
        ctk.CTkLabel(tab, text="Correo:").grid(row=0, column=0, padx=10, pady=10)
        correo_entry = ctk.CTkEntry(tab)
        correo_entry.grid(row=0, column=1, padx=10, pady=10)

        ctk.CTkLabel(tab, text="Nombre:").grid(row=0, column=2, padx=10, pady=10)
        nombre_entry = ctk.CTkEntry(tab)
        nombre_entry.grid(row=0, column=3, padx=10, pady=10)

        # Botón para agregar cliente
        def agregar_cliente():
            correo = correo_entry.get()
            nombre = nombre_entry.get()

            if not correo or not nombre:
                messagebox.showerror("Error", "Todos los campos son obligatorios.")
                return

            try:
                nuevo_cliente = Cliente_crud.crear_cliente(session, nombre, correo)
                messagebox.showinfo("Éxito", "Cliente agregado correctamente.")
                cargar_clientes()
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo agregar el cliente: {e}")

        ctk.CTkButton(tab, text="Agregar Cliente", command=agregar_cliente).grid(row=0, column=4, padx=10, pady=10)

        # Tabla de clientes
        treeview = ttk.Treeview(tab, columns=("ID", "Correo", "Nombre"), show="headings", height=15)
        treeview.grid(row=1, column=0, columnspan=5, padx=10, pady=10)
        treeview.heading("ID", text="ID")
        treeview.heading("Correo", text="Correo")
        treeview.heading("Nombre", text="Nombre")

        def cargar_clientes():
            for row in treeview.get_children():
                treeview.delete(row)
            clientes = Cliente_crud.obtener_clientes(session)
            for cliente in clientes:
                treeview.insert("", "end", values=(cliente.id, cliente.correo, cliente.nombre))

        cargar_clientes()

    def create_ingredientes_tab(self):
        tab = self.tab_view.add("Ingredientes")

        # Campos de entrada
        ctk.CTkLabel(tab, text="Nombre:").grid(row=0, column=0, padx=10, pady=10)
        nombre_entry = ctk.CTkEntry(tab)
        nombre_entry.grid(row=0, column=1, padx=10, pady=10)

        ctk.CTkLabel(tab, text="Tipo:").grid(row=0, column=2, padx=10, pady=10)
        tipo_entry = ctk.CTkEntry(tab)
        tipo_entry.grid(row=0, column=3, padx=10, pady=10)

        ctk.CTkLabel(tab, text="Cantidad:").grid(row=1, column=0, padx=10, pady=10)
        cantidad_entry = ctk.CTkEntry(tab)
        cantidad_entry.grid(row=1, column=1, padx=10, pady=10)

        ctk.CTkLabel(tab, text="Unidad de Medida:").grid(row=1, column=2, padx=10, pady=10)
        unidad_medida_entry = ctk.CTkEntry(tab)
        unidad_medida_entry.grid(row=1, column=3, padx=10, pady=10)

        # Botón para agregar ingrediente
        def agregar_ingrediente():
            nombre = nombre_entry.get()
            tipo = tipo_entry.get()
            cantidad = cantidad_entry.get()
            unidad_medida = unidad_medida_entry.get()

            if not nombre or not tipo or not cantidad or not unidad_medida:
                messagebox.showerror("Error", "Todos los campos son obligatorios.")
                return

            try:
                nuevo_ingrediente = crear_ingrediente(session, nombre, tipo, float(cantidad), unidad_medida)
                messagebox.showinfo("Éxito", "Ingrediente agregado correctamente.")
                cargar_ingredientes()
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo agregar el ingrediente: {e}")

        ctk.CTkButton(tab, text="Agregar Ingrediente", command=agregar_ingrediente).grid(row=2, column=0, columnspan=4, pady=10)

        # Tabla de ingredientes
        treeview = ttk.Treeview(tab, columns=("ID", "Nombre", "Tipo", "Cantidad", "Unidad de Medida"), show="headings", height=15)
        treeview.grid(row=3, column=0, columnspan=5, padx=10, pady=10)
        treeview.heading("ID", text="ID")
        treeview.heading("Nombre", text="Nombre")
        treeview.heading("Tipo", text="Tipo")
        treeview.heading("Cantidad", text="Cantidad")
        treeview.heading("Unidad de Medida", text="Unidad de Medida")

        def cargar_ingredientes():
            for row in treeview.get_children():
                treeview.delete(row)
            ingredientes = obtener_ingredientes(session)
            for ingrediente in ingredientes:
                treeview.insert("", "end", values=(ingrediente.id, ingrediente.nombre, ingrediente.tipo, ingrediente.cantidad, ingrediente.unidad_medida))

        cargar_ingredientes()

    def create_menu_tab(self):
        tab = self.tab_view.add("Menú")

        # Campos de entrada
        ctk.CTkLabel(tab, text="Nombre:").grid(row=0, column=0, padx=10, pady=10)
        nombre_entry = ctk.CTkEntry(tab)
        nombre_entry.grid(row=0, column=1, padx=10, pady=10)

        ctk.CTkLabel(tab, text="Descripción:").grid(row=0, column=2, padx=10, pady=10)
        descripcion_entry = ctk.CTkEntry(tab)
        descripcion_entry.grid(row=0, column=3, padx=10, pady=10)

        ctk.CTkLabel(tab, text="Precio:").grid(row=1, column=0, padx=10, pady=10)
        precio_entry = ctk.CTkEntry(tab)
        precio_entry.grid(row=1, column=1, padx=10, pady=10)

        # Botón para agregar menú
        def agregar_menu():
            nombre = nombre_entry.get()
            descripcion = descripcion_entry.get()
            precio = precio_entry.get()

            if not nombre or not descripcion or not precio:
                messagebox.showerror("Error", "Todos los campos son obligatorios.")
                return

            try:
                nuevo_menu = crear_menu(session, nombre, descripcion, float(precio))
                messagebox.showinfo("Éxito", "Menú agregado correctamente.")
                cargar_menus()
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo agregar el menú: {e}")

        ctk.CTkButton(tab, text="Agregar Menú", command=agregar_menu).grid(row=1, column=2, columnspan=2, pady=10)

        # Tabla de menús
        treeview = ttk.Treeview(tab, columns=("ID", "Nombre", "Descripción", "Precio"), show="headings", height=15)
        treeview.grid(row=2, column=0, columnspan=4, padx=10, pady=10)
        treeview.heading("ID", text="ID")
        treeview.heading("Nombre", text="Nombre")
        treeview.heading("Descripción", text="Descripción")
        treeview.heading("Precio", text="Precio")

        def cargar_menus():
            for row in treeview.get_children():
                treeview.delete(row)
            menus = obtener_menus(session)
            for menu in menus:
                treeview.insert("", "end", values=(menu.id, menu.nombre, menu.descripcion, menu.precio))

        cargar_menus()

        # Botón para actualizar la lista de menús
        ctk.CTkButton(tab, text="Actualizar Lista", command=cargar_menus).grid(row=3, column=0, columnspan=4, pady=10)

    def create_pedidos_tab(self):
        tab = self.tab_view.add("Pedidos")

        # Campos de entrada
        ctk.CTkLabel(tab, text="Cliente ID:").grid(row=0, column=0, padx=10, pady=10)
        cliente_id_entry = ctk.CTkEntry(tab)
        cliente_id_entry.grid(row=0, column=1, padx=10, pady=10)

        ctk.CTkLabel(tab, text="Total:").grid(row=0, column=2, padx=10, pady=10)
        total_entry = ctk.CTkEntry(tab)
        total_entry.grid(row=0, column=3, padx=10, pady=10)

        # Botón para agregar pedido
        def agregar_pedido():
            cliente_id = cliente_id_entry.get()
            total = total_entry.get()

            if not cliente_id or not total:
                messagebox.showerror("Error", "Todos los campos son obligatorios.")
                return

            try:
                nuevo_pedido = crear_pedido(session, cliente_id, float(total))
                messagebox.showinfo("Éxito", "Pedido agregado correctamente.")
                cargar_pedidos()
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo agregar el pedido: {e}")

        ctk.CTkButton(tab, text="Agregar Pedido", command=agregar_pedido).grid(row=1, column=0, columnspan=4, pady=10)

        # Tabla de pedidos
        treeview = ttk.Treeview(tab, columns=("ID", "Cliente ID", "Fecha", "Total"), show="headings", height=15)
        treeview.grid(row=2, column=0, columnspan=4, padx=10, pady=10)
        treeview.heading("ID", text="ID")
        treeview.heading("Cliente ID", text="Cliente ID")
        treeview.heading("Fecha", text="Fecha")
        treeview.heading("Total", text="Total")

        def cargar_pedidos():
            for row in treeview.get_children():
                treeview.delete(row)
            pedidos = obtener_pedidos(session)
            for pedido in pedidos:
                treeview.insert("", "end", values=(pedido.id, pedido.cliente_id, pedido.fecha_creacion, pedido.total))

        cargar_pedidos()

        # Botón para actualizar la lista de pedidos
        ctk.CTkButton(tab, text="Actualizar Lista", command=cargar_pedidos).grid(row=3, column=0, columnspan=4, pady=10)

if __name__ == "__main__":
    app = GestionRestauranteApp()
    app.mainloop()

