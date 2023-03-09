docker build -t extract_city:1 -f deployment/extract_city/Dockerfile .
docker run --rm -it \
    -e POSTGRES_PASSWORD=$POSTGRES_PASSWORD \
    extract_city:1
