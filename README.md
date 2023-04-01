# school-project-01

## Architecture

- Scraper container will scrap 'le monde' and provide database host on Azure
- The scraper container is triggered everydays by azure function (dont work yet)
- Streamlit app take data from database to visualize data
- Degraded mode: if database is out, data are automatically provide by csv for continuous visualisation

![alt text](ressource/azure.jpg)


## init
Run init-db.sh for initialize Azure database
```
bash deployment/script/init-db.sh
```

## update scraper container on azure
Run azure_update-db.sh for update scraper container on Azure
```
bash deployment/script/azure_update-db.sh
```

## visualize
Click [here](https://tek0ver-school-project-01-deploymentstreamlitstreamlit-1naka4.streamlit.app/?fbclid=IwAR1aP61VhQgQu1M-QXTI4P76xiRbzbfN8jz3OInhtaYcRv-jbrQf6IDf13w)
to go to streamlit