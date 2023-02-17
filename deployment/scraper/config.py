# connection parameters to sql server
param_dict = {
    "host"      : "postgres",
    "database"  : "postgres",
    "user"      : "postgres",
    "password"  : "postgres"
}

# number of page to scrap (set 0 for all) until reach title in save.txt
nb_page = 1

# headless mod for selenium driver
headless = True

# choose what you want update
article = True
content = True