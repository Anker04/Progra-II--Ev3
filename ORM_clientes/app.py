import customtkinter as ctk
from tkinter import ttk, messagebox
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from crud.cliente_crud import ClienteCrud
from crud.ingrediente_crud import IngredienteCrud
from crud.menu_crud import MenuCrud
from crud.pedido_crud import PedidoCrud
from datetime import datetime
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from utils import generar_boleta  
from fpdf import FPDF

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
        self.geometry("1100x600")
        self.resizable(False, False)

        # Tabview principal
        self.tab_view = ctk.CTkTabview(self, width=780, height=550)
        self.tab_view.pack(pady=20, padx=10)

        # Crear pestañas
        self.create_clientes_tab()
        self.create_ingredientes_tab()
        self.create_menu_tab()
        self.create_pedidos_tab()
        self.create_graficos_tab()

    def create_clientes_tab(self):
        tab = self.tab_view.add("Clientes")

        ctk.CTkLabel(tab, text="Correo:").grid(row=0, column=0, padx=10, pady=10)
        correo_entry = ctk.CTkEntry(tab)
        correo_entry.grid(row=0, column=1, padx=10, pady=10)

        ctk.CTkLabel(tab, text="Nombre:").grid(row=0, column=2, padx=10, pady=10)
        nombre_entry = ctk.CTkEntry(tab)
        nombre_entry.grid(row=0, column=3, padx=10, pady=10)

        self.editing_client_id = None

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
                # Limpiar campos después de agregar
                correo_entry.delete(0, ctk.END)
                nombre_entry.delete(0, ctk.END)
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo agregar el cliente: {e}")

        # Botón para agregar cliente
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

        # Función para editar cliente
        def editar_cliente():
            selected_item = treeview.selection()
            if selected_item:
                cliente_id = treeview.item(selected_item)["values"][0]  # Obtén el ID del cliente seleccionado
                cliente = ClienteCrud.obtener_cliente_por_id(session, cliente_id)  # Obtén el cliente por ID
                if cliente:
                    correo_entry.delete(0, ctk.END)
                    correo_entry.insert(0, cliente.correo)  # Coloca el correo en el campo de entrada
                    nombre_entry.delete(0, ctk.END)
                    nombre_entry.insert(0, cliente.nombre)  # Coloca el nombre en el campo de entrada

                    # Cambiar el estado a edición
                    self.editing_client_id = cliente.id  # Guardar el ID del cliente en edición
                    actualizar_button.config(state="normal")  # Habilitar el botón de actualizar
                else:
                    messagebox.showerror("Error", "No se pudo encontrar el cliente.")
            else:
                messagebox.showwarning("Advertencia", "Debe seleccionar un cliente para editar.")

        # Botón para editar cliente
        ctk.CTkButton(tab, text="Editar Cliente", command=editar_cliente).grid(row=2, column=0, padx=10, pady=10)

        # Función para actualizar cliente
        def actualizar_cliente():
            correo = correo_entry.get()
            nombre = nombre_entry.get()

            if not correo or not nombre:
                messagebox.showerror("Error", "Todos los campos son obligatorios.")
                return

            try:
                ClienteCrud.actualizar_cliente(session, self.editing_client_id, nombre, correo)
                messagebox.showinfo("Éxito", "Cliente actualizado correctamente.")
                cargar_clientes()
                # Limpiar campos después de actualizar
                correo_entry.delete(0, ctk.END)
                nombre_entry.delete(0, ctk.END)
                self.editing_client_id = None  # Reiniciar el ID de edición
                actualizar_button.config(state="disabled")  # Deshabilitar el botón de actualizar
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo actualizar el cliente: {e}")

        # Botón para actualizar cliente
        actualizar_button = ctk.CTkButton(tab, text="Actualizar Cliente", command=actualizar_cliente, state="disabled")
        actualizar_button.grid(row=0, column=5, padx=10, pady=10)

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

        ctk.CTkButton(tab, text="Eliminar Cliente", command=eliminar_cliente).grid(row=2, column=1, padx=10, pady=10)

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

        # Función para eliminar ingrediente
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
        precio_entry= ctk.CTkEntry(tab)
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
            menu_nombre = menu_combobox.get()

            if not cliente_nombre or not menu_nombre:
                messagebox.showerror("Error", "Todos los campos son obligatorios.")
                return

            cliente = ClienteCrud.obtener_cliente_por_nombre(session, cliente_nombre)
            menu = MenuCrud.obtener_menu_por_nombre(session, menu_nombre)

            if cliente and menu:
                try:
                    # Calcular el total (esto es solo un ejemplo, adapta según tus necesidades)
                    total = menu.precio  # Asumiendo que el precio se encuentra en el objeto 'menu'

                    # Crear el pedido en la base de datos
                    pedido = PedidoCrud.crear_pedido(session, cliente.id, total)  # Asegúrate de pasar el total aquí

                    # Actualizar la tabla de pedidos
                    cargar_pedidos()  # Asegúrate de que esta función esté definida para cargar los pedidos en la tabla

                    messagebox.showinfo("Éxito", "Pedido realizado correctamente.")
                except Exception as e:
                    messagebox.showerror("Error", f"No se pudo realizar el pedido: {e}")
            else:
                messagebox.showerror("Error", "Cliente o menú no válido.")
        ctk.CTkButton(tab, text="Realizar Pedido", command=agregar_pedido).grid(row=2, column=0, columnspan=4, pady=10)

        # Tabla de pedidos
        treeview = ttk.Treeview(tab, columns=("ID", "Cliente", "Menú", "Fecha"), show="headings", height=15)
        treeview.grid(row=3, column=0, columnspan=4, padx=10, pady=10)
        treeview.heading("ID", text="ID")
        treeview.heading("Cliente", text="Cliente")
        treeview.heading("Menú", text="Menú")
        treeview.heading("Fecha", text="Fecha")

        def generar_boleta():
            cliente_nombre = cliente_combobox.get()
            menu_nombre = menu_combobox.get()

            if not cliente_nombre or not menu_nombre:
                messagebox.showerror("Error", "Debe seleccionar un cliente y un menú.")
                return

            cliente = ClienteCrud.obtener_cliente_por_nombre(session, cliente_nombre)
            menu = MenuCrud.obtener_menu_por_nombre(session, menu_nombre)

            if cliente and menu:
                pdf = FPDF()
                pdf.add_page()
                pdf.set_font("Arial", size=12)

                # Agregar contenido a la boleta
                pdf.cell(200, 10, txt="Boleta de Pedido", ln=True, align='C')
                pdf.cell(200, 10, txt=f"Cliente: {cliente.nombre}", ln=True)
                pdf.cell(200, 10, txt=f"Menú: {menu.nombre}", ln=True)
                pdf.cell(200, 10, txt=f"Precio: ${menu.precio:.2f}", ln=True)
                pdf.cell(200, 10, txt=f"Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", ln=True)

                # Guardar la boleta
                pdf_file_path = f"boleta_{cliente.nombre}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
                pdf .output(pdf_file_path)

                messagebox.showinfo("Éxito", f"Boleta generada correctamente: {pdf_file_path}")
            else:
                messagebox.showerror("Error", "Cliente o menú no válido.")

        ctk.CTkButton(tab, text="Generar Boleta", command=generar_boleta).grid(row=2, column=4, padx=10, pady=10)

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

            # Obtener todos los pedidos desde la base de datos
            pedidos = PedidoCrud.obtener_pedidos(session)

            # Iterar sobre cada pedido y cargar sus detalles
            for pedido in pedidos:
                # Obtener el cliente usando su ID
                cliente = ClienteCrud.obtener_cliente_por_id(session, pedido.cliente_id)

                # Obtener el menú usando su ID
                menu = MenuCrud.obtener_menu_por_id(session, pedido.menu_id)  # Cambia esto si es necesario

                # Verificar que se encontró el cliente y el menú antes de insertarlos
                if cliente and menu:
                    treeview.insert("", "end", values=(pedido.id, cliente.nombre, menu.nombre, pedido.fecha))
                else:
                    # Manejo de errores si cliente o menú no se encuentran
                    print(f"Error: Pedido ID {pedido.id} tiene un cliente o menú no válido.")
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

    def create_graficos_tab(self):
        tab = self.tab_view.add("Gráficos")

        # Botón para generar gráfico de ventas
        ctk.CTkButton(tab, text="Generar Gráfico de Ventas", command=self.generar_grafico_ventas).grid(pady=20)

    def generar_grafico_ventas(self):
        # Obtener los datos de ventas
        pedidos = PedidoCrud.obtener_pedidos(session)
        fechas = [pedido.fecha for pedido in pedidos]
        meses = [datetime.strptime(fecha, "%Y-%m-%d %H:%M:%S").strftime("%B") for fecha in fechas]

        # Contar ventas por mes
        venta_por_mes = {}
        for mes in meses:
            if mes not in venta_por_mes:
                venta_por_mes[mes] = 0
            venta_por_mes[mes] += 1

        # Preparar los datos para el gráfico
        meses = list(venta_por_mes.keys())
        ventas = list(venta_por_mes.values())

        # Crear gráfico
        fig, ax = plt.subplots()
        ax.bar(meses, ventas, color='skyblue')
        ax.set_title("Ventas por Mes")
        ax.set_xlabel("Mes")
        ax.set_ylabel("Número de Ventas")
        ax.set_xticklabels(meses, rotation=45)

        # Mostrar el gráfico en la interfaz
        canvas = FigureCanvasTkAgg(fig, master=self.tab_view.tab("Gráficos"))
        canvas.get_tk_widget().grid(sticky="nsew", padx=20, pady=20)
        canvas.draw()

if __name__ == "__main__":
    app = GestionRestauranteApp()
    app.mainloop()