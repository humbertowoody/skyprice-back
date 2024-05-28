#
#
#  .d8888b. 888             8888888b.        d8b
# d88P  Y88b888             888   Y88b       Y8P
# Y88b.     888             888    888
#  "Y888b.  888  888888  888888   d88P888d888888 .d8888b .d88b.
#     "Y88b.888 .88P888  8888888888P" 888P"  888d88P"   d8P  Y8b
#       "888888888K 888  888888       888    888888     88888888
# Y88b  d88P888 "88bY88b 888888       888    888Y88b.   Y8b.
#  "Y8888P" 888  888 "Y88888888       888    888 "Y8888P "Y8888
#                        888
#                   Y8b d88P
#                    "Y88P"               (C) Humberto Alejandro Ortega Alcocer
#
# Dockerfile para una aplicación FastAPI con Uvicorn y Pipenv


# Usar una imagen oficial de Python como imagen base
FROM python:3.12-slim as builder

# Actualizar el sistema e instalar dependencias necesarias para SciPy, Scikit-learn, Tensorflow, Keras, etc.
RUN apt-get update && apt-get install -y --no-install-recommends \
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
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Establecer el directorio de trabajo en el contenedor
WORKDIR /app

# Copiar Pipfile y Pipfile.lock al contenedor
COPY Pipfile Pipfile.lock /app/

# Instalar pipenv y las dependencias del proyecto
RUN pip install --upgrade pip pipenv && \
    pipenv install --system --deploy

# Copiar el resto del código de la aplicación al contenedor
COPY . /app

# Etapa final
FROM python:3.12-slim as run

# Copiar los archivos de la etapa anterior
COPY --from=builder /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin
COPY --from=builder /app /app

# Establecer el directorio de trabajo en el contenedor
WORKDIR /app

# Instalar dependencias adicionales
RUN apt-get update && apt-get install -y --no-install-recommends \
    libhdf5-dev \
    libfreetype6-dev \
    libpng-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Exponer el puerto 5000
EXPOSE 5000

# Comando para ejecutar la aplicación usando Uvicorn con configuraciones "production-ready"
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "5000"]
