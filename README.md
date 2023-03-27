# school-project-01

## Architecture

- Scraper container will scrap 'le monde' and provide database host on Azure
- (dont work yet) The scraper container is trigger every days by azure function
- Streamlit use database to visualize data

![alt text](ressource/azure.jpg)


## init
Run init-db.sh for initialize Azure database
```
bash script/init-db.sh
```

## update scraper container on azure
Run script/azure_update-db.sh for update scraper container on Azure
```
bash script/azure_update-db.sh
```

## visualize
Click [here](https://tek0ver-school-project-01-deploymentstreamlitstreamlit-1naka4.streamlit.app/?fbclid=IwAR1aP61VhQgQu1M-QXTI4P76xiRbzbfN8jz3OInhtaYcRv-jbrQf6IDf13w)
to go to streamlit