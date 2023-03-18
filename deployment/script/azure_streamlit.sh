image_name=streamlit

docker build -t $image_name:1 -f deployment/$image_name/Dockerfile .
docker tag $image_name:1 vincipubliccr.azurecr.io/$image_name:1
docker push vincipubliccr.azurecr.io/$image_name:1
az container create \
    --resource-group school-project-public-rg \
    --name $image_name \
    --image vincipubliccr.azurecr.io/$image_name:1 \
    --registry-username vincipubliccr \
    --registry-password $REGISTRY_PASSWORD \
    --secure-environment-variables POSTGRES_PASSWORD=$POSTGRES_PASSWORD \
    --ip-address Public \
    --ports 8501 \
    --restart-policy never \
    --location westeurope