from models import Cliente
from sqlalchemy.orm import Session

def crear_cliente(db: Session, nombre: str, correo: str):
    nuevo_cliente = Cliente(nombre=nombre, correo=correo)
    db.add(nuevo_cliente)
    db.commit()
    db.refresh(nuevo_cliente)
    return nuevo_cliente

def obtener_clientes(db: Session):
    return db.query(Cliente).all()

def actualizar_cliente(db: Session, cliente_id: int, nombre: str, correo: str):
    cliente = db.query(Cliente).filter(Cliente.id == cliente_id).first()
    if cliente:
        cliente.nombre = nombre
        cliente.correo = correo
        db.commit()
        return cliente
    return None

def eliminar_cliente(db: Session, cliente_id: int):
    cliente = db.query(Cliente).filter(Cliente.id == cliente_id).first()
    if cliente:
        db.delete(cliente)
        db.commit()
        return cliente
    return None
