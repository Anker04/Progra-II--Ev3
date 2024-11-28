from sqlalchemy.orm import Session
from sqlalchemy.orm.exc import NoResultFound
from models import Cliente

class ClienteCrud:
    @staticmethod
    def crear_cliente(db: Session, nombre: str, correo: str):
        # Verificar si ya existe un cliente con el mismo correo
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
    def obtener_cliente_por_id(db: Session, cliente_id: int):
        try:
            return db.query(Cliente).filter(Cliente.id == cliente_id).one()
        except NoResultFound:
            return None

    @staticmethod
    def actualizar_cliente(db: Session, cliente_id: int, nuevo_nombre: str, nuevo_correo: str = None):
        cliente = db.query(Cliente).filter_by(id=cliente_id).first()
        if not cliente:
            raise ValueError(f"No se encontró el cliente con el ID '{cliente_id}'.")

        # Verifica si el nuevo correo ya está en uso
        if nuevo_correo and nuevo_correo != cliente.correo:
            cliente_existente = db.query(Cliente).filter_by(correo=nuevo_correo).first()
            if cliente_existente:
                raise ValueError(f"El correo {nuevo_correo} ya está en uso por otro cliente.")
            cliente.correo = nuevo_correo

        cliente.nombre = nuevo_nombre
        db.commit()
        db.refresh(cliente)
        return cliente

    @staticmethod
    def eliminar_cliente(db: Session, cliente_id: int):
        cliente = db.query(Cliente).filter_by(id=cliente_id).first()
        if not cliente:
            raise ValueError(f"No se encontró el cliente con el ID '{cliente_id}'.")
        db.delete(cliente)
        db.commit()
        return cliente
