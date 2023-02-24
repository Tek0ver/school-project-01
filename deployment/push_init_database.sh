docker build -t init_database:1 -f init_database/Dockerfile .
docker tag init_database:1 vincicr.azurecr.io/init_database:1
docker push vincicr.azurecr.io/init_database:1