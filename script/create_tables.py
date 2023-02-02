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
    sql = f'''
        CREATE TABLE articles (
            id SERIAL PRIMARY KEY,
            journal VARCHAR(50),
            title VARCHAR(255),
            date TIMESTAMP,
            link VARCHAR(255)
        )
        '''
    
    # Executing the query
    cursor.execute(sql)
    print("Table created !")
    
    # Commit your changes in the database
    conn.commit()
    # Closing the connection
    conn.close()



if __name__ == "__main__":
    main()