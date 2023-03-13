FROM selenium/standalone-chrome

WORKDIR /app

COPY deployment/update-db/requirements.txt .

RUN sudo apt-get update -y
RUN sudo apt-get install python3-pip -y
RUN pip3 install -r requirements.txt
Run python3 -m spacy download en_core_web_sm
RUN python3 -m spacy download fr_core_news_sm

COPY deployment/update-db/ .

CMD ["bash", "start.sh"]