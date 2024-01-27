FROM python:3.11
ENV PYTHONUNBUFFERED=1
RUN apt-get update && apt-get install -y python3-dev default-libmysqlclient-dev build-essential pkg-config
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt --no-cache-dir
COPY . .
