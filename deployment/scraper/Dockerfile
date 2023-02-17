FROM selenium/standalone-chrome

WORKDIR /app

COPY ./requirements.txt .

RUN sudo apt-get update -y
RUN sudo apt-get install python3-pip -y
RUN pip3 install -r requirements.txt

COPY . .

CMD ["python3", "etl.py"]
