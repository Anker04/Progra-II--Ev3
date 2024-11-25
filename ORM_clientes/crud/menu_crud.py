from models import Menu
from sqlalchemy.orm import Session

def crear_menu(db: Session, nombre: str, descripcion: str, precio: float):
    nuevo_menu = Menu(nombre=nombre, descripcion=descripcion, precio=precio)
    db.add(nuevo_menu)
    db.commit()
    db.refresh(nuevo_menu)
    return nuevo_menu

def obtener_menus(db: Session):
    return db.query(Menu).all()

def actualizar_menu(db: Session, menu_id: int, nombre: str, descripcion: str, precio: float):
    menu = db.query(Menu).filter(Menu.id == menu_id).first()
    if menu:
        menu.nombre = nombre
        menu.descripcion = descripcion
        menu.precio = precio
        db.commit()
        return menu
    return None

def eliminar_menu(db: Session, menu_id: int):
    menu = db.query(Menu).filter(Menu.id == menu_id).first()
    if menu:
        db.delete(menu)
        db.commit()
        return menu
    return None
