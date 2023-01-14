import psycopg2
import config

def get_table():
    # an example function for sql query
    query = """
        SELECT *
        FROM le_monde;
        """

    conn = None
    try:
        conn = psycopg2.connect(dbname= config.database, user=config.user, password=config.password, host=config.host)
        cur = conn.cursor()
        cur.execute(query)
        row = cur.fetchone()

        while row is not None:
            print(row)
            row = cur.fetchone()

        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()


if __name__ == '__main__':
    get_table()