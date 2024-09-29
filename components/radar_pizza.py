import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from mplsoccer import PyPizza
from scipy import stats
import io 

def prepare_carac(df):
    # Défense
    df["Cartons reçus"] = df["Cartons jaunes par 90"] + df["Cartons rouges par 90"]

    # Calcul de la longueur
    df["Passes réussies"] = round(df["Passes par 90"] * df["Passes précises, %"] / 100, 2)
    df["Passes vers l'avant réussies"] = round(df["Passes avant par 90"] * df["Passes en avant précises, %"] / 100, 2)
    df["Passes arrière réussies"] = round(df["Passes arrière par 90"] * df["Passes arrière précises, %"] / 100, 2)
    df["Passes latérales réussies"] = round(df["Passes latérales par 90"] * df["Passes latérales précises, %"] / 100, 2)
    df["Passes longues réussies"] = round(df["Passes longues par 90"] * df["Longues passes précises, %"] / 100, 2)
    df["Passes dernier tiers réussies"] = round(df["Passes dans tiers adverse par 90"] * df["Passes dans tiers adverse précises, %"] / 100, 2)
    df["Passes vers la surface réussies"] = round(df["Passes vers la surface de réparation par 90"] * df["Passes vers la surface de réparation précises, %"] / 100, 2)
    df["Passes progressives réussies"] = round(df["Passes progressives par 90"] * df["Passes progressives précises, %"] / 100, 2)

    # Calcul des duels
    df["Duels gagnés"] = df["Duels par 90"] * df["Duels gagnés, %"] / 100
    df["Duels offensifs gagnés"] = df["Duels offensifs par 90"] * df["Duels de marquage, %"] / 100
    df["Duels défensifs gagnés"] = df["Duels défensifs par 90"] * df["Duels défensifs gagnés, %"] / 100
    df["Duels aériens gagnés"] = df["Duels aériens par 90"] * df["Duels aériens gagnés, %"] / 100

    # Dribbles et centres
    df["Dribbles réussis"] = df["Dribbles par 90"] * df["Dribbles réussis, %"] / 100
    df["Centres réussis"] = df["Centres par 90"] * df["Сentres précises, %"] / 100

    # Passes décisives et calcul de G-xG
    df["23Ast"] = df["Secondes passes décisives par 90"] + df["Troisièmes passes décisives par 90"]
    df["G-xG"] = df["Buts par 90"] - df["xG par 90"]

    # Passes dangereuses et terrain gagné
    df["Passes dangereuses"] = df["Passes quasi décisives par 90"] + df["Passes judicieuses par 90"]
    df["Terrain gagné"] = df["Passes progressives par 90"] + df["Courses progressives par 90"]
    df["Passes derniers tiers"] = df["Passes dans tiers adverse par 90"] + df["Réalisations en profondeur par 90"]
    df["Passes risquées"] = df["Passes pénétrantes par 90"] + df["Passes vers la surface de réparation par 90"]
        
    # Proportions de passes
    df["Proportion passes avant"] = df["Passes avant par 90"] / df["Passes par 90"]
    df["Proportion passes latérales"] = df["Passes latérales par 90"] / df["Passes par 90"]
    df["Proportion passes arrières"] = df["Passes arrière par 90"] / df["Passes par 90"]
    df["Proportion passes risquées"] = df["Passes risquées"] / df["Passes par 90"]
    df["Proportion passes derniers tiers"] = df["Passes derniers tiers"] / df["Passes par 90"]
    df["Proportion passes longues"] = df["Passes longues par 90"] / df["Passes par 90"]
    df["Proportion passes dangereuses"] = df["Passes dangereuses"] / df["Passes par 90"]
    df["Proportion passes vers la surface de réparation"] = df["Passes vers la surface de réparation par 90"] / df["Passes par 90"]

    # Actions décisives et passes
    df["Actions décisives"] = df["Buts par 90"] + df["Passes décisives par 90"]
    df["Actions décisives attendues"] = df["xG par 90"] + df["xA par 90"]

    df.columns = df.columns.str.replace(",", ".", regex=False)

    return df

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

# Fonction pour générer la liste des équipes en fonction de la ligue sélectionnée
def get_teams(df, ligue_selectionnee, top_5_ligues):
    if ligue_selectionnee == "Top 5 européen":
        # equipes = df[df['Team'].isin(top_5_ligues)]['Équipe dans la période sélectionnée'].unique().tolist()
        equipes = df.loc[df['Team'].isin(top_5_ligues), 'Équipe dans la période sélectionnée'].unique().tolist()

    elif ligue_selectionnee != "Toutes":
        equipes = df[df['Team'] == ligue_selectionnee]['Équipe dans la période sélectionnée'].unique().tolist()
    else:
        equipes = df['Équipe dans la période sélectionnée'].unique().tolist()
    return sorted(equipes)

# Fonction pour filtrer les joueurs selon la ligue et l'équipe sélectionnée
def filter_players(df, ligue_selectionnee, equipe_selectionnee, top_5_ligues):
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
    return sorted(joueurs), joueurs_echantillon

