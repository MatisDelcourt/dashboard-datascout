import streamlit as st
import pandas as pd
from functions.functions_radar_compa import double_graph, prepare_carac

def show():
    # Charger les données des joueurs
    df = pd.read_csv('data/Monde.csv')

    df = prepare_carac(df)

    # Interface utilisateur pour sélectionner deux joueurs
    st.title("Radar Comparaison - Analyse des joueurs")

    col1, col2 = st.columns(2)

    # Sélection du joueur 1 et sa couleur
    with col1:
        joueur_1 = st.selectbox("Sélectionner le joueur 1", df['Joueur'].unique(), key="joueur_1")
        joueur_2 = st.selectbox("Sélectionner le joueur 2", df['Joueur'].unique(), key="joueur_2")

    # Sélection du joueur 2 et sa couleur
    with col2:
        couleur_joueur_1 = st.color_picker("Couleur du joueur 1", "#0000FF")  # Couleur bleue par défaut
        couleur_joueur_2 = st.color_picker("Couleur du joueur 2", "#FF0000")  # Couleur rouge par défaut


    # Nombre minimum de minutes jouées
    minimum_minutes = st.slider("Minutes minimum", min_value=0, max_value=2000, value=200)

    # Template "Danger" : Statistiques utilisées pour la comparaison
    template_danger = ['Actions décisives', 'Buts par 90', 'xG par 90', 'Passes décisives par 90', 
                       'xA par 90', 'Passes décisives avec tir par 90', '23Ast', 'Passes quasi décisives par 90', 
                       'Centres réussis', 'Tirs par 90', 'Tirs à la cible. %', 'Taux de conversion but/tir']

    # Générer et afficher le radar
    fig = double_graph(
                df=df,
                name_1=joueur_1,
                name_2=joueur_2,
                carac=template_danger,
                championnat="Ligue 1",  # Exemple de championnat
                minimum_minutes=minimum_minutes,
                couleur_dominante_1=couleur_joueur_1,
                couleur_dominante_2=couleur_joueur_2,
                mode="danger",
                black_version=False
            )
        
    # Afficher la figure
    st.pyplot(fig)