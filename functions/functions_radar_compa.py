import pandas as pd
from functions.radar import Radar
import streamlit as st

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

def choose_carac_and_player(df, name="Alex Bono", carac=None, minimum_minutes=540):
    # Fonction qui permet d'isoler les caractéristiques d'intêret du joueur d'intêret
    if carac is None:
        carac = ["PSxG"]
    df_filter_player = (df['Joueur'] == name)
    df_interet = df[df_filter_player]
    df_interet_filtered = pd.DataFrame()
    df_interet_filtered["Joueur"] = df_interet["Joueur"]
    df_interet_filtered["Équipe dans la période sélectionnée"] = df_interet["Équipe dans la période sélectionnée"]
    df_interet_filtered["Minutes jouées  "] = df_interet["Minutes jouées  "]
    df_interet_filtered['Âge'] = df_interet['Âge']

    try:
        df_filter_player = df["Minutes jouées  "] >= minimum_minutes
    except TypeError:
        df_filter_player = df["Minutes jouées  "].astype("int32") >= minimum_minutes
    df_all_filtered = df[df_filter_player]
    df_all_filtered["Joueur"] = df["Joueur"]
    df_all_filtered["Équipe dans la période sélectionnée"] = df["Équipe dans la période sélectionnée"]
    #df_all_filtered["Pos"] = df["Pos"]
    df_all_filtered["Minutes jouées  "] = df["Minutes jouées  "]
    df_all_filtered['Âge'] = df_all_filtered['Âge']
    # df_all_filtered["Age"] = 2022 - df["Born"]

    for i in carac:
        df_interet_filtered[i] = df_interet[i]
        df_all_filtered[i] = df[i]

    print(df_interet_filtered)
    print(df_all_filtered)
    return df_interet_filtered, df_all_filtered


def calculate_centile(df_all, carac):
    quantiles = []
    for i in carac:
        low_quantile = df_all[i].astype("float").quantile(0.01)
        top_quantile = df_all[i].astype("float").quantile(0.99)
        quantiles.append([i, low_quantile, top_quantile])
    return quantiles


def prepare_radar_data(df_interet, quantiles):
    params = []
    ranges = []
    values = []
    for i in quantiles:
        parameter = carac_abbreviation_to_real_name(i[0])
        params.append(parameter)
        ranges.append((float(i[1]), float(i[2])))
        print(i)
        values.append(float(df_interet[i[0]].values[0]))
    return params, ranges, values


def color_name_to_hex(color_name):
    color_dict = dict()
    with open('data/color.csv', newline='') as f:
        for line in f:
            line = line.strip('\n')
            (key, val) = line[:-2].split(",")
            color_dict[key] = val
        try:
            final_color = color_dict[color_name]
        except KeyError as e:
            print(e, "n'existe pas dans color.csv, prends une autre couleur stp. Je mets du vert en attendant")
            final_color = color_dict["green"]
        return final_color


def carac_abbreviation_to_real_name(carac):
    carac_dict = dict()
    with open('data/Radar_Pizza/carac_names.csv', newline='') as f:
        for line in f:
            line = line.strip('\n')
            (key, val) = line.split(",")
            carac_dict[key] = val[:-1]

    return carac_dict[carac]


def prepare_radar_formatting(name, championnat, df_interet):
    #team = df_interet["Squad"].values[0]
    #position = df_interet["Pos"].values[0]
    age = 30 #df_interet["Âge"].values[0]
    minutes = df_interet["Minutes jouées  "].values[0]
    title_name = "Tetê vs Ailiers du top 5 européen"
    subtitle_name = "OL" + " - " + "Ailier" + " - " + str(22) + " ans" + " - " + str(minutes) + " mins"
    file_name = "images/" + name + ".jpg"

    return title_name, subtitle_name, file_name

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

# Gestion des filtres de ligue, équipe et joueurs
def filter_inputs(df, top_5_ligues):
    col1, col2, col3 = st.columns(3)

    with col1:
        min_minutes, max_minutes = int(df['Minutes jouées  '].min()), int(df['Minutes jouées  '].max())
        minutes_selectionnees = st.number_input("Minutes min.", min_value=min_minutes, max_value=max_minutes, value=min_minutes)

    df = df[df['Minutes jouées  '] >= minutes_selectionnees]

    with col2:
        ligues = df['Team'].unique().tolist()
        ligue_options = ["Toutes les ligues", "Top 5 européen"] + ligues
        ligue_selectionnee = st.selectbox("Championnat", ligue_options)

        if ligue_selectionnee == "Toutes les ligues":
            df = df  # Ne pas filtrer, retourner tout le DataFrame
        elif ligue_selectionnee == "Top 5 européen":
            df = df[df['Team'].isin(top_5_ligues)]  # Filtrer les équipes du Top 5
        else:
            df = df[df['Team'] == ligue_selectionnee]  # Filtrer selon la ligue sélectionnée

    with col3:
        # Ajout du filtre sur l'âge avec un slider (supposant que la colonne "Age" existe)
        min_age = int(df["Âge"].min())  # Age minimal présent dans les données
        max_age = int(df["Âge"].max())  # Age maximal présent dans les données
        age_range = st.slider("Sélectionnez la tranche d'âge", min_value=min_age, max_value=max_age, value=(min_age, max_age))

        # Filtrage du DataFrame par âge
        df = df[(df["Âge"] >= age_range[0]) & (df["Âge"] <= age_range[1])]

    return df, ligue_selectionnee, minutes_selectionnees

