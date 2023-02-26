FROM python:3.9-slim

WORKDIR /app

COPY deployment/init_database/requirements.txt .

RUN apt-get update -y
RUN pip3 install -r requirements.txt

COPY deployment/init_database/init_database.py .
COPY deployment/config.py .

CMD ["python3", "init_database.py"]