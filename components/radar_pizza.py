import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from mplsoccer import PyPizza
from scipy import stats

# Fonction pour convertir l'abbreviation en nom complet des caractéristiques
def carac_abbreviation_to_real_name(carac):
    carac_dict = dict()
    # Vous pouvez adapter ce chemin pour votre projet
    with open('data/Radar_Pizza/carac_names.csv', newline='') as f:
        for line in f:
            line = line.strip('\n')
            (key, val) = line.split(",")
            carac_dict[key] = val
    return carac_dict[carac]

# Fonction pour générer les centiles
def calculate_percentiles(df, player_filter, carac_list):
    values_list = []
    player_of_i = df[player_filter]
    for i in carac_list:
        df = df.fillna('')
        carac1 = list(df[i])
        carac_player = list(player_of_i[i])
        centile = stats.percentileofscore(carac1, carac_player)
        if i in ['Fautes par 90']:
            centile = np.abs(centile - 100)
        values_list.append(int(centile))
    return values_list

# Charger le CSV
# @st.cache
def load_data(file_path):
    return pd.read_csv(file_path)

def show():
    # Charger les données des joueurs
    df = load_data("data/Radar_Pizza/Monde.csv")

    # Interface utilisateur pour filtrer par ligue et joueur
    st.title("Radar Pizza - Analyse des joueurs")

    # Utiliser les colonnes pour compacter les inputs
    col1, col2, col3 = st.columns(3)

    # Entrée du nombre minimum de minutes jouées dans la première colonne
    with col1:
        min_minutes, max_minutes = int(df['Minutes jouées  '].min()), int(df['Minutes jouées  '].max())
        minutes_selectionnees = st.number_input("Minutes min.", min_value=min_minutes, max_value=max_minutes, value=min_minutes)

    # Filtrer les joueurs en fonction des minutes jouées
    df = df[df['Minutes jouées  '] >= minutes_selectionnees]

    # Sélection de la ligue dans la deuxième colonne
    with col2:
        top_5_ligues = ['Angleterre D1', 'Allemagne D1', 'Italie D1', 'France D1', 'Espagne D1']
        ligues = df['Team'].unique().tolist()
        ligue_options = ["Toutes", "Top 5 européen"] + ligues
        ligue_selectionnee = st.selectbox("Championnat", ligue_options)

    # Sélection de l'équipe dans la troisième colonne
    with col3:
        if ligue_selectionnee == "Top 5 européen":
            equipes = df[df['Team'].isin(top_5_ligues)]['Équipe dans la période sélectionnée'].unique().tolist()
        elif ligue_selectionnee != "Toutes":
            equipes = df[df['Team'] == ligue_selectionnee]['Équipe dans la période sélectionnée'].unique().tolist()
        else:
            equipes = df['Équipe dans la période sélectionnée'].unique().tolist()

        equipes = sorted(equipes)
        equipe_selectionnee = st.selectbox("Équipe", ["Toutes"] + equipes)

    # Filtrer uniquement la liste des joueurs selon la ligue et l'équipe sélectionnées (sans modifier le DataFrame)
    if ligue_selectionnee == "Top 5 européen" and equipe_selectionnee == "Toutes":
        joueurs = df[df['Team'].isin(top_5_ligues)]['Joueur'].unique().tolist()
        joueurs_echantillon = df[df['Team'].isin(top_5_ligues)]
    elif ligue_selectionnee == "Top 5 européen" and equipe_selectionnee != "Toutes":
        joueurs = df[(df['Team'].isin(top_5_ligues)) & (df['Équipe dans la période sélectionnée'] == equipe_selectionnee)]['Joueur'].unique().tolist()
        joueurs_echantillon = df[(df['Team'].isin(top_5_ligues))]
    elif ligue_selectionnee != "Toutes" and equipe_selectionnee == "Toutes":
        joueurs = df[df['Team'] == ligue_selectionnee]['Joueur'].unique().tolist()
        joueurs_echantillon = df[df['Team'] == ligue_selectionnee]
    elif ligue_selectionnee != "Toutes" and equipe_selectionnee != "Toutes":
        joueurs = df[(df['Team'] == ligue_selectionnee) & (df['Équipe dans la période sélectionnée'] == equipe_selectionnee)]['Joueur'].unique().tolist()
        joueurs_echantillon = df[(df['Team'] == ligue_selectionnee)]
    elif equipe_selectionnee != "Toutes":
        joueurs = df[df['Équipe dans la période sélectionnée'] == equipe_selectionnee]['Joueur'].unique().tolist()
        joueurs_echantillon = df
    else:
        joueurs = df['Joueur'].unique().tolist()
        joueurs_echantillon = df

    # Sélectionner un joueur
    joueurs = sorted(joueurs)
    joueur_selectionne = st.selectbox("Sélectionner un joueur", joueurs)

    # Filtrer les données pour le joueur sélectionné
    player_filter = (df['Joueur'] == joueur_selectionne)
    player_of_i = df[player_filter]
    
    # Lire la colonne Place et extraire le premier poste
    place = player_of_i['Place'].values[0]
    premier_poste = place.split(",")[0].strip()  # Séparer par virgule et prendre le premier élément

    # Filtrer l'échantillon de joueurs en fonction du premier poste
    joueurs_echantillon['Premier poste'] = joueurs_echantillon['Place'].apply(lambda x: x.split(",")[0].strip())

    if premier_poste in ["CF"]:
        postes_to_compare = 'Buteurs'
        joueurs_echantillon = joueurs_echantillon[joueurs_echantillon['Premier poste'] == 'CF']
    elif premier_poste in ["LW", "LWF", "LAMF", "RW", "RWF", "RAMF"]:
        postes_to_compare = 'Ailiers'
        joueurs_echantillon = joueurs_echantillon[joueurs_echantillon['Premier poste'].isin(['LW', 'LWF', 'LAMF', 'RW', 'RWF', 'RAMF'])]
    elif premier_poste in ["AMF", "LCMF", "RCMF"]:
        postes_to_compare = 'Milieux offensifs'
        joueurs_echantillon = joueurs_echantillon[joueurs_echantillon['Premier poste'].isin(['AMF', 'LCMF', 'RCMF'])]
    elif premier_poste in ["DMF", "LDMF", "RDMF", "LCMF", "RCMF"]:
        postes_to_compare = 'Milieux centraux'
        joueurs_echantillon = joueurs_echantillon[joueurs_echantillon['Premier poste'].isin(['DMF', 'LDMF', 'RDMF', 'LCMF', 'RCMF'])]
    elif premier_poste in ["LWB", "LB", "RWB", "RB"]:
        postes_to_compare = 'Latéraux'
        joueurs_echantillon = joueurs_echantillon[joueurs_echantillon['Premier poste'].isin(['LWB', 'LB', 'RWB', 'RB'])]
    elif premier_poste in ["CB", "LCB", "RCB"]:  
        postes_to_compare = 'Défenseurs centraux'  
        joueurs_echantillon = joueurs_echantillon[joueurs_echantillon['Premier poste'].isin(['CB', 'LCB', 'RCB'])]

    # Liste des caractéristiques à afficher dans le radar pizza
    carac_list = ["xA par 90",
                'Courses progressives par 90', 'Passes progressives par 90', 'Passes longues par 90', 
                'Passes dans tiers adverse par 90', "Tacles glissés PAdj", "Interceptions PAdj"]

    # Calcul des centiles pour chaque caractéristique
    values_list = calculate_percentiles(joueurs_echantillon, player_filter, carac_list)

    # Générer les couleurs des tranches et du texte en fonction des valeurs
    slice_colors = []
    text_colors = []
    for i in values_list:
        if i < 25:
            color = "#FE0101"
        elif 25 <= i < 50:
            color = "#FF760D"
        elif 50 <= i < 75:
            color = "#D7DF01"
        else:
            color = "#00CA09"
        slice_colors.append(color)
        text_colors.append("#000000")

    # Convertir les abréviations en noms complets des caractéristiques
    carac_names = []
    for i in carac_list:
        carac_new = carac_abbreviation_to_real_name(i)
        if len(carac_new.split(" ")) >= 3:
            carac_new = (" ").join(carac_new.split(" ")[:2]) + "\n" + (" ").join(carac_new.split(" ")[2:])
        carac_names.append(carac_new[:-1])

    # Générer le radar pizza
    baker = PyPizza(
        params=carac_names,  # liste des paramètres
        background_color="#161d23",  # couleur de fond
        straight_line_color="#000000",  # couleur des lignes droites
        straight_line_lw=1,  # largeur des lignes droites
        last_circle_color="#000000",  # couleur du dernier cercle
        last_circle_lw=1,  # largeur du dernier cercle
        other_circle_lw=0,  # largeur des autres cercles
        inner_circle_size=10  # taille du cercle intérieur
    )

    # Créer la figure du radar pizza
    fig, ax = baker.make_pizza(
        values_list,  # liste des valeurs
        figsize=(10, 12),  # taille de la figure
        param_location=112,  # ajuster l'emplacement des paramètres
        color_blank_space="same",  # utiliser la même couleur pour l'espace vide
        slice_colors=slice_colors,  # couleur des tranches individuelles
        value_colors=text_colors,  # couleur du texte des valeurs
        value_bck_colors=slice_colors,  # couleur de fond des valeurs
        blank_alpha=0.4,  # transparence des espaces vides
        kwargs_slices=dict(
            edgecolor="#000000", zorder=2, linewidth=1
        ),  # paramètres pour les tranches
        kwargs_params=dict(
            color="#FFFFFF", fontsize=18,  # paramètres pour les noms des paramètres
            va="center"
        ),
        kwargs_values=dict(
            color="#000000", fontsize=24,  # paramètres pour les valeurs
            zorder=3,
            bbox=dict(
                edgecolor="#000000", facecolor="cornflowerblue",
                boxstyle="round,pad=0.2", lw=1
            )
        )
    )

    # Afficher la figure dans Streamlit
    st.pyplot(fig)

    # Afficher la légende sous le graphique
    st.markdown(f"**Référentiel de comparaison :** {postes_to_compare} - {ligue_selectionnee if ligue_selectionnee != 'Toutes' else 'Toutes les ligues'}")
    st.markdown(f"**Nombre de joueurs dans l'échantillon :** {len(joueurs_echantillon)}")
    st.markdown(f"**Nombre minimum de minutes jouées :** {minutes_selectionnees} minutes")