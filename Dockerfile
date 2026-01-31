FROM python:3.12-slim

ENV PYTHONUNBUFFERED=1
ENV CELERY_BROKER_URL=redis://redis:6379/0
ENV CELERY_RESULT_BACKEND=redis://redis:6379/0

WORKDIR /code

RUN apt-get update && apt-get install -y build-essential
COPY requirements.txt /code/
RUN pip install --no-cache-dir -r requirements.txt

COPY . /code/