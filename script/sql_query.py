from os import environ
import pandas as pd
from sqlalchemy import create_engine


def main():
    db_to_df("le_monde")


def db_to_df(table: str):
    # an example function for sql query
    query = f"""
        SELECT *
        FROM {table};
        """

    conn_string = f'postgresql://{environ["POSTGRES_USER"]}:{environ["POSTGRES_PASSWORD"]}@{environ["POSTGRES_HOST"]}/{environ["POSTGRES_DB"]}'
    conn = create_engine(conn_string).connect()
    df = pd.read_sql_query(sql=query,con=conn)
    conn.close()

    return df



if __name__ == '__main__':
    main()