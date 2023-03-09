from os import environ

# name of database
database_name = "test"

# azure sql conn string
azure_conn_admin = f"host=vinci-db.postgres.database.azure.com port=5432 dbname=postgres user=postgres password={environ['POSTGRES_PASSWORD']} sslmode=require"
azure_conn_user = f"host=vinci-db.postgres.database.azure.com port=5432 dbname={database_name} user=postgres password={environ['POSTGRES_PASSWORD']} sslmode=require"

# number of page to scrap (set 0 for all)
nb_page = 0

# size of batch of contents to export
batch_size = 10

# headless mod for selenium driver
headless = True

# choose what you want update
article = False
content = True

# export
csv = False
database = True

# scrap only most recent articles than last time
only_new_articles = True