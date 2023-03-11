docker build -t initdb:1 -f deployment/init_database/Dockerfile .
docker run --rm -it \
    -e POSTGRES_PASSWORD=$POSTGRES_PASSWORD \
    initdb:1
