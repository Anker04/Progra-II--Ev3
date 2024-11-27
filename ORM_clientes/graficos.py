
import matplotlib.pyplot as plt

def generar_grafico_ventas_diarias(ventas_diarias):
    """
    Genera un gráfico de ventas diarias.
    :param ventas_diarias: Diccionario con fechas y cantidad de ventas.
    """
    fechas = list(ventas_diarias.keys())
    ventas = list(ventas_diarias.values())
    
    plt.figure(figsize=(10, 6))
    plt.bar(fechas, ventas, color='skyblue')
    plt.xlabel('Fecha')
    plt.ylabel('Ventas')
    plt.title('Ventas Diarias')
    plt.xticks(rotation=45)
    plt.tight_layout()
    
    # Guardamos el gráfico para mostrarlo en la interfaz
    plt.savefig('ventas_diarias.png')
    plt.close()

def generar_grafico_menu_mas_vendido(ventas_por_menu):
    """
    Genera un gráfico de barras para los menús más vendidos.
    :param ventas_por_menu: Diccionario con nombres de menús y cantidad de ventas.
    """
    menus = list(ventas_por_menu.keys())
    ventas = list(ventas_por_menu.values())
    
    plt.figure(figsize=(10, 6))
    plt.bar(menus, ventas, color='lightcoral')
    plt.xlabel('Menú')
    plt.ylabel('Ventas')
    plt.title('Menú Más Vendido')
    plt.xticks(rotation=45)
    plt.tight_layout()
    
    # Guardamos el gráfico para mostrarlo en la interfaz
    plt.savefig('menu_mas_vendido.png')
    plt.close()

def generar_grafico_ingredientes_mas_utilizados(ingredientes_utilizados):
    """
    Genera un gráfico de barras para los ingredientes más utilizados.
    :param ingredientes_utilizados: Diccionario con ingredientes y cantidad de uso.
    """
    ingredientes = list(ingredientes_utilizados.keys())
    cantidades = list(ingredientes_utilizados.values())
    
    plt.figure(figsize=(10, 6))
    plt.bar(ingredientes, cantidades, color='lightgreen')
    plt.xlabel('Ingrediente')
    plt.ylabel('Cantidad Utilizada')
    plt.title('Ingredientes Más Utilizados')
    plt.xticks(rotation=45)
    plt.tight_layout()
    
    # Guardamos el gráfico para mostrarlo en la interfaz
    plt.savefig('ingredientes_mas_utilizados.png')
    plt.close()

def obtener_graficos():
    """
    Devuelve los gráficos generados como un arreglo.
    """
    # Suponiendo que ya se tiene un diccionario de ventas, menús y ingredientes.
    ventas_diarias = {'2024-11-01': 50, '2024-11-02': 60, '2024-11-03': 55}  # Datos de ejemplo
    ventas_por_menu = {'Completo Italiano': 100, 'Completo Normal': 150}  # Datos de ejemplo
    ingredientes_utilizados = {'Tomate': 80, 'Pan de Completo': 120, 'Palta': 60}  # Datos de ejemplo
    
    # Llamamos a las funciones para generar los gráficos
    generar_grafico_ventas_diarias(ventas_diarias)
    generar_grafico_menu_mas_vendido(ventas_por_menu)
    generar_grafico_ingredientes_mas_utilizados(ingredientes_utilizados)
    
    # Devolvemos los nombres de los archivos de los gráficos generados
    return ['ventas_diarias.png', 'menu_mas_vendido.png', 'ingredientes_mas_utilizados.png']
