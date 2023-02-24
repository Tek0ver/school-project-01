import config
import psycopg2


def main():
    if not exist(config.database_name):
        create_database(config.database_name)
        create_tables()



def exist(database: str):
    with psycopg2.connect(config.azure_conn_admin) as conn:
        cursor = conn.cursor()
        cursor.execute(f"SELECT datname FROM pg_catalog.pg_database WHERE datname = '{database}'")
        exists = cursor.fetchone()

    if exists:
        print(f"{database} already exist")
        return True



def create_database(database: str):
    conn =  psycopg2.connect(config.azure_conn_admin)
    conn.autocommit = True
    cursor = conn.cursor()

    cursor.execute(f'CREATE DATABASE {database}')
    
    conn.close()

    print(f"{database} created")



def create_tables():
    """
    create a table set in parameter
    """
    with psycopg2.connect(config.azure_conn_user) as conn:
        cursor = conn.cursor()
        
        queries = [
            """
            CREATE TABLE IF NOT EXISTS articles (
                id SERIAL PRIMARY KEY,
                journal VARCHAR(50),
                title VARCHAR(255),
                article_date TIMESTAMP,
                link VARCHAR(255)
            );
            """,
            """
            CREATE TABLE IF NOT EXISTS contents (
                id SERIAL PRIMARY KEY,
                article_id INTEGER NOT NULL,
                content TEXT,
                nb_words INTEGER,
                FOREIGN KEY (article_id)
                REFERENCES articles (id)
            );
            """,
            """
            CREATE TABLE IF NOT EXISTS cities (
                id SERIAL PRIMARY KEY,
                city VARCHAR (50),
                population_2022 INTEGER
            );
            """,
            """
            CREATE TABLE IF NOT EXISTS content_cities (
                id SERIAL PRIMARY KEY,
                content_id INTEGER NOT NULL,
                city_id INTEGER NOT NULL,
                nb_occurence INTEGER,
                FOREIGN KEY (content_id)
                REFERENCES contents (id),
                FOREIGN KEY (city_id)
                REFERENCES cities (id)
            );
            """
        ]
        
        # Executing the query
        for query in queries:
            cursor.execute(query)
            print("Table created !")


if __name__ == "__main__":
    main()