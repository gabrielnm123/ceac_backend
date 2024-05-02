FROM python:3.12.1

COPY . /app/.

RUN apt update && pip install --upgrade pip && pip install -r /app/requirements.txt
