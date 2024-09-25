# Utiliza la imagen oficial de Python 3.9 con el tag "slim", que es una versión más ligera
FROM python:3.10-slim

# Establece el directorio de trabajo dentro del contenedor en "/app"
WORKDIR /app

# Copia el archivo "requirements.txt" desde el directorio actual en el host
# hacia el directorio "/app" dentro del contenedor
COPY requirements.txt requirements.txt

# Ejecuta el comando "pip install" para instalar las dependencias especificadas
# en el archivo "requirements.txt"
RUN pip install -r requirements.txt

# Copia todos los archivos y directorios del directorio actual en el host
# hacia el directorio "/app" dentro del contenedor
COPY . .

# Expone el puerto 5000 del contenedor para que sea accesible desde el exterior
EXPOSE 5000

# Establece el comando por defecto que se ejecutará cuando se inicie el contenedor
# En este caso, se ejecutará el archivo "app.py" con el intérprete de Python
CMD ["python", "app.py"]