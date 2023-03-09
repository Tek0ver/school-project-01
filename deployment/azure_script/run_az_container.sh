az login -u $AZURE_MAIL -p $AZURE_PASSWORD

az container start --name articles \
                   --resource-group school-project-public-rg

echo articles succeded

az container start --name contents \
                   --resource-group school-project-public-rg
                
echo contents succeded

az container start --name city \
                   --resource-group school-project-public-rg

echo city succeded
