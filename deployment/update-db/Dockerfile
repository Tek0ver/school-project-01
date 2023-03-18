FROM selenium/standalone-chrome

WORKDIR /app

COPY deployment/update-db/requirements.txt .

RUN sudo apt-get update -y \
    && sudo apt-get install python3-pip -y
RUN pip3 install -r requirements.txt
RUN python3 -m spacy download en_core_web_sm \
    && python3 -m spacy download fr_core_news_sm

COPY deployment/update-db/ .

CMD ["bash", "start.sh"]