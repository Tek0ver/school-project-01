import os

os.system("az login --service-principal --username 'b929ed1d-dc29-4f80-b3ea-fee5aaf43edf' --password 'ypH8Q~-HSGTKiMxGtDRzCF1OlgkcJMNuWuA_ObPU' --tenant 'b7b023b8-7c32-4c02-92a6-c8cdaa1d189c'")
os.system("az container start --name update-db --resource-group school-project-public-rg")