FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY todolist/ .

ENV PYTHONBUFFERED 1

CMD python manage.py runserver 0.0.0.8000
