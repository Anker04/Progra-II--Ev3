import matplotlib.pyplot as plt

def grafico_ventas_por_fecha(fechas, totales):
    plt.figure(figsize=(10, 6))
    plt.bar(fechas, totales, color='skyblue')
    plt.xlabel('Fechas')
    plt.ylabel('Total Ventas')
    plt.title('Ventas por Fecha')
    plt.show()

def grafico_menus_populares(menus, cantidades):
    plt.figure(figsize=(10, 6))
    plt.pie(cantidades, labels=menus, autopct='%1.1f%%')
    plt.title('Menús más Populares')
    plt.show()
