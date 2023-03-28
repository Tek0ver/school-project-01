import streamlit as st
from toolbox import DatabaseInterface
from datetime import datetime
import graphs


########################### load data and init streamlit ###########################


@st.cache_data()
def load_data():
    databaseInterface = DatabaseInterface()
    data_articles = databaseInterface.select("query_articles")
    data_cities_from_articles = databaseInterface.select("query_cities_from_articles")

    # date range
    date_min = min(data_articles["article_date"]).to_pydatetime()
    date_max = max(data_articles["article_date"]).to_pydatetime()
    print(f"[LOG] date min: {date_min}, date max: {date_max}")

    return data_articles, data_cities_from_articles, date_min, date_max

data_articles, data_cities_from_articles, date_min, date_max = load_data()

# Initialization
if 'session_count' not in st.session_state:
    print("[LOG] New streamlit session")
    st.session_state['session_count'] = 0


########################### streamlit page ###########################


st.session_state['session_count'] += 1
print(f"[LOG] New page generation ({st.session_state['session_count']})")

st.sidebar.header("Menu")
sidebar_menu_00 = st.sidebar.selectbox(
    "Analyse", ("Couverture médiatique", "Heatmap des villes", "Data")
)


if sidebar_menu_00 == "Couverture médiatique":

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


elif sidebar_menu_00 == "Data":
    st.header("Data")
    st.write(data_articles)
    st.write(data_cities_from_articles)
