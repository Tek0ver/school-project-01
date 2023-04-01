from toolbox import DatabaseInterface

from geopy.geocoders import Nominatim
import qwikidata.sparql

databaseInterface = DatabaseInterface()


def main():
    """update table geo_city [[city, latitude, longitude, count]]"""

    query = """
        SELECT article_date, city
        FROM articles
        JOIN contents ON articles.id = contents.article_id
        JOIN content_cities ON contents.id = content_cities.content_id
        WHERE article_date > '2021-06-01'
        ORDER BY article_date
        ;
    """
    df_city = databaseInterface.select(query)

    cities = select_cities()
    # drop city that already in geocity table for avoid over calculation
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
    df_geocity["population_2023"] = df_geocity["city"].apply(population)
    df_geocity = df_geocity.dropna()

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
        print(f"[warning] latitude of {city} not found")


def longitude(city: str):
    """return city's longitude"""
    # Initialize Nominatim API
    geolocator = Nominatim(user_agent="MyApp")
    location = geolocator.geocode(city)
    try:
        lon = location.longitude
        return lon
    except:
        print(f"[warning] longitude of {city} not found")


def population(city:str, country:str ='Ukraine'):
    langs = ['fr', 'en']
    for lang in langs:
        query = """
        SELECT ?city ?cityLabel ?country ?countryLabel ?population
        WHERE
        {
        ?city rdfs:label '%s'@%s.
        ?city wdt:P1082 ?population.
        ?city wdt:P17 ?country.
        ?city rdfs:label ?cityLabel.
        ?country rdfs:label ?countryLabel.
        FILTER(CONTAINS(?countryLabel, "%s")).
        }
        """ % (city, lang, country)
        
        try:
            res = qwikidata.sparql.return_sparql_query_results(query)
            out = res['results']['bindings'][0]
            return out['population']['value']
        except:
            pass
    print(f"[warning] population of {city} not found")



if __name__ == "__main__":
    main()
