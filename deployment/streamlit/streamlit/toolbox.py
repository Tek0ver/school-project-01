import settings
import psycopg2
import pandas as pd
import config


class DatabaseInterface:

    def __init__(self):
        self.mode = 'azure'
        try:
            self.conn = psycopg2.connect(config.azure_conn_user)
            self.cursor = self.conn.cursor()
        except:
            #TODO log to implement
            self.mode = 'local'
            print('[FAIL] Database failure, local mode activated.')
            self.data = {
                'articles': pd.read_csv('./data-offline/articles.csv')
                }

    def select(self, query: str) -> pd.DataFrame:
        if self.mode == 'azure':
            self.cursor.execute(query)
            data = self.cursor.fetchall()
            column_names = [desc[0] for desc in self.cursor.description]
            dataframe = pd.DataFrame(data, columns=column_names)
            return dataframe
        elif self.mode == 'local':
            return self.data['articles']

    def save_to_database(self):
        pass
