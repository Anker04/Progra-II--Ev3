from models import Ingrediente
from sqlalchemy.orm import Session

class IngredienteCrud:
    @staticmethod
    def crear_ingrediente(db: Session, nombre: str, tipo: str, cantidad: float, unidad_medida: str):
        # Validaciones
        if cantidad <= 0:
            raise ValueError("La cantidad debe ser un número positivo.")
        if not unidad_medida:
            raise ValueError("La unidad de medida no puede estar vacía.")
        
        nuevo_ingrediente = Ingrediente(
            nombre=nombre,
            tipo=tipo,
            cantidad=cantidad,
            unidad_medida=unidad_medida
        )
        db.add(nuevo_ingrediente)
        db.commit()
        db.refresh(nuevo_ingrediente)
        return nuevo_ingrediente

    @staticmethod
    def obtener_ingredientes(db: Session):
        return db.query(Ingrediente).all()

    @staticmethod
    def actualizar_ingrediente(db: Session, ingrediente_id: int, cantidad: float):
        if cantidad < 0:
            raise ValueError("La cantidad no puede ser negativa.")
        
        ingrediente = db.query(Ingrediente).filter(Ingrediente.id == ingrediente_id).first()
        if not ingrediente:
            raise ValueError(f"No se encontró el ingrediente con ID {ingrediente_id}.")
        
        ingrediente.cantidad = cantidad
        db.commit()
        db.refresh(ingrediente)
        return ingrediente

    @staticmethod
    def modificar_cantidad(db: Session, ingrediente_id: int, cantidad_cambio: float):
        """
        Modifica la cantidad de un ingrediente de forma acumulativa.
        `cantidad_cambio` puede ser positiva (agregar) o negativa (restar).
        """
        ingrediente = db.query(Ingrediente).filter(Ingrediente.id == ingrediente_id).first()
        if not ingrediente:
            raise ValueError(f"No se encontró el ingrediente con ID {ingrediente_id}.")
        
        nueva_cantidad = ingrediente.cantidad + cantidad_cambio
        if nueva_cantidad < 0:
            raise ValueError(f"La cantidad resultante para el ingrediente ID {ingrediente_id} no puede ser negativa.")
        
        ingrediente.cantidad = nueva_cantidad
        db.commit()
        db.refresh(ingrediente)
        return ingrediente

    @staticmethod
    def eliminar_ingrediente(db: Session, ingrediente_id: int):
        ingrediente = db.query(Ingrediente).filter(Ingrediente.id == ingrediente_id).first()
        if not ingrediente:
            raise ValueError(f"No se encontró el ingrediente con ID {ingrediente_id}.")
        
        db.delete(ingrediente)
        db.commit()
        return ingrediente
