import streamlit as st
import pandas as pd
from toolbox import DatabaseInterface
import matplotlib.pyplot as plt
from datetime import datetime
import seaborn as sns
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


def countplot(df: pd.DataFrame, feature: str):
    fig = plt.figure()
    chart = sns.countplot(df, x=feature, order=df[feature].value_counts().index)
    chart.set_xticklabels(
        chart.get_xticklabels(), rotation=60, horizontalalignment="right"
    )
    sns.set(rc={"figure.figsize": (10, 5)})

    st.pyplot(fig)


def bubblemap(df: pd.DataFrame):
    """Data with latitude/longitude and values"""
    fig = px.scatter_mapbox(
        df,
        lat="latitude",
        lon="longitude",
        size="count",
        color="count",
        color_continuous_scale=px.colors.sequential.Plasma,
        hover_name="city",
        zoom=4,
        center={"lat": 50, "lon": 30},
        mapbox_style="carto-positron",
        height=700,
        size_max=40
    )

    st.plotly_chart(fig)



################################################# def variables #################################################

# articles
query = """
    SELECT * FROM articles
    WHERE article_date > '2022-01-01'
    ;
"""
articles = load_data(query)


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

    # print graph
    st.header("Graphique")
    date_range = st.slider("Range de date voulu ?", value=(date_min, date_max))

    ########################### update data ##############################

    # cities
    query_city = f"""
        SELECT article_date, content_cities.city, latitude, longitude
        FROM articles
        JOIN contents ON articles.id = contents.article_id
        JOIN content_cities ON contents.id = content_cities.content_id
        JOIN geocity ON content_cities.city = geocity.city
        WHERE '{date_range[0]}' < article_date AND article_date < '{date_range[1]}'
        ORDER BY article_date
        ;
    """
    df_city = load_data(query_city)
    df_city["city"] = df_city["city"].str.capitalize()

    df_mapcity = (
        df_city.groupby(["city", "latitude", "longitude"])
        .count()
        .sort_values("article_date", ascending=False)
        .reset_index()
    )
    df_mapcity = df_mapcity.rename(columns={"article_date": "count"})
    df_mapcity = df_mapcity.dropna()

    ##########################################################

    bubblemap(df_mapcity)
    countplot(df_city, "city")
    st.write(df_mapcity)
    st.write(df_city)
