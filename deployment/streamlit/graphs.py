import streamlit as st
import pandas as pd
from toolbox import DatabaseInterface
import matplotlib.pyplot as plt
from datetime import datetime
import seaborn as sns
import plotly.express as px


def countplot(df: pd.DataFrame, feature: str):
    fig = plt.figure()
    print(df.shape)
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
        hover_data=['latitude', 'longitude', 'count', 'population_2023'],
        zoom=4,
        center={"lat": 50, "lon": 30},
        mapbox_style="carto-positron",
        height=700,
        size_max=40,
    )

    st.plotly_chart(fig)

def graph(data, date_range, journals=['Le Monde', 'Libération']):

    date_start_war = datetime(year=2022, month=2, day=24)

    convert_labels = {
        'Le Monde': 'le monde',
        'Libération': 'liberation',
        'le monde': 'Le Monde',
        'liberation': 'Libération'
    }
    journal_filter = [convert_labels[journal] for journal in journals]

    data = data[
        (data["article_date"] >= date_range[0])
        & (data["article_date"] <= date_range[1])
        & (data["journal"].isin(journal_filter))
    ]

    ax = sns.displot(data, x='article_date', hue='journal', kde=True,
                     edgecolor='white')
    ax.tick_params(axis='x', rotation=40)

    sns.move_legend(
        ax, "lower center",
        bbox_to_anchor=(.5, 1), ncol=3, title=None, frameon=False,
    )

    ax.set(xlabel='', ylabel='Nombre d\'articles parus')

    for i, label in enumerate(ax._legend.texts):
        label.set_text(convert_labels[label.get_text()])

    if date_range[0] < date_start_war and date_start_war < date_range[1]:
        plt.axvline(x=date_start_war, color="red", linestyle="dashed")
        min_ylim, max_ylim = plt.ylim()
        plt.text(x=plt.xlim()[0],
                 y=max_ylim*0.9,
                 s=" Invasion de l'Ukraine par la Russie",
                 color="red",
                 in_layout=False)

    st.pyplot(ax)
