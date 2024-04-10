# Usar una imagen oficial de Python como imagen base
FROM python:3.12

# Actualizar el sistema e instalar dependencias necesarias para SciPy, Scikit-learn, Tensorflow, Keras, etc.
RUN apt-get update && apt-get install -y \
    build-essential \
    libblas-dev \
    liblapack-dev \
    libatlas-base-dev \
    gfortran \
    libhdf5-dev \
    libfreetype6-dev \
    libpng-dev \
    libzmq3-dev \
    pkg-config \
    software-properties-common \
    swig \
    curl \
    git \
    g++ \
    gcc \
    && apt-get clean

# Establecer el directorio de trabajo en el contenedor
WORKDIR /app

# Copiar Pipfile y Pipfile.lock al contenedor
COPY Pipfile Pipfile.lock /app/

# Instalar pipenv y las dependencias del proyecto
RUN pip install --upgrade pip && \
    pip install pipenv && \
    pipenv install --system --deploy

# Copiar el resto del código de la aplicación al contenedor
COPY . /app

# Exponer el puerto 5000
EXPOSE 5000

# Comando para ejecutar la aplicación usando Uvicorn con configuraciones "production-ready"
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "5000"]
