import math
import warnings

from PIL import Image
import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt

from scipy import stats

import streamlit as st
from functions.functions_distribution import load_data, get_carac_list, get_players_final, carac_abbreviation_to_real_name
from functions.functions_radar_pizza import filter_inputs, filter_players, filter_by_position
import io

def show():
    carac_list = []
    
    # Interface utilisateur pour filtrer par ligue et joueur
    st.title("Distribution - Analyse des joueurs")

    langue = 'Français'

    df = load_data("data/Monde_2024.csv")
    top_5_ligues = ['Angleterre D1', 'Allemagne D1', 'Italie D1', 'France D1', 'Espagne D1']

    # Gestion des filtres pour ligue, équipe, minutes et joueurs
    df, ligue_selectionnee, equipe_selectionnee = filter_inputs(df, top_5_ligues)

    joueurs, joueurs_echantillon = filter_players(df, ligue_selectionnee, equipe_selectionnee, top_5_ligues)
    joueur_selectionne = st.selectbox("Sélectionner un joueur", joueurs)

    # Filtrer les données pour le joueur sélectionné
    player_filter = (df['Joueur'] == joueur_selectionne)
    player_of_i = df[player_filter]
    
    # Lire la colonne Place et extraire le premier poste
    place = player_of_i['Place'].values[0]
    premier_poste = place.split(",")[0].strip()  # Séparer par virgule et prendre le premier élément

    # Filtrer l'échantillon de joueurs en fonction du premier poste
    joueurs_echantillon, postes_to_compare = filter_by_position(joueurs_echantillon, premier_poste)

    # Ajout d'une case à cocher pour savoir si l'on veut utiliser un poste spécifique
    poste_specifique = st.checkbox("Utiliser le poste 'Spécifique'")

    # Si la case est cochée, proposer des options spécifiques
    if poste_specifique:
        graph = st.selectbox("Choisir un type de graph Spécifique", ['Défensif', 'Duels', 'Projection', 'Finition', 'Construction', 'Création', 'Passes Adj'])
        poste = 'Spécifique'
    else:
        # Sinon, proposer les options classiques pour le graph
        graph = st.selectbox("Choisir le type de graph", ['Complet', 'Allégé'])

        # Attribution du poste selon le poste du joueur
        if postes_to_compare == 'Buteurs':
            poste = 'Buteur'
        elif postes_to_compare == 'Milieux offensifs':
            poste = 'Milieu Offensif'
        elif postes_to_compare == 'Ailiers':
            poste = 'Ailier'
        elif postes_to_compare == 'Milieux centraux':
            poste = 'Milieu Central'
        elif postes_to_compare == 'Milieux défensifs':
            poste = 'Milieu Défensif'
        elif postes_to_compare == 'Latéraux':
            poste = 'Latéral'
        elif postes_to_compare == 'Défenseurs centraux':
            poste = 'Défenseur Central'
        else:
            poste = 'Spécifique'

    carac_list = get_carac_list(poste, graph)

    players_final = get_players_final(joueurs_echantillon)

    # METTRE LE NOM DU JOUEUR ANALYSE
    player = players_final[players_final['Joueur'] == joueur_selectionne]

    f, axes = plt.subplots(math.ceil(len(carac_list) / 3), 3, figsize=(10, 10))

    if len(carac_list) % 3 == 2:
        f.delaxes(axes[int(len(carac_list) / 3), 2])
    if len(carac_list) % 3 == 1:
        f.delaxes(axes[int(len(carac_list) / 3), 2])
        f.delaxes(axes[int(len(carac_list) / 3), 1])

    number = 0
    for i in carac_list:

        value = player[i].values[0]

        pct = stats.percentileofscore(players_final[i], value)

        if pct >= 90:
            col = "darkgreen"
        if 70 <= pct < 90:
            col = "yellowgreen"
        if 50 <= pct < 70:
            col = "gold"
        if 30 <= pct < 50:
            col = "orange"
        if 0 <= pct < 30:
            col = "red"

        # Plot the distribution
        ax = sns.histplot(players_final[i], color=col, fill=col, bins=30, kde=False, ax=axes[int(number / 3), number % 3])

        # Add a vertical line for the player's value
        ax.axvline(value, 0, 0.95, lw=1, color="white", linestyle="--")

        # Determine the y-position for the label
        y_position = ax.get_ylim()[1]  # Place label slightly below the top of the graph

        # Add the "Top X%" label at the top of the player's bar
        ax.text(value, y_position, f"{value:.2f}", color="white", ha='center', va='bottom', fontsize=10, fontname='Roboto')

        # Set the title and other graph customizations
        carac_name = carac_abbreviation_to_real_name(i, langue)
        ax.set_title(f"{carac_name.upper()}\n", color="#FFFFFF", fontname='Roboto')
        ax.spines['bottom'].set_color('#FFFFFF')
        ax.tick_params(axis='x', colors='#FFFFFF')
        ax.tick_params(axis='y', colors='#FFFFFF')
        ax.set_facecolor('#161d23')

        # Clean up the graph
        ax.set(xlabel=None)
        ax.set(ylabel=None)
        ax.set(yticks=[])

        number += 1

    # Finish the graphs
    sns.despine(left=True)
    plt.subplots_adjust(hspace=1)
    plt.style.use("default")

    fig = plt.gcf()

    fig.patch.set_facecolor('#161d23')

    fig.set_size_inches(10, 11)  # length, height

    # Afficher le graphique dans Streamlit
    st.pyplot(fig)

    buffer = io.BytesIO()
    fig.savefig(buffer, format='png', bbox_inches="tight")
    buffer.seek(0)

    st.download_button(
        label="Télécharger le chart en PNG",
        data=buffer,
        file_name=f"distribution_{player_of_i['Joueur'].values[0]}.png",
        mime="image/png"
    )