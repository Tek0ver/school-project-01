import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

@st.cache(allow_output_mutation=True)
def load_data() -> tuple[pd.DataFrame, pd.DataFrame]:
    data = pd.read_csv('../data/streamlit_01_data.csv')
    data = preprocess_dates(data)
    
    # Group and order by date
    data_grouped = data.groupby('date').size().to_frame("count").reset_index()
    data_grouped.sort_values('date')
    data_grouped['date'] = pd.to_datetime(data_grouped['date'])

    return data, data_grouped


def preprocess_dates(data: pd.DataFrame) -> pd.DataFrame:
    data = data.rename(columns={'date': 'full date'})
    data['date'] = pd.to_datetime(data['full date'])
    # Drop articles with no date
    data = data[data['date'].notna()]
    data['date'] = data['date'].map(lambda dt: dt.strftime('%Y-%m-%d'))
    
    return data

def graph(data, date_range):
    fig, ax = plt.subplots(1,1)
    data = data[
        (data['date'] >= date_range[0])
        & (data['date'] <= date_range[1])]
    plot = plt.bar(x='date', height='count', data=data)
    ax.plot()

    st.pyplot(fig)
    st.write(data)


data, data_grouped = load_data()

# Streamlit sidebar
st.sidebar.header("Répartition des articles sur le sujet de l'Ukraine dans le temps")
add_sidebar0 = st.sidebar.selectbox('Analyse', ('Couverture médiatique', 'Heatmap des villes'))
journaux = ['le monde', 'le canard', 'le figaro', 'sud ouest']
add_sidebar1 = st.sidebar.multiselect('Journal', journaux)
add_sidebar2 = st.sidebar.selectbox('Année', (2021, 2022, 2023))

# Couverture médiatique
if add_sidebar0 == 'Couverture médiatique':

    st.header('Couverture médiatique')
    
    st.write('Voici les données collectées :')
    
    lines = st.slider('Combien de lignes voulez vous voir ?', 1, 200, 5)
    
    st.write(data[['date', 'title']].head(lines))

    st.header('Graph')
    
    date_range = st.slider(
        "Range de date voulu ?",
        value=(datetime(2021, 1, 1), datetime(2023, 12, 31)))

    graph(data_grouped, date_range)
