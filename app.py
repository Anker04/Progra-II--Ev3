import customtkinter as ctk

class RestaurantApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Sistema de Gestión de Restaurante")
        self.geometry("800x600")
        self.configurar_interfaz()

    def configurar_interfaz(self):
        # Ejemplo de pestañas
        self.tab_control = ctk.CTkTabview(self, width=800, height=600)
        self.tab_control.pack(expand=True, fill="both")
        
        self.tab_ingredientes = self.tab_control.add("Ingredientes")
        self.tab_clientes = self.tab_control.add("Clientes")
        self.tab_pedidos = self.tab_control.add("Pedidos")
        
        # Más contenido en cada pestaña
        ctk.CTkLabel(self.tab_ingredientes, text="Gestión de Ingredientes").pack(pady=20)

if __name__ == "__main__":
    app = RestaurantApp()
    app.mainloop()
