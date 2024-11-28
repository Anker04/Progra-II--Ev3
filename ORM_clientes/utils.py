from fpdf import FPDF

def generar_boleta(cliente, pedidos, total):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt=f"Boleta para {cliente.nombre}", ln=True, align='C')
    pdf.cell(200, 10, txt=f"Correo: {cliente.correo}", ln=True, align='L')
    pdf.cell(200, 10, txt="Detalle de Compra:", ln=True, align='L')

    for pedido in pedidos:
        pdf.cell(200, 10, txt=f"{pedido['menu']} - {pedido['cantidad']} x ${pedido['precio']}", ln=True, align='L')

    pdf.cell(200, 10, txt=f"Total: ${total}", ln=True, align='R')
    pdf.output(f"boleta_{cliente.nombre}.pdf")
    print(f"Boleta generada: boleta_{cliente.nombre}.pdf")
