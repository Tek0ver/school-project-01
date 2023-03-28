import psycopg2
import pandas as pd
import config

queries = {
    "query_articles":
        """
        SELECT * FROM articles
        WHERE article_date > '2022-01-01'
        ;
        """,
    "query_cities_from_articles":
        """
        SELECT article_date, content_cities.city, latitude, longitude
        FROM articles
        JOIN contents ON articles.id = contents.article_id
        JOIN content_cities ON contents.id = content_cities.content_id
        JOIN geocity ON content_cities.city = geocity.city
        ORDER BY article_date
        ;
        """
}

class DatabaseInterface:

    def __init__(self):
        self.mode = 'azure'
        try:
            self.conn = psycopg2.connect(config.azure_conn_user)
            self.cursor = self.conn.cursor()
            print(f"[SUCCESS] Connected to azure database {config.database_name}")
        except:
            self.mode = 'local'
            print('[FAIL] Database failure, local mode activated.')
            self.data = {
                'articles': pd.read_csv('./data-offline/articles.csv', date_parser=pd.Timestamp),
                'content_cities': pd.read_csv('./data-offline/content_cities.csv'),
                'contents': pd.read_csv('./data-offline/contents.csv'),
                'geocity': pd.read_csv('./data-offline/geocity.csv')
                }

            # convert datetime
            self.data['articles']['article_date'] = pd.to_datetime(self.data['articles']['article_date'])

            print("[SUCCESS] Connected to local csv")

    def select(self, query: str) -> pd.DataFrame:
        if self.mode == 'azure':
            self.cursor.execute(queries[query])
            data = self.cursor.fetchall()
            column_names = [desc[0] for desc in self.cursor.description]
            dataframe = pd.DataFrame(data, columns=column_names)
            return dataframe
        elif self.mode == 'local':
            if query == "query_articles":
                return self.data['articles']
            elif query == "query_cities_from_articles":
                df = pd.merge(
                    self.data['articles'],
                    self.data['contents'], 
                    left_on='id', 
                    right_on='article_id', 
                    how='inner'
                )
                df = pd.merge(
                    df,
                    self.data['content_cities'],
                    left_on='id_y', 
                    right_on='id', 
                    how='inner'
                )
                df = pd.merge(
                    df,
                    self.data['geocity'],
                    left_on='city', 
                    right_on='city', 
                    how='inner'
                )

                df = df[['article_date', 'city', 'latitude', 'longitude']]
                return df
