FROM python:3.9-slim

WORKDIR /app

COPY init_database/requirements.txt .

RUN apt-get update -y
RUN pip3 install -r requirements.txt

COPY init_database/init_database.py .
COPY config.py .

CMD ["python3", "init_database.py"]