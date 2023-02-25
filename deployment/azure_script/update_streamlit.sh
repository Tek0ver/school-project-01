docker build -t streamlit:1 -f streamlit/Dockerfile .
docker tag streamlit:1 vincipubliccr.azurecr.io/streamlit:1
docker push vincipubliccr.azurecr.io/streamlit:1
az container create \
    --resource-group school-project-public-rg \
    --name streamlit \
    --image vincipubliccr.azurecr.io/streamlit:1 \
    --registry-username vincipubliccr \
    --registry-password $REGISTRY_PASSWORD \
    --secure-environment-variables POSTGRES_PASSWORD=$POSTGRES_PASSWORD \
    --ip-address Public \
    --ports 8501 \
    --restart-policy never \
    --location westeurope