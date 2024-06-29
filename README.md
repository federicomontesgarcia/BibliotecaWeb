Biblioteca Web

Pasos para la instalación:
1. Clonar el repositorio.
   git clone https://github.com/tu-usuario/nombre-del-proyecto.git
2. Crear y activar un entorno virtual de python (ejemplo para ubuntu).
   python -m venv env
   source env/bin/activate 
3. Instalar las dependencias del proyecto a partir del archivo requirements.txt.
   pip install -r requirements.txt
4. Aplicar las migraciones.
   python manage.py migrate
5. Crear un super usuario para ingresar con rol administrador.
   python manage.py createsuperuser
6. Iniciar el servidor de desarrollo.
   python manage.py runserver

 
   
