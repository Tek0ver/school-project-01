import streamlit as st
import psycopg2
import pandas as pd
from toolbox import DatabaseInterface
import matplotlib.pyplot as plt
from datetime import datetime
import seaborn as sns

databaseInterface = DatabaseInterface()

@st.cache_data()
def load_data(query):
    return(databaseInterface.select(query))

def graph(data, date_range):
    fig, ax = plt.subplots(1,1)
    data = data[
        (data['article_date'] >= date_range[0])
        & (data['article_date'] <= date_range[1])]
    ax.hist(data['article_date'], bins='auto')

    st.pyplot(fig)

def graph2(data, date_range):
    # fig, ax = plt.
    pass

st.sidebar.header('Menu')
sidebar_menu_00 = st.sidebar.selectbox('Analyse', ('Couverture médiatique', 'Heatmap des villes'))

query = "SELECT * FROM articles;"
articles = load_data(query)


if sidebar_menu_00 == 'Couverture médiatique':

    st.header('Data')
    st.write(articles)

    st.header('Graphique')


    # TODO: Make sure that date goes at least to the first to the last article
    date_range = st.slider(
        "Range de date voulu ?",
        value=(datetime(2021, 1, 1), datetime(2023, 12, 31)))
    
    graph(articles, date_range)
