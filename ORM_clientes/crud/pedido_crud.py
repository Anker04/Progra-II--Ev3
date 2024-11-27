from models import Pedido
from sqlalchemy.orm import Session

def crear_pedido(db: Session, cliente_id: int, total: float):
    nuevo_pedido = Pedido(cliente_id=cliente_id, total=total)
    db.add(nuevo_pedido)
    db.commit()
    db.refresh(nuevo_pedido)
    return nuevo_pedido



def obtener_pedidos(db: Session):
    return db.query(Pedido).all()

def eliminar_pedido(db: Session, pedido_id: int):
    pedido = db.query(Pedido).filter(Pedido.id == pedido_id).first()
    if pedido:
        db.delete(pedido)
        db.commit()
        return pedido
    return None
