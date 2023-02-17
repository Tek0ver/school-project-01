# app/Dockerfile

FROM python:3.9-slim

WORKDIR /app

RUN apt-get

RUN pip3 install -r requirements.txt

COPY . .

CMD ["python3", "init_database.py"]