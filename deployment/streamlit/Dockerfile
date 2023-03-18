FROM python:3.9-slim

WORKDIR /app

COPY deployment/streamlit/requirements.txt .

RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    software-properties-common \
    git \
    && rm -rf /var/lib/apt/lists/*

RUN pip3 install -r requirements.txt

COPY deployment/streamlit .

EXPOSE 8501

ENTRYPOINT ["streamlit", "run", "./streamlit/streamlit.py", "--server.port=8501", "--server.address=0.0.0.0"]
