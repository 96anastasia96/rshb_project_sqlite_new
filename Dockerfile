FROM python:3.10-alpine

COPY requirements.txt /requirements.txt

RUN pip install -r /requirements.txt

RUN adduser --disabled-password user
USER user

COPY config /config
WORKDIR /config

EXPOSE 8000