FROM python:3.9-slim

WORKDIR /app

COPY deployment/scraper/geocity/requirements.txt .

RUN apt-get update -y
RUN pip3 install -r requirements.txt

COPY deployment/scraper/geocity/ .

CMD ["python3", "geocity.py"]