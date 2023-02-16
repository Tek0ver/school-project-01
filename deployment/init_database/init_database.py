import psycopg2
from os import environ



def main():
    create_tables()


def create_tables():
    """
    create a table set in parameter
    """
    conn=psycopg2.connect(
        database=environ["POSTGRES_DB"],
        user=environ["POSTGRES_USER"],
        password=environ["POSTGRES_PASSWORD"],
        host=environ["POSTGRES_HOST"],
        port="5432"
    )
    
    cursor = conn.cursor()
    
    # create table
    queries = [
        """
        CREATE TABLE articles (
            id SERIAL PRIMARY KEY,
            journal VARCHAR(50),
            title VARCHAR(255),
            article_date TIMESTAMP,
            link VARCHAR(255)
        );
        """,
        """
        CREATE TABLE contents (
            id SERIAL PRIMARY KEY,
            article_id INTEGER NOT NULL,
            content TEXT,
            nb_words INTEGER,
            FOREIGN KEY (article_id)
            REFERENCES articles (id)
        );
        """,
        """
        CREATE TABLE cities (
            id SERIAL PRIMARY KEY,
            city VARCHAR (50),
            population_2022 INTEGER
        );
        """,
        """
        CREATE TABLE content_cities (
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
    
    # Commit your changes in the database
    conn.commit()
    # Closing the connection
    conn.close()



if __name__ == "__main__":
    main()