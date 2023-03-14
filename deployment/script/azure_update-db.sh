az login -u $AZURE_MAIL -p $AZURE_PASSWORD

docker build -t update-db:1 --shm-size 1gb -f deployment/scraper/update-db/Dockerfile .
docker tag update-db:1 vincipubliccr.azurecr.io/update-db:1
docker push vincipubliccr.azurecr.io/update-db:1

az container create \
    --resource-group school-project-public-rg \
    --name city \
    --image vincipubliccr.azurecr.io/update-db:1 \
    --registry-username vincipubliccr \
    --registry-password $REGISTRY_PASSWORD \
    --secure-environment-variables POSTGRES_PASSWORD=$POSTGRES_PASSWORD \
    --restart-policy OnFailure \
    --location westeurope
    # use volume if --shm-size dont work, but before that try to increase shm size(1gb work)
    # --azure-file-volume-account-name dockervolumevincipublic \
    # --azure-file-volume-account-key $AZURE_FILE_VOLUME_ACCOUNT_KEY \
    # --azure-file-volume-share-name shm \
    # --azure-file-volume-mount-path /dev/shm/ \


az container start --name update-db --resource-group school-project-public-rg
echo database updated