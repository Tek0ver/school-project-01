import streamlit as st
import psycopg2
import pandas as pd
from toolbox import DatabaseInterface
import matplotlib.pyplot as plt
from datetime import datetime
import seaborn as sns
from geopy.geocoders import Nominatim
import plotly.express as px


databaseInterface = DatabaseInterface()


################################################# def functions #################################################


@st.cache_data()
def load_data(query):
    return databaseInterface.select(query)


def graph(data, date_range):
    fig, ax = plt.subplots(1, 1)
    data = data[
        (data["article_date"] >= date_range[0])
        & (data["article_date"] <= date_range[1])
    ]
    ax.hist(data["article_date"], bins="auto")

    st.pyplot(fig)


def countplot(df: pd.DataFrame, feature: str, date_range):
    fig = plt.figure()
    df = df[
        (df["article_date"] >= date_range[0]) & (df["article_date"] <= date_range[1])
    ]
    chart = sns.countplot(df, x=feature, order=df[feature].value_counts().index)
    chart.set_xticklabels(
        chart.get_xticklabels(), rotation=60, horizontalalignment="right"
    )
    sns.set(rc={"figure.figsize": (10, 5)})

    st.pyplot(fig)


def bubblemap(df: pd.DataFrame):
    """Data with latitude/longitude and values"""

    fig, ax = plt.subplots()

    fig = px.scatter_mapbox(
        df,
        lat="latitude",
        lon="longitude",
        size="count",
        color="count",
        hover_name="city",
        zoom=3,
        mapbox_style="open-street-map",
        height=700,
    )

    st.pyplot(fig)


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


################################################# def variables #################################################

# articles
query = """
    SELECT * FROM articles
    WHERE article_date > '2022-01-01'
    ;
"""
articles = load_data(query)

# cities
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

query_geocity = """
    SELECT city, count, latitude, longitude
    FROM geocity
    ;
"""

df_geocity = load_data(query_geocity)

# date range
date_min = min(articles["article_date"]).to_pydatetime()
date_max = max(articles["article_date"]).to_pydatetime()


################################################# front #################################################

st.sidebar.header("Menu")
sidebar_menu_00 = st.sidebar.selectbox(
    "Analyse", ("Couverture médiatique", "Heatmap des villes")
)

if sidebar_menu_00 == "Couverture médiatique":

    st.header("Data")
    st.write(articles)

    st.header("Graphique")

    # TODO: Make sure that date goes at least to the first to the last article
    date_range = st.slider("Range de date voulu ?", value=(date_min, date_max))

    graph(articles, date_range)


elif sidebar_menu_00 == "Heatmap des villes":
    # print dataframe
    st.header("Data")
    st.write(df_city)
    st.write(df_geocity)

    # print graph
    st.header("Graphique")
    date_range = st.slider("Range de date voulu ?", value=(date_min, date_max))
    countplot(df_city, "city", date_range)
    bubblemap(df_geocity)
