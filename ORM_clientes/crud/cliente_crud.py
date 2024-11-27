from sqlalchemy.orm import Session
from models import Cliente 

class ClienteCrud:
    @staticmethod
    def crear_cliente(db: Session, nombre: str, correo: str):
        cliente_existente = db.query(Cliente).filter_by(correo=correo).first()
        if cliente_existente:
            raise ValueError(f"El cliente con el correo {correo} ya existe")
        cliente = Cliente(nombre=nombre, correo=correo)
        db.add(cliente)
        db.commit()
        db.refresh(cliente)
        return cliente

    @staticmethod
    def obtener_clientes(db: Session):
        return db.query(Cliente).all()

    @staticmethod
    def obtener_cliente_por_nombre(db: Session, nombre_cliente: str):
        return db.query(Cliente).filter(Cliente.nombre == nombre_cliente).first()

    @staticmethod
    def actualizar_cliente(db: Session, correo_actual: str, nuevo_nombre: str, nuevo_correo: str = None):
        cliente = db.query(Cliente).filter_by(correo=correo_actual).first()
        if not cliente:
            raise ValueError(f"No se encontró el cliente con el correo '{correo_actual}'.")
        
        # Actualiza solo si es necesario
        if nuevo_correo and nuevo_correo != cliente.correo:
            cliente.correo = nuevo_correo
        cliente.nombre = nuevo_nombre
        db.commit()
        db.refresh(cliente)
        return cliente

    @staticmethod
    def eliminar_cliente(db: Session, correo: str):
        cliente = db.query(Cliente).filter_by(correo=correo).first()
        if not cliente:
            raise ValueError(f"No se encontró el cliente con el correo '{correo}'.")
        db.delete(cliente)
        db.commit()
        return cliente
