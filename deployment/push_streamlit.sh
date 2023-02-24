docker build -t streamlit:1 -f streamlit/Dockerfile .
docker tag streamlit:1 vincicr.azurecr.io/streamlit:1
docker push vincicr.azurecr.io/streamlit:1