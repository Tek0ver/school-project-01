import streamlit as st
from toolbox import DatabaseInterface
from datetime import datetime
import graphs


########################### load data and init streamlit ###########################


@st.cache_data(ttl=86400)
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


def date_slider():
    range_date = st.slider("Séléctionnez une plage de date :", value=(date_min, date_max))
    if range_date[0] == range_date[1]:
        st.warning("Veuillez séléctionner deux dates différentes.")
        st.stop()
    return range_date


st.session_state['session_count'] += 1
print(f"[LOG] New page generation ({st.session_state['session_count']})")

st.sidebar.header("Menu")
sidebar_menu_00 = st.sidebar.selectbox(
    "Analyse", ("Couverture médiatique", "Données géographiques", "Data")
)

if sidebar_menu_00 == "Couverture médiatique":

    st.title("COUVERTURE MÉDIATIQUE")
    st.write("Vous trouverez ici le graphique de la couverture médiatique sur l'Ukraine de mi 2021 à mi 2023 \
             en terme de nombre d'articles parus sur différents sites d'actualité français.")
    
    date_range = date_slider()
    journal_filter = st.multiselect(
        'Séléctionnez le ou les journaux :',
        ['Le Monde', 'Libération'],
        ['Le Monde', 'Libération'])

    # check for at least one journal selected
    if journal_filter:
        with st.spinner('Chargement'):
            graphs.graph(data_articles, date_range, journal_filter)
            st.write(" On peut constater qu'avec le début de la guerre, le nombre d'articles sur l'Ukraine a fortement augmenté.")
    else:
        st.warning("Sélectionnez au moins un journal dans la liste.")

elif sidebar_menu_00 == "Données géographiques":

    st.title("DONNÉES GÉOGRAPHIQUES")
    st.write("Vous trouverez ici les villes mentionnées dans les articles parus dans la plage \
             de date séléctionnée au travers de deux graphiques.")
    st.info("Dans cette version, seulement les articles de Le Monde sont utilisés.", icon="⚠️")

    date_range = date_slider()

    df_cities = data_cities_from_articles.copy()
    df_cities = df_cities[
        (df_cities['article_date'] >= date_range[0])
        & (df_cities['article_date'] <= date_range[1])]
    df_cities["city"] = df_cities["city"].str.capitalize()

    df_mapcity = (
        df_cities.groupby(["city", "population_2023", "latitude", "longitude"])
        .count()
        .sort_values("article_date", ascending=False)
        .reset_index()
    )
    df_mapcity = df_mapcity.rename(columns={"article_date": "count"})
    df_mapcity = df_mapcity.dropna()

    with st.spinner('Chargement'):
        # print graphs
        st.header("Cartes des villes mentionnées dans les articles")
        graphs.bubblemap(df_mapcity)
        st.write("")
        st.header("Nombre de mentions des villes dans les articles")
        graphs.countplot(df_cities, "city")

elif sidebar_menu_00 == "Data":
    st.title("Data")
    st.write("Vous pouvez voir ici un extrait des donneés utilisées pour générer les différentes visualisations sur ce site. \
             Ces données ont été récupérées par notre équipe à l'aide de scraping.")
    st.write("Quelques chiffres :")
    nb_articles = data_articles.shape[0]
    min_date = data_articles['article_date'].min()
    max_date = data_articles['article_date'].max()
    delta_date = max_date - min_date
    min_date = min_date.strftime('%d/%m/%Y')
    max_date = max_date.strftime('%d/%m/%Y')
    st.write(f"Il y a actuellement {nb_articles} articles provenants de Le Monde et de Libération \
             parus entre le {min_date} et le {max_date}, soit sur une période de {delta_date.days} jours.")
    st.header("Articles :")
    st.dataframe(data_articles[['journal', 'article_date', 'title']])
    st.header("Informations des villes :")
    st.dataframe(data_cities_from_articles)
