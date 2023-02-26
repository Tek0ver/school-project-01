docker build -t scraper:1 -f deployment/scraper/Dockerfile .
docker run --rm -it \
    -e POSTGRES_PASSWORD=$POSTGRES_PASSWORD \
    -v /dev/shm:/dev/shm \
    scraper:1
