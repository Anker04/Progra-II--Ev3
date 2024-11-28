from models import Pedido, Cliente
from sqlalchemy.orm import Session
from datetime import datetime

class PedidoCrud:
    @staticmethod
    def crear_pedido(db: Session, cliente_id: int, menu_id: int, total: float):
        nuevo_pedido = Pedido(cliente_id=cliente_id, menu_id=menu_id, total=total, fecha=datetime.now())
        db.add(nuevo_pedido)
        db.commit()
        db.refresh(nuevo_pedido)
        return nuevo_pedido

    @staticmethod
    def obtener_pedidos(db: Session):
        return db.query(Pedido).all()

    @staticmethod
    def obtener_pedidos_por_cliente(db: Session, cliente_id: int):
        pedidos = db.query(Pedido).filter(Pedido.cliente_id == cliente_id).all()
        if not pedidos:
            print(f"No se encontraron pedidos para el cliente con ID {cliente_id}.")
        return pedidos

    @staticmethod
    def eliminar_pedido(db: Session, pedido_id: int):
        pedido = db.query(Pedido).filter(Pedido.id == pedido_id).first()
        if not pedido:
            raise ValueError(f"No se encontró un pedido con el ID {pedido_id}.")
        
        db.delete(pedido)
        db.commit()
        return pedido
