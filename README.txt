El archivo "iniciar.bat" configura lo necesario e inicia el programa (en Windows)

Para configurarlo de forma manual es necesario lo siguiente:

Crear el entorno virtual si no existe:
python -m venv env

Levantar el entorno virtual:
env\Scripts\activate

Instalar las librerías que se encuentran en el archivo "requirements.txt":
pip install -r requirements.txt

Iniciar la app:
python app.py