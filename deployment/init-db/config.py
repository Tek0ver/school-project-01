from os import environ

# name of database
database_name = "main"

# azure sql conn string
azure_conn_admin = f"host=vinci-db.postgres.database.azure.com port=5432 dbname=postgres user=postgres password={environ['POSTGRES_PASSWORD']} sslmode=require"
azure_conn_user = f"host=vinci-db.postgres.database.azure.com port=5432 dbname={database_name} user=postgres password={environ['POSTGRES_PASSWORD']} sslmode=require"
