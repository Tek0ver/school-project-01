docker build -t scraper:1 -f scraper/Dockerfile .
docker tag scraper:1 vincicr.azurecr.io/scraper:1
docker push vincicr.azurecr.io/scraper:1