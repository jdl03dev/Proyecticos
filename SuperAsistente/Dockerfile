FROM python:3.12.2-slim

# Instala herramientas de compilación y bibliotecas necesarias
RUN apt-get update && apt-get install -y \
    git \
    build-essential \
    ffmpeg \
    libsndfile1 \
    portaudio19-dev \
    python3-dev \
    libffi-dev \
    libasound-dev \
    && apt-get clean

WORKDIR /app
COPY . /app

RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "main.py"]
