# connection parameters to sql server
param_dict = {
    "host"      : "postgres",
    "database"  : "postgres",
    "user"      : "postgres",
    "password"  : "postgres"
}

# azure conn string
azure_conn_admin = "host=vinci.postgres.database.azure.com port=5432 dbname=postgres user=postgres password=Vincisql01 sslmode=require"
azure_conn_user = "host=vinci.postgres.database.azure.com port=5432 dbname=dev user=postgres password=Vincisql01 sslmode=require"

# number of page to scrap (set 0 for all) until reach title in save.txt
nb_page = 1

# headless mod for selenium driver
headless = True

# choose what you want update
article = True
content = False

# export
csv = False
database = True

# scrap only most recent articles than last time
only_new_articles = False