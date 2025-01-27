FROM python:3.12.8-slim-bookworm
LABEL authors="stanislawski"
WORKDIR /usr/src/plateDetector

RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    build-essential \
    gfortran \
    libopenblas-dev \
    liblapack-dev \
    libatlas-base-dev \
    pkg-config \
    libgl1-mesa-glx \
    libglib2.0-0 \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

COPY . .

RUN pip3 install --upgrade pip setuptools

RUN  pip3 install --upgrade pip setuptools && pip3 install --no-cache-dir -r requirements.txt

CMD ["gunicorn", "-w", "1", "-k", "uvicorn.workers.UvicornWorker", "main:app", "--bind", "0.0.0.0:8001"]