FROM python:3.12.8-slim
LABEL authors="stanislawski"

WORKDIR /usr/src/flaskApp

RUN apt-get update && apt-get install -y \
    gcc \
    uwsgi-plugin-python3

COPY . .

RUN pip3 install --no-cache-dir -r requirements.txt

CMD ["uwsgi", "--socket", "0.0.0.0:8000", "--protocol=http", "-w", "wsgi:app"]