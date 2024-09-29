import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import plotly.graph_objects as go

# CSS personnalisé pour réduire les marges
st.markdown("""
    <style>
    .block-container {
        padding-top: 1rem;
        padding-bottom: 1rem;
    }
    .element-container {
        margin-bottom: 0.5rem; /* Réduit l'espacement entre les éléments */
    }
    </style>
    """, unsafe_allow_html=True)

# Fonction qui ajuste la couleur de la valeur en fonction de son intervalle
def get_value_color(value):
    if value < 20:
        return 'red'
    elif 20 <= value < 40:
        return 'orange'
    elif 40 <= value < 60:
        return 'yellow'
    elif 60 <= value < 80:
        return 'lightgreen'
    else:
        return 'green'

def show():
    st.title("Index de Performance")

        # Charger le fichier Excel avec le chemin correct
    file_path = "data/Performance_Index.xlsx"  # Ajustez le chemin si nécessaire
    try:
        df = pd.read_excel(file_path)
    except FileNotFoundError:
        st.error(f"Le fichier {file_path} n'a pas été trouvé.")
        return
    
    # Affichage des filtres côte à côte pour compacter
    col1, col2 = st.columns(2)

    # Filtre par Ligue (dans col1)
    with col1:
        ligues = df['League'].unique().tolist()
        ligue_selectionnee = st.selectbox("Sélectionner une ligue", ["Toutes"] + ligues)

    # Filtre par Équipe (dans col2)
    with col2:
        equipes = df['Équipe'].unique().tolist()
        equipe_selectionnee = st.selectbox("Sélectionner une équipe", ["Toutes"] + equipes)

    # Appliquer les filtres
    if ligue_selectionnee != "Toutes":
        df = df[df['League'] == ligue_selectionnee]
    if equipe_selectionnee != "Toutes":
        df = df[df['Équipe'] == equipe_selectionnee]

    # Filtre par Âge et Valeur marchande côte à côte
    col3, col4 = st.columns(2)
    with col3:
        # Filtre par Âge
        age_min, age_max = int(df['Âge'].min()), int(df['Âge'].max())
        age_selectionne = st.slider("Sélectionner une tranche d'âge", age_min, age_max, (age_min, age_max))
        df = df[(df['Âge'] >= age_selectionne[0]) & (df['Âge'] <= age_selectionne[1])]
    
    with col4:
        # Filtre par Valeur Marchande
        valeur_min, valeur_max = df['Valeur Marchande'].min(), df['Valeur Marchande'].max()
        valeur_selectionnee = st.slider("Sélectionner une tranche de valeur marchande", int(valeur_min), int(valeur_max), (int(valeur_min), int(valeur_max)))
        df = df[(df['Valeur Marchande'] >= valeur_selectionnee[0]) & (df['Valeur Marchande'] <= valeur_selectionnee[1])]

    # Sélectionner un joueur parmi les joueurs filtrés
    joueurs = df['Joueur'].unique()
    joueur_selectionne = st.selectbox("Sélectionner un joueur", joueurs)

    # Filtrer le DataFrame pour obtenir les infos du joueur sélectionné
    joueur_info = df[df['Joueur'] == joueur_selectionne].iloc[0]

    # Afficher les informations du joueur
    st.write(f"**Nom :** {joueur_info['Joueur']}")
    st.write(f"**Équipe :** {joueur_info['Équipe']}")
    st.write(f"**Âge :** {int(joueur_info['Âge'])} ans")
    st.write(f"**League :** {joueur_info['League']}")
    st.write(f"**Minutes jouées :** {joueur_info['Minutes']}")
    st.write(f"**Poste :** {joueur_info['Poste']}")
    st.write(f"**Meilleur poste :** {joueur_info['Meilleur Poste']}")

    # Colonnes de performance
    performance_columns = ['Défenseur Stoppeur', 'Défenseur Relanceur', 'Arrière Latéral', 'Latéral Offensif', 
                        'Milieu Sentinelle', 'Milieu Récupérateur', 'Milieu Box-to-Box', 'Milieu Relayeur',
                        'Meneur de Jeu', 'Meneur de Jeu Excentré', 'Ailier Défensif', 'Ailier Intérieur', 
                        'Ailier de Débordement', 'Attaquant Pivot', 'Attaquant de Pressing', 'Renard des Surfaces', 
                        'Attaquant Complet']

    # Récupérer les performances du joueur et trier par ordre décroissant
    performances = joueur_info[performance_columns]
    sorted_performances = performances.dropna().sort_values(ascending=False)

    # Afficher les jauges de manière compacte en utilisant des colonnes avec largeur ajustée
    num_cols = 3  # Nombre de jauges par ligne
    cols = st.columns([1, 1, 1])  # Ajustement de la largeur des colonnes, ici égales

    for i, (role, value) in enumerate(sorted_performances.items()):
        col = cols[i % num_cols]  # Place les jauges côte à côte dans des colonnes avec la largeur ajustée
        with col:
            value_color = get_value_color(value)
            fig = go.Figure(go.Indicator(
                mode="gauge+number",
                value=value,
                number={'font': {'color': value_color}},
                title={'text': role, 'font': {'size': 10}},  # Réduire la taille du texte du rôle
                gauge={
                    'axis': {'range': [0, 100]},
                    'bar': {'color': 'blue'},
                    'steps': [
                        {'range': [0, 20], 'color': 'red'},
                        {'range': [20, 40], 'color': 'orange'},
                        {'range': [40, 60], 'color': 'yellow'},
                        {'range': [60, 80], 'color': 'lightgreen'},
                        {'range': [80, 100], 'color': 'green'}],
                }))
            # Réduire la hauteur de chaque jauge
            fig.update_layout(margin=dict(l=20, r=20, t=30, b=20), height=200)

            st.plotly_chart(fig, use_container_width=True)
