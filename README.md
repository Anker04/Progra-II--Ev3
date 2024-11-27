# Proyecto ORM de Clientes

Este es un proyecto que utiliza SQLAlchemy para gestionar clientes a través de un CRUD (Crear, Leer, Actualizar, Eliminar). La aplicación está construida utilizando Python y la biblioteca `tkinter` para crear una interfaz gráfica que permita a los usuarios interactuar con la base de datos de clientes. 

## Características

- **Crear cliente**: Permite agregar nuevos clientes a la base de datos.
- **Leer clientes**: Muestra todos los clientes existentes en la base de datos.
- **Actualizar cliente**: Permite modificar los datos de un cliente existente.
- **Eliminar cliente**: Elimina un cliente de la base de datos.
- **Interfaz gráfica**: La aplicación utiliza `customtkinter` para ofrecer una interfaz de usuario moderna.

## Requisitos

Para ejecutar este proyecto, necesitarás tener Python 3.12 (o una versión superior) y las siguientes bibliotecas instaladas:

- `SQLAlchemy`
- `tkinter`
- `customtkinter`

Puedes instalar las dependencias necesarias utilizando `pip`. Asegúrate de tener un entorno virtual configurado para evitar conflictos con otras dependencias globales.

pip install sqlalchemy customtkinter

#Estructura del Proyecto
Proyecto/
│
├── crud/                  # Carpeta que contiene los archivos de lógica del CRUD
│   ├── cliente_crud.py    # Lógica para crear, leer, actualizar y eliminar clientes
│
├── models/                # Carpeta que contiene los modelos de la base de datos
│   ├── cliente.py         # Modelo de Cliente con SQLAlchemy
│
├── app.py                 # Archivo principal de la aplicación
├── database.py            # Configuración de la base de datos
└── README.md              # Este archivo

## Instalación y Configuración
Clona el repositorio:

git clone https://github.com/tu-usuario/tu-repositorio.git
cd tu-repositorio
Crea un entorno virtual:

python -m venv venv
Activa el entorno virtual:

En Windows:
Copiar código
.\venv\Scripts\activate

En macOS/Linux:
Copiar código
source venv/bin/activate
Instala las dependencias:

pip install -r requirements.txt
Configura la base de datos:

La base de datos se maneja a través de SQLAlchemy y se crea automáticamente cuando se ejecuta la aplicación.

## Uso
Ejecuta la aplicación con el siguiente comando:

python app.py
La interfaz gráfica te permitirá interactuar con la base de datos:

Crear cliente: Ingresa el nombre y correo de un nuevo cliente.
Ver clientes: Visualiza la lista de clientes existentes.
Actualizar cliente: Modifica los datos de un cliente existente.
Eliminar cliente: Elimina un cliente de la base de datos.

## Funcionalidad del CRUD
Crear Cliente
- **Puedes agregar un nuevo cliente proporcionando el nombre y el correo electrónico. La aplicación verificará si el correo ya existe en la base de datos antes de crear el cliente.

  Leer Clientes
- **Visualiza una lista de todos los clientes almacenados en la base de datos. Los clientes se muestran con su nombre y correo electrónico.

Actualizar Cliente
- **Puedes actualizar el nombre y/o correo electrónico de un cliente existente. Si el correo se modifica, la aplicación actualizará ese campo en la base de datos.

Eliminar Cliente
- **Permite eliminar un cliente específico basado en su correo electrónico. Si el cliente no existe, se mostrará un mensaje de error.

## Tecnologías Utilizadas
- **Python: Lenguaje principal del proyecto.
- **SQLAlchemy: ORM utilizado para interactuar con la base de datos.
- **Tkinter: Biblioteca para crear la interfaz gráfica.
- **CustomTkinter: Una extensión de Tkinter para interfaces gráficas modernas.
- **Contribuciones
  ¡Las contribuciones son bienvenidas! Si deseas contribuir, sigue estos pasos:

Haz un fork de este repositorio.
Crea una nueva rama (git checkout -b feature-nueva-funcionalidad).
Realiza tus cambios y haz un commit (git commit -am 'Agrega nueva funcionalidad').
Sube tus cambios (git push origin feature-nueva-funcionalidad).
Abre un Pull Request.