# Fonction pour filtrer l'échantillon de joueurs par poste
def filter_by_position(joueurs_echantillon, premier_poste):
    # joueurs_echantillon['Premier poste'] = joueurs_echantillon['Place'].apply(lambda x: x.split(",")[0].strip())
    joueurs_echantillon.loc[:, 'Premier poste'] = joueurs_echantillon['Place'].apply(lambda x: x.split(",")[0].strip())
    
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
    
    return joueurs_echantillon, postes_to_compare

# Fonction pour générer le radar pizza
def generate_pizza_chart(values_list, carac_names, slice_colors, text_colors):
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
            color="#FFFFFF", fontsize=17,  # paramètres pour les noms des paramètres
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
    return fig

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
        equipes = get_teams(df, ligue_selectionnee, top_5_ligues)
        equipe_selectionnee = st.selectbox("Équipe", ["Toutes"] + equipes)

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

    # Liste des caractéristiques à afficher dans le radar pizza
    # Définir les templates
    templates = {
        'Danger': ["Actions décisives", "Actions décisives attendues", 
                   "xG par 90", "Buts par 90", "xA par 90", "Passes décisives par 90",
                   "Passes décisives avec tir par 90", "23Ast",
                   "Centres réussis", "Сentres précises. %",
                   "Tirs par 90", "Tirs à la cible. %", "Taux de conversion but/tir"],
        'Projection': ["Attaques réussies par 90", 'Courses progressives par 90', 'Accélérations par 90',
                       'Dribbles réussis', "Dribbles réussis. %", 'Duels offensifs par 90',
                       "Duels de marquage. %", 'Fautes subies par 90', 'Touches de balle dans la surface de réparation sur 90'],
        'Défense': ["Actions défensives réussies par 90", "Duels défensifs gagnés", "Duels défensifs gagnés. %",
                    "Duels aériens gagnés", "Duels aériens gagnés. %", "Tacles glissés PAdj", "Tirs contrés par 90",
                    "Interceptions PAdj", "Fautes par 90", "Cartons reçus"],
        'Construction': ["Passes par 90", "Passes précises. %", "Passes vers l'avant réussies",
                         "Passes dernier tiers réussies", "Passes progressives réussies", "Passes vers la surface réussies",
                         "Passes longues réussies", "Longues passes précises. %", "Passes réceptionnées par 90"],
        'Proportion': ["Proportion passes avant", "Proportion passes latérales", "Proportion passes arrières", 
                       "Proportion passes risquées", "Proportion passes derniers tiers", "Proportion passes longues",
                       "Proportion passes dangereuses", "Proportion passes vers la surface de réparation"]
    }

    # Ajouter le template "Custom"
    templates["Custom"] = "Personnalisé"

    # Sélectionner un template
    template_selectionnee = st.selectbox("Sélectionner un template", list(templates.keys()))

    if template_selectionnee == "Custom":
        st.write("Sélectionnez les caractéristiques que vous souhaitez afficher :")

        carac_selectionnees = []

        # Créer des sections repliables pour chaque catégorie
        for category, carac_list in templates.items():
            if category != "Custom":  # Éviter d'inclure le template "Custom"
                with st.expander(category):
                    # Ajouter un bouton "Tout cocher"
                    check_all = st.checkbox(f"Tout cocher {category}", key=f'check_all_{category}', value=False)
                    
                    # Afficher 3 caractéristiques par ligne
                    cols = st.columns(3)
                    for idx, carac in enumerate(sorted(carac_list)):
                        with cols[idx % 3]:
                            # Si "Tout cocher" est activé, cocher toutes les cases
                            checked = check_all or (category == "Danger" and idx < 5)
                            if st.checkbox(carac, key=f'custom_{carac}', value=checked):
                                carac_selectionnees.append(carac)

        # Utiliser les caractéristiques sélectionnées
        carac_list = carac_selectionnees

    else:
        # Utiliser les caractéristiques du template sélectionné
        carac_list = templates[template_selectionnee]

    joueurs_echantillon = prepare_carac(joueurs_echantillon)

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
    fig = generate_pizza_chart(values_list, carac_names, slice_colors, text_colors)

    # Afficher la figure dans Streamlit
    st.pyplot(fig)

    # Sauvegarder l'image dans un buffer pour permettre le téléchargement
    buffer = io.BytesIO()
    fig.savefig(buffer, format='png', bbox_inches="tight")
    buffer.seek(0)

    # Ajouter le bouton pour télécharger l'image
    st.download_button(
        label="Télécharger le radar pizza en PNG",
        data=buffer,
        file_name=f"radar_pizza_{joueur_selectionne}.png",
        mime="image/png"
    )

    # Afficher la légende sous le graphique
    st.markdown(f"**Référentiel de comparaison :** {postes_to_compare} - {ligue_selectionnee if ligue_selectionnee != 'Toutes' else 'Toutes les ligues'}")
    st.markdown(f"**Nombre de joueurs dans l'échantillon :** {len(joueurs_echantillon)}")
    st.markdown(f"**Nombre minimum de minutes jouées :** {minutes_selectionnees} minutes")