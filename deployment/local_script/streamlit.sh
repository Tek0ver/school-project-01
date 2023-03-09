docker build -t streamlit:1 -f deployment/streamlit/Dockerfile .
docker run --rm -it \
    -e POSTGRES_PASSWORD=$POSTGRES_PASSWORD \
    streamlit:1
