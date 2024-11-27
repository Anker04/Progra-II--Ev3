import customtkinter as ctk
from tkinter import ttk, messagebox
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine


# Importando las clases CRUD de cada entidad
from crud.cliente_crud import ClienteCrud
from crud.ingrediente_crud import IngredienteCrud  # Correcto, importamos la clase
from crud.menu_crud import MenuCrud  # Importamos la clase que contiene los métodos estáticos
from crud.pedido_crud import PedidoCrud  # Asegúrate de importar la clase CRUD de Pedido

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

        # Función para agregar cliente
        def agregar_cliente():
            correo = correo_entry.get()
            nombre = nombre_entry.get()

            if not correo or not nombre:
                messagebox.showerror("Error", "Todos los campos son obligatorios.")
                return

            try:
                nuevo_cliente = ClienteCrud.crear_cliente(session, nombre, correo)
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
            clientes = ClienteCrud.obtener_clientes(session)
            for cliente in clientes:
                treeview.insert("", "end", values=(cliente.id, cliente.correo, cliente.nombre))

        cargar_clientes()

        # Botón de eliminar cliente
        def eliminar_cliente():
            selected_item = treeview.selection()
            if selected_item:
                cliente_id = treeview.item(selected_item)["values"][0]
                try:
                    ClienteCrud.eliminar_cliente(session, cliente_id)
                    messagebox.showinfo("Éxito", "Cliente eliminado correctamente.")
                    cargar_clientes()
                except Exception as e:
                    messagebox.showerror("Error", f"No se pudo eliminar el cliente: {e}")
            else:
                messagebox.showwarning("Advertencia", "Debe seleccionar un cliente para eliminar.")

        ctk.CTkButton(tab, text="Eliminar Cliente", command=eliminar_cliente).grid(row=2, column=0, padx=10, pady=10)

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

        # Función para agregar ingrediente
        def agregar_ingrediente():
            nombre = nombre_entry.get()
            tipo = tipo_entry.get()
            cantidad = cantidad_entry.get()
            unidad_medida = unidad_medida_entry.get()

            if not nombre or not tipo or not cantidad or not unidad_medida:
                messagebox.showerror("Error", "Todos los campos son obligatorios.")
                return

            try:
                nuevo_ingrediente = IngredienteCrud.crear_ingrediente(session, nombre, tipo, float(cantidad), unidad_medida)
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
            ingredientes = IngredienteCrud.obtener_ingredientes(session)
            for ingrediente in ingredientes:
                treeview.insert("", "end", values=(ingrediente.id, ingrediente.nombre, ingrediente.tipo, ingrediente.cantidad, ingrediente.unidad_medida))

        cargar_ingredientes()

        # Botón de eliminar ingrediente
        def eliminar_ingrediente():
            selected_item = treeview.selection()
            if selected_item:
                ingrediente_id = treeview.item(selected_item)["values"][0]
                try:
                    IngredienteCrud.eliminar_ingrediente(session, ingrediente_id)
                    messagebox.showinfo("Éxito", "Ingrediente eliminado correctamente.")
                    cargar_ingredientes()
                except Exception as e:
                    messagebox.showerror("Error", f"No se pudo eliminar el ingrediente: {e}")
            else:
                messagebox.showwarning("Advertencia", "Debe seleccionar un ingrediente para eliminar.")

        ctk.CTkButton(tab, text="Eliminar Ingrediente", command=eliminar_ingrediente).grid(row=4, column=0, padx=10, pady=10)

    def create_menu_tab(self):
        tab = self.tab_view.add("Menú")

        # Campos de entrada
        ctk.CTkLabel(tab, text="Nombre:").grid(row=0, column=0, padx=10, pady=10)
        nombre_entry = ctk.CTkEntry(tab)
        nombre_entry.grid(row=0, column=1, padx=10, pady=10)

        ctk.CTkLabel(tab, text="Descripción:").grid(row=1, column=0, padx=10, pady=10)
        descripcion_entry = ctk.CTkEntry(tab)
        descripcion_entry.grid(row=1, column=1, padx=10, pady=10)

        ctk.CTkLabel(tab, text="Precio:").grid(row=2, column=0, padx=10, pady=10)
        precio_entry = ctk.CTkEntry(tab)
        precio_entry.grid(row=2, column=1, padx=10, pady=10)

        # Función para agregar menú
        def agregar_menu():
            nombre = nombre_entry.get()
            descripcion = descripcion_entry.get()
            precio = precio_entry.get()

            if not nombre or not descripcion or not precio:
                messagebox.showerror("Error", "Todos los campos son obligatorios.")
                return

            try:
                nuevo_menu = MenuCrud.crear_menu(session, nombre, descripcion, float(precio))
                messagebox.showinfo("Éxito", "Menú agregado correctamente.")
                cargar_menus()
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo agregar el menú: {e}")

        ctk.CTkButton(tab, text="Agregar Menú", command=agregar_menu).grid(row=3, column=0, columnspan=4, pady=10)

        # Tabla de menús
        treeview = ttk.Treeview(tab, columns=("ID", "Nombre", "Descripción", "Precio"), show="headings", height=15)
        treeview.grid(row=4, column=0, columnspan=5, padx=10, pady=10)
        treeview.heading("ID", text="ID")
        treeview.heading("Nombre", text="Nombre")
        treeview.heading("Descripción", text="Descripción")
        treeview.heading("Precio", text="Precio")

        def cargar_menus():
            for row in treeview.get_children():
                treeview.delete(row)
            menus = MenuCrud.obtener_menus(session)
            for menu in menus:
                treeview.insert("", "end", values=(menu.id, menu.nombre, menu.descripcion, menu.precio))

        cargar_menus()

        # Botón de eliminar menú
        def eliminar_menu():
            selected_item = treeview.selection()
            if selected_item:
                menu_id = treeview.item(selected_item)["values"][0]
                try:
                    MenuCrud.eliminar_menu(session, menu_id)
                    messagebox.showinfo("Éxito", "Menú eliminado correctamente.")
                    cargar_menus()
                except Exception as e:
                    messagebox.showerror("Error", f"No se pudo eliminar el menú: {e}")
            else:
                messagebox.showwarning("Advertencia", "Debe seleccionar un menú para eliminar.")

        ctk.CTkButton(tab, text="Eliminar Menú", command=eliminar_menu).grid(row=5, column=0, padx=10, pady=10)

    def create_pedidos_tab(self):
        tab = self.tab_view.add("Pedidos")

        # Campos de entrada
        ctk.CTkLabel(tab, text="Cliente:").grid(row=0, column=0, padx=10, pady=10)
        cliente_combobox = ctk.CTkComboBox(tab, values=[cliente.nombre for cliente in ClienteCrud.obtener_clientes(session)])
        cliente_combobox.grid(row=0, column=1, padx=10, pady=10)

        ctk.CTkLabel(tab, text="Fecha:").grid(row=0, column=2, padx=10, pady=10)
        fecha_entry = ctk.CTkEntry(tab, state="readonly")
        fecha_entry.grid(row=0, column=3, padx=10, pady=10)

        fecha_entry.insert(0, datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

        ctk.CTkLabel(tab, text="Menú:").grid(row=1, column=0, padx=10, pady=10)
        menu_combobox = ctk.CTkComboBox(tab, values=[menu.nombre for menu in MenuCrud.obtener_menus(session)])
        menu_combobox.grid(row=1, column=1, padx=10, pady=10)

        # Función para agregar pedido
        def agregar_pedido():
            cliente_nombre = cliente_combobox.get()
            fecha = fecha_entry.get()
            menu_nombre = menu_combobox.get()

            if not cliente_nombre or not menu_nombre:
                messagebox.showerror("Error", "Todos los campos son obligatorios.")
                return

            cliente = ClienteCrud.obtener_cliente_por_nombre(session, cliente_nombre)
            menu = MenuCrud.obtener_menu_por_nombre(session, menu_nombre)

            if cliente and menu:
                try:
                    PedidoCrud.crear_pedido(session, cliente.id, menu.id, fecha)
                    messagebox.showinfo("Éxito", "Pedido realizado correctamente.")
                except Exception as e:
                    messagebox.showerror("Error", f"No se pudo realizar el pedido: {e}")
            else:
                messagebox.showerror("Error", "No se encontró el cliente o el menú.")

        ctk.CTkButton(tab, text="Realizar Pedido", command=agregar_pedido).grid(row=2, column=0, columnspan=4, pady=10)

        # Tabla de pedidos
        treeview = ttk.Treeview(tab, columns=("ID", "Cliente", "Menú", "Fecha"), show="headings", height=15)
        treeview.grid(row=3, column=0, columnspan=4, padx=10, pady=10)
        treeview.heading("ID", text="ID")
        treeview.heading("Cliente", text="Cliente")
        treeview.heading("Menú", text="Menú")
        treeview.heading("Fecha", text="Fecha")

        def cargar_pedidos():
            for row in treeview.get_children():
                treeview.delete(row)
            pedidos = PedidoCrud.obtener_pedidos(session)
            for pedido in pedidos:
                cliente = ClienteCrud.obtener_cliente_por_id(session, pedido.id_cliente)
                menu = MenuCrud.obtener_menu_por_id(session, pedido.id_menu)
                treeview.insert("", "end", values=(pedido.id, cliente.nombre, menu.nombre, pedido.fecha))

        cargar_pedidos()

        # Botón de eliminar pedido
        def eliminar_pedido():
            selected_item = treeview.selection()
            if selected_item:
                pedido_id = treeview.item(selected_item)["values"][0]
                try:
                    PedidoCrud.eliminar_pedido(session, pedido_id)
                    messagebox.showinfo("Éxito", "Pedido eliminado correctamente.")
                    cargar_pedidos()
                except Exception as e:
                    messagebox.showerror("Error", f"No se pudo eliminar el pedido: {e}")
            else:
                messagebox.showwarning("Advertencia", "Debe seleccionar un pedido para eliminar.")

        ctk.CTkButton(tab, text="Eliminar Pedido", command=eliminar_pedido).grid(row=4, column=0, padx=10, pady=10)


if __name__ == "__main__":
    app = GestionRestauranteApp()
    app.mainloop()
