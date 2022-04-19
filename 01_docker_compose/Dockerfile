# Базовый образ Python
FROM python:3.9-alpine

# Рабочая директория
WORKDIR /usr/src/app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Установка зависимостей для psycopg2
RUN apk update \
    && apk add postgresql-dev gcc python3-dev musl-dev

# Устанавливаем requirements.txt
COPY ./requirements.txt .
RUN pip install -r requirements.txt

# Копируем entrypoint.sh
COPY ./app/entrypoint.sh .
RUN chmod +x entrypoint.sh

# Копируем приложение 
COPY ./app .

ENTRYPOINT ./entrypoint.sh