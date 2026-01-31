FROM python:3.12-slim

ENV PYTHONUNBUFFERED=1

WORKDIR /code

RUN apt-get update && apt-get install -y build-essential
COPY requirements.txt /code/
RUN pip install --no-cache-dir -r requirements.txt

COPY . /code/