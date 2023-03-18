image_name=update-db

az login -u $AZURE_MAIL -p $AZURE_PASSWORD

docker build -t $image_name:1 --shm-size 2gb -f deployment/$image_name/Dockerfile .
docker tag $image_name:1 vincipubliccr.azurecr.io/$image_name:1
docker push vincipubliccr.azurecr.io/$image_name:1

az container create \
    --resource-group school-project-public-rg \
    --name $image_name \
    --image vincipubliccr.azurecr.io/$image_name:1 \
    --registry-username vincipubliccr \
    --registry-password $REGISTRY_PASSWORD \
    --secure-environment-variables POSTGRES_PASSWORD=$POSTGRES_PASSWORD \
    --restart-policy OnFailure \
    --location westeurope
    # use volume if --shm-size dont work, but before that try to increase shm size(2gb work)
    # --azure-file-volume-account-name dockervolumevincipublic \
    # --azure-file-volume-account-key $AZURE_FILE_VOLUME_ACCOUNT_KEY \
    # --azure-file-volume-share-name shm \
    # --azure-file-volume-mount-path /dev/shm/ \


# az container start --name $image_name --resource-group school-project-public-rg
# echo container "$image_name" updated