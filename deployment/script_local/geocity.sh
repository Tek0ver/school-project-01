docker build -t geocity:1 -f deployment/scraper/geocity/Dockerfile .
docker run --rm -it \
    -e POSTGRES_PASSWORD=$POSTGRES_PASSWORD \
    geocity:1
