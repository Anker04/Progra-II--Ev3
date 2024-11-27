from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from database import Base
from datetime import datetime

class Cliente(Base):
    __tablename__ = "clientes"
    id = Column(Integer, primary_key=True)
    correo = Column(String, unique=True, nullable=False)
    nombre = Column(String, nullable=False)
    pedidos = relationship("Pedido", back_populates="cliente")

class Ingrediente(Base):
    __tablename__ = "ingredientes"
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, unique=True, nullable=False)
    tipo = Column(String, nullable=False)
    cantidad = Column(Float, nullable=False)
    unidad_medida = Column(String, nullable=False)

class Menu(Base):
    __tablename__ = "menus"
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, nullable=False)
    descripcion = Column(String)
    precio = Column(Float, nullable=False)

class Pedido(Base):
    __tablename__ = "pedidos"
    id = Column(Integer, primary_key=True, index=True)
    cliente_id = Column(Integer, ForeignKey("clientes.id"))
    fecha_creacion = Column(DateTime, default=datetime.utcnow)
    total = Column(Float, nullable=False)
    cliente = relationship("Cliente", back_populates="pedidos")