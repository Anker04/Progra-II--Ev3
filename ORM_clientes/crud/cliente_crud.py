from models import Cliente
from sqlalchemy.orm import Session

class Cliente_crud:
    @staticmethod
    def crear_cliente(db: Session, nombre: str, correo: str):
        cliente_existente = db.query(Cliente).filter_by(correo = correo).first()
        if cliente_existente:
            print(f"El cliente con el correo {correo} ya existe")
            return cliente_existente

        cliente = Cliente(nombre=nombre, correo=correo)
        db.add(cliente)
        db.commit()
        db.refresh(cliente)
        return cliente

    @staticmethod
    def obtener_clientes(db: Session):
        return db.query(Cliente).all()

    @staticmethod
    def actualizar_cliente(db: Session, correo_actual: str, nuevo_nombre: str, nuevo_correo: str = None):
        cliente = db.query(Cliente).get(correo_actual)
        if not cliente:
            print(f"No se encontró el cliente con el email '{correo_actual}'.")
            return None
        if nuevo_correo and nuevo_correo != correo_actual:
            nuevo_cliente = Cliente(nombre=nuevo_nombre, email=nuevo_correo)
            db.add(nuevo_cliente)
            db.commit()
            db.delete(cliente)
            db.commit()
            return nuevo_cliente
        else:
            cliente.nombre = nuevo_nombre
            db.commit()
            db.refresh(cliente)
            return cliente

    @staticmethod
    def eliminar_cliente(db: Session, correo: str):
        cliente = db.query(Cliente).get(correo)
        if cliente:
            db.delete(cliente)
            db.commit()
            return cliente
        return None
