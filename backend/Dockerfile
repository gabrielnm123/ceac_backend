FROM python:3.12.1

COPY requirements.txt /app/requirements.txt

RUN apt update && apt install -y libmariadb-dev && pip install --upgrade pip && pip install -r /app/requirements.txt && rm /app/requirements.txt