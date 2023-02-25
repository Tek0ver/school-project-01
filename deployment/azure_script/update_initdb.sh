docker build -t init_database:1 -f init_database/Dockerfile .
docker tag init_database:1 vincipubliccr.azurecr.io/init_database:1
docker push vincipubliccr.azurecr.io/init_database:1
az container create \
    --resource-group school-project-public-rg \
    --name initdb \
    --image vincipubliccr.azurecr.io/init_database:1 \
    --registry-username vincipubliccr \
    --registry-password $REGISTRY_PASSWORD \
    --secure-environment-variables POSTGRES_PASSWORD=$POSTGRES_PASSWORD \
    --restart-policy never \
    --location westeurope