# Fonction pour filtrer les joueurs selon la ligue et l'équipe sélectionnée
def filter_players(df, ligue_selectionnee, equipe_selectionnee, top_5_ligues):
    if ligue_selectionnee == "Top 5 européen" and equipe_selectionnee == "Toutes":
        joueurs = df[df['Team'].isin(top_5_ligues)]['Joueur'].unique().tolist()
        joueurs_echantillon = df[df['Team'].isin(top_5_ligues)]
    elif ligue_selectionnee == "Top 5 européen" and equipe_selectionnee != "Toutes":
        joueurs = df[(df['Team'].isin(top_5_ligues)) & (df['Équipe dans la période sélectionnée'] == equipe_selectionnee)]['Joueur'].unique().tolist()
        joueurs_echantillon = df[(df['Team'].isin(top_5_ligues))]
    elif ligue_selectionnee != "Toutes les ligues" and equipe_selectionnee == "Toutes":
        joueurs = df[df['Team'] == ligue_selectionnee]['Joueur'].unique().tolist()
        joueurs_echantillon = df[df['Team'] == ligue_selectionnee]
    elif ligue_selectionnee != "Toutes les ligues" and equipe_selectionnee != "Toutes":
        joueurs = df[(df['Team'] == ligue_selectionnee) & (df['Équipe dans la période sélectionnée'] == equipe_selectionnee)]['Joueur'].unique().tolist()
        joueurs_echantillon = df[(df['Team'] == ligue_selectionnee)]
    elif equipe_selectionnee != "Toutes":
        joueurs = df[df['Équipe dans la période sélectionnée'] == equipe_selectionnee]['Joueur'].unique().tolist()
        joueurs_echantillon = df
    else:
        joueurs = df['Joueur'].unique().tolist()
        joueurs_echantillon = df
    return sorted(joueurs), joueurs_echantillon

# Fonction pour filtrer les joueurs par poste
def filter_by_position(df):

    # Sélection du poste
    postes_options = ["Tous", "Défenseurs centraux", "Latéraux", "Milieux centraux", "Milieux offensifs", "Ailiers", "Buteurs"]
    poste_selectionne = st.selectbox("Sélectionner un poste", postes_options)

    df['Premier poste'] = df['Place'].apply(lambda x: x.split(",")[0].strip())
    
    if poste_selectionne == "Buteurs":
        return df[df['Premier poste'] == 'CF'], poste_selectionne
    elif poste_selectionne == "Ailiers":
        return df[df['Premier poste'].isin(['LW', 'LWF', 'LAMF', 'RW', 'RWF', 'RAMF'])], poste_selectionne
    elif poste_selectionne == "Milieux offensifs":
        return df[df['Premier poste'].isin(['AMF', 'LCMF', 'RCMF'])], poste_selectionne
    elif poste_selectionne == "Milieux centraux":
        return df[df['Premier poste'].isin(['DMF', 'LDMF', 'RDMF', 'LCMF', 'RCMF'])], poste_selectionne
    elif poste_selectionne == "Latéraux":
        return df[df['Premier poste'].isin(['LWB', 'LB', 'RWB', 'RB'])], poste_selectionne
    elif poste_selectionne == "Défenseurs centraux":
        return df[df['Premier poste'].isin(['CB', 'LCB', 'RCB'])], poste_selectionne
    else:
        return df, poste_selectionne  # Si aucun poste n'est sélectionné, retourner tout le DataFrame

# Dictionnaire pour renommer les caractéristiques dans l'interface utilisateur
ui_rename_dict = {
    "23Ast": "Passes amenant à une PD",
    "Buts par 90": "Buts",
    "Passes décisives par 90": "Passes décisives",
    "Passes décisives avec tir par 90": "Passes amenant à un tir",
    "Tirs à la cible. %": "Tirs cadrés %",
    "xA par 90": "xA",
    "Tirs par 90": "Tirs",
    "xG par 90": "xG",
    "Сentres précises. %": "Précision des centres %",

    "Accélérations par 90": "Accélérations",
    "Attaques réussies par 90": "Actions offensives réussies",
    "Courses progressives par 90": "Courses progressives",
    "Dribbles réussis. %": "Réussite des dribbles %",
    "Duels de marquage. %": "Réussite des duels offensifs %",
    "Fautes subies par 90": "Fautes subies",
    "Touches de balle dans la surface de réparation sur 90": "Touches de balle dans la surface",

    "Actions défensives réussies par 90": "Actions défensives réussies",
    "Fautes par 90": "Fautes commises",
    "Tirs contrés par 90": "Tirs contrés",

    "Longues passes précises. %": "Précision passes longues %",
    "Passes précises. %": "Précision passes %",
    "Passes réceptionnées par 90": "Passes réceptionnées",
}

