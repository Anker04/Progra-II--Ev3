from models import Menu
from sqlalchemy.orm import Session

class MenuCrud:
    @staticmethod
    def crear_menu(db: Session, nombre: str, descripcion: str, precio: float):
        # Validaciones
        if precio <= 0:
            raise ValueError("El precio debe ser un valor positivo.")
        if not nombre.strip():
            raise ValueError("El nombre del menú no puede estar vacío.")
        if not descripcion.strip():
            raise ValueError("La descripción no puede estar vacía.")
        
        nuevo_menu = Menu(nombre=nombre, descripcion=descripcion, precio=precio)
        db.add(nuevo_menu)
        db.commit()
        db.refresh(nuevo_menu)
        return nuevo_menu

    @staticmethod
    def obtener_menus(db: Session):
        return db.query(Menu).all()

    @staticmethod
    def actualizar_menu(db: Session, menu_id: int, nombre: str, descripcion: str, precio: float):
        # Validaciones
        if precio <= 0:
            raise ValueError("El precio debe ser un valor positivo.")
        if not nombre.strip():
            raise ValueError("El nombre del menú no puede estar vacío.")
        if not descripcion.strip():
            raise ValueError("La descripción no puede estar vacía.")
        
        menu = db.query(Menu).filter(Menu.id == menu_id).first()
        if not menu:
            raise ValueError(f"No se encontró el menú con ID {menu_id}.")
        
        menu.nombre = nombre
        menu.descripcion = descripcion
        menu.precio = precio
        db.commit()
        db.refresh(menu)
        return menu

    @staticmethod
    def eliminar_menu(db: Session, menu_id: int):
        menu = db.query(Menu).filter(Menu.id == menu_id).first()
        if not menu:
            raise ValueError(f"No se encontró el menú con ID {menu_id}.")
        
        db.delete(menu)
        db.commit()
        return menu
