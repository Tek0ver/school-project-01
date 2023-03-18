import config
import ukraine_cities
from toolbox import DatabaseInterface

import pandas as pd

import psycopg2
import locationtagger
import nltk


databaseInterface = DatabaseInterface()


# essential entity models downloads
nltk.downloader.download("maxent_ne_chunker")
nltk.downloader.download("words")
nltk.downloader.download("treebank")
nltk.downloader.download("maxent_treebank_pos_tagger")
nltk.downloader.download("punkt")
nltk.download("averaged_perceptron_tagger")


def main():
    conn = psycopg2.connect(config.azure_conn_user)

    # get the number of row in content_cities table for process only not exist row
    count_content_cities = content_cities_count(conn)
    # select contents
    contents = select_contents(conn, count_content_cities)
    # create dataframe "content_id", "city"
    df = extract_cities(contents)
    # export to database
    databaseInterface.export_to_database(df, table="content_cities")
    print("content_cities updated")

    conn.close()


def select_contents(conn, count_content_cities: int):
    if count_content_cities > 0:
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
    else:
        query = """
            SELECT id, content
            FROM contents
            ORDER BY id ASC
            ;
            """

    cursor = conn.cursor()
    cursor.execute(query)
    contents = cursor.fetchall()

    return contents


def extract_cities(contents):
    df = pd.DataFrame(columns=["content_id", "city"])

    for content in contents:
        if len(content[1]) > 0:
            content_id = content[0]
            cities = Extract(content[1]).cities()
            for city in cities:
                if city in ukraine_cities.ukraine_cities:
                    row = [content_id, city]
                    df.loc[len(df)] = row

    return df


def content_cities_count(conn):
    """return the number of rows in content_cities table"""

    query = """
        select count(*) from content_cities;
    """
    cursor = conn.cursor()
    cursor.execute(query)
    count = cursor.fetchall()

    return count[0][0]


class Extract:
    def __init__(self, content):
        self.place_entity = locationtagger.find_locations(text=content)

    def country(self):
        # getting all countries
        return [w for w in self.place_entity.countries]

    def cities(self):
        # getting all cities
        return [w for w in self.place_entity.cities]


if __name__ == "__main__":
    main()