# Gérer la sélection des templates et des caractéristiques personnalisées
def select_template(templates, ui_rename_dict):
    template_selectionnee = st.selectbox("Sélectionner un template", list(templates.keys()))

    if template_selectionnee == "Custom":
        st.write("Sélectionnez les caractéristiques que vous souhaitez afficher :")
        carac_selectionnees = []

        for category, carac_list in templates.items():
            if category != "Custom":
                with st.expander(category):
                    check_all = st.checkbox(f"Tout cocher {category}", key=f'check_all_{category}', value=False)
                    cols = st.columns(3)
                    for idx, carac in enumerate(sorted(carac_list)):
                        ui_label = ui_rename_dict.get(carac, carac)
                        with cols[idx % 3]:
                            checked = check_all or (category == "Danger" and idx < 5)
                            if st.checkbox(ui_label, key=f'custom_{carac}', value=checked):
                                carac_selectionnees.append(carac)
        carac_list = carac_selectionnees
    else:
        carac_list = templates[template_selectionnee]
    
    return carac_list

def double_graph(df, name_1, name_2, carac, championnat, minimum_minutes,
                 couleur_dominante_1, couleur_dominante_2, postes, black_version):
    df_interet_1, df_all = choose_carac_and_player(df, name_1, carac, minimum_minutes)
    df_interet_2, df_all = choose_carac_and_player(df, name_2, carac, minimum_minutes)

    quantiles = calculate_centile(df_all, carac)
    params_1, ranges_1, values_1 = prepare_radar_data(df_interet_1, quantiles)
    params_2, ranges_2, values_2 = prepare_radar_data(df_interet_2, quantiles)

    values = [values_1, values_2]

    _, subtitle_name_1, file_name_1 = prepare_radar_formatting(name_1, championnat, df_interet_1)
    _, subtitle_name_2, file_name_2 = prepare_radar_formatting(name_2, championnat, df_interet_1)

    title_name_1 = name_1
    title_name_2 = name_2

    team_1 = df_interet_1["Équipe dans la période sélectionnée"].values[0]
    age_1 = int(df_interet_1["Âge"].values[0])
    minutes_1 = int(df_interet_1["Minutes jouées  "].values[0])

    team_2 = df_interet_2["Équipe dans la période sélectionnée"].values[0]
    age_2 = int(df_interet_2["Âge"].values[0])
    minutes_2 = int(df_interet_2["Minutes jouées  "].values[0])

    #  ICI SI PROBLEME AVEC LE NOM DES EQUIPES GENRE SALT LAKE CITY
    subtitle_name_1 = team_1 + " - " + str(minutes_1) + " mins" + "\n" + str(age_1) + " ans" #"En défenseur central" #
    subtitle_name_2 = team_2 + " - " + str(minutes_2) + " mins" + "\n" + str(age_2) + " ans" #"En latéral gauche" #

    if black_version:
        couleur_secondaire_1 = "lightgrey"
        couleur_secondaire_2 = "lightgrey"

    else:
        couleur_secondaire_1 = "black"
        couleur_secondaire_2 = "black"

    title = dict(
        title_name=title_name_1,
        title_color=couleur_dominante_1, # color_name_to_hex(couleur_dominante_1),
        subtitle_name=subtitle_name_1,
        subtitle_color=couleur_secondaire_1, # color_name_to_hex(couleur_secondaire_1),
        title_name_2=title_name_2,
        title_color_2=couleur_dominante_2, # color_name_to_hex(couleur_dominante_2),
        subtitle_name_2=subtitle_name_2,
        subtitle_color_2=couleur_secondaire_2, # color_name_to_hex(couleur_secondaire_2),
        title_fontsize=16,
        subtitle_fontsize=15,
    )
    endnote = "Visualisation réalisée par Data'Scout @datascout_\n" \
              " Data/90mins, >" + str(minimum_minutes) + "mins\n" \
              + postes + " - " + championnat + "\n Source : Wyscout"

    if black_version:
        radar = Radar(fontfamily="Liberation Serif", background_color="#121212", patch_color="#28252C",
                      label_color="#FFFFFF",
                      range_color="#FFFFFF", label_fontsize=9, range_fontsize=8)
        end_color = "#95919B"
    else:
        radar = Radar(fontfamily="Liberation Serif", background_color="#FFFFFF", patch_color="#D6D6D6",
                      label_color="#000000",
                      range_color="#000000", label_fontsize=9, range_fontsize=8)
        end_color = "#000000"

    fig, ax = radar.plot_radar(ranges=ranges_1, params=params_1, values=values,
                             radar_color=[couleur_dominante_1, couleur_dominante_2],
                             title=title, alphas=[0.6, 0.6], endnote=endnote, end_color=end_color, end_size=8,
                             compare=True,
                             logo="data/input_images/logo_noir.png", logo_coord=[0.4125, 0.4025, 0.2, 0.15],
                             image_1="data/input_images/lateral.png", image_coord_1=[0.32, 0.79, 0.04, 0.1],
                             image_2="data/input_images/lateral.png", image_coord_2=[0.66, 0.79, 0.04, 0.1])
    
    return fig