docker build -t update-db:1 -f deployment/update-db/Dockerfile .
docker run --rm -it \
    -e POSTGRES_PASSWORD=$POSTGRES_PASSWORD \
    -v /dev/shm:/dev/shm \
    update-db:1
