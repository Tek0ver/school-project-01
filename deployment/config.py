from os import environ

# connection parameters to sql server
param_dict = {
    "host"      : "postgres",
    "database"  : "postgres",
    "user"      : "postgres",
    "password"  : "postgres"
}

database_name = "vinci"

# azure conn string
azure_conn_admin = f"host=vinci.postgres.database.azure.com port=5432 dbname=postgres user=postgres password={environ['POSTGRES_PASSWORD']} sslmode=require"
azure_conn_user = f"host=vinci.postgres.database.azure.com port=5432 dbname={database_name} user=postgres password={environ['POSTGRES_PASSWORD']} sslmode=require"

# number of page to scrap (set 0 for all) until reach title in save.txt
nb_page = 0

# headless mod for selenium driver
headless = True

# choose what you want update
article = True
content = True

# export
csv = False
database = True

# scrap only most recent articles than last time
only_new_articles = True