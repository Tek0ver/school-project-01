import config
import ukraine_cities

import pandas as pd

import psycopg2
import locationtagger
import nltk

from io import StringIO


# essential entity models downloads
nltk.downloader.download("maxent_ne_chunker")
nltk.downloader.download("words")
nltk.downloader.download("treebank")
nltk.downloader.download("maxent_treebank_pos_tagger")
nltk.downloader.download("punkt")
nltk.download("averaged_perceptron_tagger")


def main():
    conn = psycopg2.connect(config.azure_conn_user)
    query = """
        SELECT id, content
        FROM contents
        WHERE id > (
            SELECT MAX(content_id)
            FROM content_cities
        )
        ORDER BY id ASC
        ;
        """

    cursor = conn.cursor()
    cursor.execute(query)
    contents = cursor.fetchall()

    df = pd.DataFrame(columns=["content_id", "city"])

    for content in contents:
        if len(content[1]) > 0:
            content_id = content[0]
            cities = Extract(content[1]).cities()
            for city in cities:
                if city in ukraine_cities.ukraine_cities:
                    row = [content_id, city]
                    df.loc[len(df)] = row

    print(df)

    export_to_database(conn, df, table="content_cities")

    conn.close()


class Extract:
    def __init__(self, content):
        self.place_entity = locationtagger.find_locations(text=content)

    def country(self):
        # getting all countries
        return [w for w in self.place_entity.countries]

    def cities(self):
        # getting all cities
        return [w for w in self.place_entity.cities]


def export_to_database(conn, df: pd.DataFrame, table: str):
    """
    export to postgresql table
    """
    # save dataframe to an in memory buffer
    cols = tuple(df.columns)
    buffer = StringIO()
    # export
    df.to_csv(buffer, header=False, index=False, sep=";")
    buffer.seek(0)
    cursor = conn.cursor()
    cursor.copy_from(buffer, table, sep=";", columns=cols)
    conn.commit()


if __name__ == "__main__":
    main()
