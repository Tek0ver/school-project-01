FROM python:3.9-slim

WORKDIR /app

COPY deployment/init-db/requirements.txt .

RUN apt-get update -y
RUN pip3 install -r requirements.txt

COPY deployment/init-db/ .

CMD ["python3", "init_db.py"]