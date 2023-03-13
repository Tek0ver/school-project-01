from toolbox import DatabaseInterface
import config

import psycopg2
import pandas as pd
from geopy.geocoders import Nominatim
from io import StringIO

databaseInterface = DatabaseInterface()


def main():
    conn = psycopg2.connect(config.azure_conn_user)

    query_city = """
        SELECT article_date, city
        FROM articles
        JOIN contents ON articles.id = contents.article_id
        JOIN content_cities ON contents.id = content_cities.content_id
        WHERE article_date > '2022-01-01'
        ORDER BY article_date
        ;
    """
    df_city = load_data(query_city)
    df_city["city"] = df_city["city"].str.capitalize()

    df_geocity = (
        df_city.groupby(["city"])
        .count()
        .sort_values("article_date", ascending=False)
        .reset_index()
    )
    df_geocity = df_geocity.rename(columns={"article_date": "count"})
    df_geocity["latitude"] = df_geocity["city"].apply(latitude)
    df_geocity["longitude"] = df_geocity["city"].apply(longitude)
    df_geocity = df_geocity.dropna()

    export_to_database(conn, df_geocity, table="geocity")

    conn.close()


def load_data(query):
    return databaseInterface.select(query)


def latitude(city: str):
    # Initialize Nominatim API
    geolocator = Nominatim(user_agent="MyApp")
    location = geolocator.geocode(city)
    try:
        lat = location.latitude
        return lat
    except:
        print(city)


def longitude(city: str):
    # Initialize Nominatim API
    geolocator = Nominatim(user_agent="MyApp")
    location = geolocator.geocode(city)
    try:
        lon = location.longitude
        return lon
    except:
        print(city)


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
