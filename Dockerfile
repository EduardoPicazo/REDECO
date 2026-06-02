FROM python:3.12-slim

# Evitar que Python escriba archivos .pyc y forzar logs sin buffer
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Directorio de trabajo en el contenedor
WORKDIR /app

# Copiar archivo de requerimientos e instalar dependencias
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el resto del código fuente al contenedor
COPY . /app/

# Mover el working directory a la carpeta de Django donde está manage.py
WORKDIR /app/NE_REDECO

# Exponer el puerto
EXPOSE 8000

# Comando para correr en producción usando Gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "NE_REDECO.wsgi:application"]
