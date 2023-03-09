FROM python:3.9-slim

WORKDIR /app

COPY deployment/scraper/extract_city/requirements.txt .

RUN apt-get update -y
RUN pip3 install -r requirements.txt
RUN python -m spacy download en_core_web_sm
RUN python -m spacy download fr_core_news_sm 

COPY deployment/scraper/extract_city/ .

CMD ["python3", "extract_city.py"]