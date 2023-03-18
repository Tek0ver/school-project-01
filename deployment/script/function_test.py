import os

os.system("az login --service-principal --username $AZURE_SERVICE_PRINCIPAL_APPID --password $AZURE_SERVICE_PRINCIPAL_PASSWORD --tenant $AZURE_SERVICE_PRINCIPAL_TENANT")
os.system("az container start --name update-db --resource-group school-project-public-rg")