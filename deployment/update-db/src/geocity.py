from toolbox import DatabaseInterface

from geopy.geocoders import Nominatim

databaseInterface = DatabaseInterface()


def main():
    """update table geo_city [[city, latitude, longitude, count]]"""

    query = """
        SELECT article_date, city
        FROM articles
        JOIN contents ON articles.id = contents.article_id
        JOIN content_cities ON contents.id = content_cities.content_id
        WHERE article_date > '2022-01-01'
        ORDER BY article_date
        ;
    """
    df_city = databaseInterface.select(query)

    cities = select_cities()
    for city in cities:
        df_city = df_city.drop(df_city[df_city["city"] == city].index)
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

    print(df_geocity)

    databaseInterface.export_to_database(df_geocity, table="geocity")
    print("geocity updated")


def select_cities():
    """create dataframe [[city]]"""
    query = """
        SELECT city
        FROM geocity
        ;
        """

    cities = databaseInterface.select(query)

    return cities["city"]


def latitude(city: str):
    """return city's latitude"""
    # Initialize Nominatim API
    geolocator = Nominatim(user_agent="MyApp")
    location = geolocator.geocode(city)
    try:
        lat = location.latitude
        return lat
    except:
        print(city)


def longitude(city: str):
    """return city's longitude"""
    # Initialize Nominatim API
    geolocator = Nominatim(user_agent="MyApp")
    location = geolocator.geocode(city)
    try:
        lon = location.longitude
        return lon
    except:
        print(city)


if __name__ == "__main__":
    main()
