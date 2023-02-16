import psycopg2
from os import environ



def main():
    create_tables()


def create_tables():
    """
    create a table set in parameter
    """
    conn = psycopg2.connect(
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
        CREATE TABLE IF NOT EXISTS articles (
            id SERIAL PRIMARY KEY,
            journal VARCHAR(50),
            title VARCHAR(255),
            date TIMESTAMP,
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