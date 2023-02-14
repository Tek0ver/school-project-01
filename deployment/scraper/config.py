# connection parameters to sql server
param_dict = {
    "host"      : "localhost",
    "database"  : "vinci",
    "user"      : "postgres",
    "password"  : "postgres"
}

# number of page to scrap (set 0 for all) until reach title in save.txt
nb_page = 1

# headless mod for selenium driver
headless = True