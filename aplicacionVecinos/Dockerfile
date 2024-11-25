# Usar una imagen base de Python
FROM python:3.9-slim

# Instalar dependencias del sistema necesarias para psycopg2 y otras librerías
RUN apt-get update && \
    apt-get install -y build-essential libpq-dev && \
    apt-get clean

# Crear y activar un entorno virtual
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Establecer el directorio de trabajo en /app
WORKDIR /app

# Copiar los archivos del proyecto a la imagen Docker
COPY . .

# Instalar las dependencias de Python
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Ejecutar Gunicorn en el puerto 8000
CMD ["gunicorn", "aplicacionVecinos.wsgi", "--bind", "0.0.0.0:8000"]