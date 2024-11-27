from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from database import Base
from datetime import datetime

class Cliente(Base):
    __tablename__ = "clientes"
    
    id = Column(Integer, primary_key=True)
    correo = Column(String, unique=True, nullable=False, index=True)  # Añadir índice para búsquedas rápidas
    nombre = Column(String, nullable=False)
    
    pedidos = relationship("Pedido", back_populates="cliente", cascade="all, delete-orphan")  # Manejo de eliminación en cascada

    def __repr__(self):
        return f"<Cliente(id={self.id}, nombre={self.nombre}, correo={self.correo})>"

class Ingrediente(Base):
    __tablename__ = "ingredientes"
    
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, unique=True, nullable=False)
    tipo = Column(String, nullable=False)
    cantidad = Column(Float, nullable=False)
    unidad_medida = Column(String, nullable=False)

    def __repr__(self):
        return f"<Ingrediente(id={self.id}, nombre={self.nombre}, cantidad={self.cantidad})>"

class Menu(Base):
    __tablename__ = "menus"
    
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, nullable=False)
    descripcion = Column(String)
    precio = Column(Float, nullable=False)

    def __repr__(self):
        return f"<Menu(id={self.id}, nombre={self.nombre}, precio={self.precio})>"

class Pedido(Base):
    __tablename__ = "pedidos"
    
    id = Column(Integer, primary_key=True, index=True)
    cliente_id = Column(Integer, ForeignKey("clientes.id"))
    fecha_creacion = Column(DateTime, default=datetime.utcnow)
    total = Column(Float, nullable=False)
    
    cliente = relationship("Cliente", back_populates="pedidos")
    
    def __repr__(self):
        return f"<Pedido(id={self.id}, cliente_id={self.cliente_id}, total={self.total})>"

# Agregar una tabla intermedia si deseas manejar la relación entre Pedido y Menu
class PedidoMenu(Base):
    __tablename__ = "pedido_menu"
    
    pedido_id = Column(Integer, ForeignKey("pedidos.id"), primary_key=True)
    menu_id = Column(Integer, ForeignKey("menus.id"), primary_key=True)
    cantidad = Column(Integer, nullable=False, default=1)  # Cantidad de este menú en el pedido

    pedido = relationship("Pedido", back_populates="menus")
    menu = relationship("Menu", back_populates="pedidos")

# Relacionar las tablas Pedido y Menu a través de la tabla intermedia
Pedido.menus = relationship("PedidoMenu", back_populates="pedido")
Menu.pedidos = relationship("PedidoMenu", back_populates="menu")
