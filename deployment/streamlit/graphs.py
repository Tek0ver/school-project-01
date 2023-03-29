import streamlit as st
import pandas as pd
from toolbox import DatabaseInterface
import matplotlib.pyplot as plt
from datetime import datetime
import seaborn as sns
import plotly.express as px

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

def graph(data, date_range):
    date_start_war = datetime(year=2022, month=2, day=24)
    fig, ax = plt.subplots(1, 1)
    data = data[
        (data["article_date"] >= date_range[0])
        & (data["article_date"] <= date_range[1])
    ]
    ax.hist(data["article_date"], bins="auto")
    ax.tick_params(axis='x', rotation=30)
    if date_range[0] < date_start_war and date_start_war < date_range[1]:
        ax.axvline(x=date_start_war, color="red", linestyle="dashed")
        min_ylim, max_ylim = plt.ylim()
        ax.text(x=date_start_war, y=max_ylim*0.9, s=" Invasion de l'Ukraine par la Russie", color="red")

    st.pyplot(fig)
