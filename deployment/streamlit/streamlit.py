import streamlit as st
import pandas as pd
from toolbox import DatabaseInterface
import matplotlib.pyplot as plt
from datetime import datetime
import seaborn as sns
import plotly.express as px
import graphs


########################### load data ###########################


databaseInterface = DatabaseInterface()

@st.cache_data()
def load_data():
    data_articles = databaseInterface.select("query_articles")
    data_cities_from_articles = databaseInterface.select("query_cities_from_articles")

    data_articles = data_articles[data_articles['article_date'] >= "2021-06-01"]
    data_cities_from_articles = data_cities_from_articles[data_cities_from_articles['article_date'] >= "2021-06-01"]
    # date range
    print(type(min(data_articles["article_date"])))
    date_min = min(data_articles["article_date"]).to_pydatetime()
    date_max = max(data_articles["article_date"]).to_pydatetime()

    return data_articles, data_cities_from_articles, date_min, date_max

data_articles, data_cities_from_articles, date_min, date_max = load_data()

########################### streamlit page ###########################


st.sidebar.header("Menu")
sidebar_menu_00 = st.sidebar.selectbox(
    "Analyse", ("Couverture médiatique", "Heatmap des villes")
)


if sidebar_menu_00 == "Couverture médiatique":

    # TODO: Make sure that date goes at least to the first to the last article
    date_range = st.slider("Range de date voulu ?", value=(date_min, date_max))

    st.header("Graphique")

    graphs.graph(data_articles, date_range)


elif sidebar_menu_00 == "Heatmap des villes":
    date_range = st.slider("Range de date voulu ?", value=(date_min, date_max))

    df_cities = data_cities_from_articles.copy()
    df_cities = df_cities[
        (df_cities['article_date'] >= date_range[0])
        & (df_cities['article_date'] <= date_range[1])]
    df_cities["city"] = df_cities["city"].str.capitalize()

    df_mapcity = (
        df_cities.groupby(["city", "latitude", "longitude"])
        .count()
        .sort_values("article_date", ascending=False)
        .reset_index()
    )
    df_mapcity = df_mapcity.rename(columns={"article_date": "count"})
    df_mapcity = df_mapcity.dropna()

    # print graph
    st.header("Graphique")
    graphs.bubblemap(df_mapcity)
    graphs.countplot(df_cities, "city")
    # print dataframe
    st.header("Data")
    st.write(df_mapcity)
    st.write(df_cities)
