import settings
import psycopg2
import pandas as pd
import config

class DatabaseInterface:

    def __init__(self):
        if settings.mode == 'local':
            self.conn = psycopg2.connect(**settings.database)
        if settings.mode == 'azure':
            self.conn = psycopg2.connect(config.azure_conn_user)

        self.cursor = self.conn.cursor()

    def select(self, query: str) -> pd.DataFrame:
        self.cursor.execute(query)
        data = self.cursor.fetchall()
        column_names = [desc[0] for desc in self.cursor.description]
        dataframe = pd.DataFrame(data, columns=column_names)
        return dataframe

    def save_to_database(self):
        pass
