docker build -t extract_city:1 --shm-size 2gb -f deployment/scraper/extract_city/Dockerfile .
docker tag extract_city:1 vincipubliccr.azurecr.io/extract_city:1
docker push vincipubliccr.azurecr.io/extract_city:1
az container create \
    --resource-group school-project-public-rg \
    --name city \
    --image vincipubliccr.azurecr.io/extract_city:1 \
    --registry-username vincipubliccr \
    --registry-password $REGISTRY_PASSWORD \
    --secure-environment-variables POSTGRES_PASSWORD=$POSTGRES_PASSWORD \
    --restart-policy never \
    --location westeurope