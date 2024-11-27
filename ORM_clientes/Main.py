from database import engine
from models import Base

if __name__ == "__main__":
    print("Creando tablas en la base de datos...")
    Base.metadata.create_all(bind=engine)
    print("Tablas creadas exitosamente.")
