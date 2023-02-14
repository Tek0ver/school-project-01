FROM python

WORKDIR /app

# install google chrome
RUN apt-get -y update
RUN apt-get -y install wget
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add -
RUN sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list'
RUN apt-get install -y google-chrome-stable

COPY . .

RUN pip3 install -r requirements.txt

CMD ["python3", "etl.py"]
