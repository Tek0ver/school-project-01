FROM selenium/standalone-chrome

WORKDIR /app

COPY deployment/scraper/articles/requirements.txt .

RUN sudo apt-get update -y
RUN sudo apt-get install python3-pip -y
RUN pip3 install -r requirements.txt

COPY deployment/scraper/articles/ .

CMD ["python3", "etl.py"]
