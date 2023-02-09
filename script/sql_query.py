from os import environ
import pandas as pd
from sqlalchemy import create_engine
import psycopg2


def main():
    select_tables()
    df = database_to_df("articles")
    print(df)
    # drop_table("articles")




def select_tables():
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
    
    cur = conn.cursor()
    
    # create table
    sql = f'''
        SELECT *
        FROM articles
        '''
    
    # Executing the query
    cur.execute(sql)
    rows = cur.fetchall()
    for row in rows:
        print(row)
    cur.close()
    # Commit your changes in the database
    conn.commit()
    # Closing the connection
    conn.close()




def database_to_df(table: str):
    """
    select all from table set in parameter from database with sql query \n
    return a dataframe
    """
    query = f"""
        SELECT *
        FROM {table};
        """

    conn_string = f'postgresql://{environ["POSTGRES_USER"]}:{environ["POSTGRES_PASSWORD"]}@{environ["POSTGRES_HOST"]}/{environ["POSTGRES_DB"]}'
    conn = create_engine(conn_string).connect()
    df = pd.read_sql_query(sql=query,con=conn)
    conn.close()

    return df


def drop_table(table: str):
    """
    drop a table set in parameter
    """
    conn=psycopg2.connect(
        database=environ["POSTGRES_DB"],
        user=environ["POSTGRES_USER"],
        password=environ["POSTGRES_PASSWORD"],
        host=environ["POSTGRES_HOST"],
        port="5432"
    )
    
    cursor = conn.cursor()
    
    # drop table
    sql = f'''DROP TABLE {table}'''
    
    # Executing the query
    cursor.execute(sql)
    print("Table dropped !")
    
    # Commit your changes in the database
    conn.commit()
    
    # Closing the connection
    conn.close()


if __name__ == '__main__':
    main()