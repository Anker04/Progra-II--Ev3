from models import Ingrediente
from sqlalchemy.orm import Session

def crear_ingrediente(db: Session, nombre: str, tipo: str, cantidad: float, unidad_medida: str):
    nuevo_ingrediente = Ingrediente(nombre=nombre, tipo=tipo, cantidad=cantidad, unidad_medida=unidad_medida)
    db.add(nuevo_ingrediente)
    db.commit()
    db.refresh(nuevo_ingrediente)
    return nuevo_ingrediente

def obtener_ingredientes(db: Session):
    return db.query(Ingrediente).all()

def actualizar_ingrediente(db: Session, ingrediente_id: int, cantidad: float):
    ingrediente = db.query(Ingrediente).filter(Ingrediente.id == ingrediente_id).first()
    if ingrediente:
        ingrediente.cantidad = cantidad
        db.commit()
        return ingrediente
    return None

def eliminar_ingrediente(db: Session, ingrediente_id: int):
    ingrediente = db.query(Ingrediente).filter(Ingrediente.id == ingrediente_id).first()
    if ingrediente:
        db.delete(ingrediente)
        db.commit()
        return ingrediente
    return None