docker build -t articles:1 --shm-size 500mb -f deployment/scraper/Dockerfile .
docker tag articles:1 vincipubliccr.azurecr.io/articles:1
docker push vincipubliccr.azurecr.io/articles:1
az container create \
    --resource-group school-project-public-rg \
    --name articles \
    --image vincipubliccr.azurecr.io/articles:1 \
    --registry-username vincipubliccr \
    --registry-password $REGISTRY_PASSWORD \
    --secure-environment-variables POSTGRES_PASSWORD=$POSTGRES_PASSWORD \
    --location westeurope \
    --restart-policy OnFailure

    # use volume if --shm-size dont work, but before that try to increase shm size(500mb work)
    # --azure-file-volume-account-name dockervolumevincipublic \
    # --azure-file-volume-account-key $AZURE_FILE_VOLUME_ACCOUNT_KEY \
    # --azure-file-volume-share-name shm \
    # --azure-file-volume-mount-path /dev/shm/ \