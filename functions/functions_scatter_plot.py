import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import streamlit as st

def load_data(file_path):
    """Charge les données à partir d'un fichier CSV."""
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

# Gestion des filtres de ligue, équipe et joueurs
def filter_inputs(df, top_5_ligues):
    col1, col2, col3 = st.columns(3)

    with col1:
        min_minutes, max_minutes = int(df['Minutes jouées  '].min()), int(df['Minutes jouées  '].max())
        minutes_selectionnees = st.number_input("Minutes min.", min_value=min_minutes, max_value=max_minutes, value=min_minutes)

    df = df[df['Minutes jouées  '] >= minutes_selectionnees]

    with col2:
        ligues = df['Team'].unique().tolist()
        ligue_options = ["Toutes", "Top 5 européen"] + ligues
        ligue_selectionnee = st.selectbox("Championnat", ligue_options)

        if ligue_selectionnee == "Toutes":
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

    return df, ligue_selectionnee

# Fonction pour filtrer les joueurs par poste
def filter_by_position(df):

    # Sélection du poste
    postes_options = ["Tous", "Défenseurs centraux", "Latéraux", "Milieux centraux", "Milieux offensifs", "Ailiers", "Buteurs"]
    poste_selectionne = st.selectbox("Sélectionner un poste", postes_options)

    df['Premier poste'] = df['Place'].apply(lambda x: x.split(",")[0].strip())
    
    if poste_selectionne == "Buteurs":
        return df[df['Premier poste'] == 'CF']
    elif poste_selectionne == "Ailiers":
        return df[df['Premier poste'].isin(['LW', 'LWF', 'LAMF', 'RW', 'RWF', 'RAMF'])]
    elif poste_selectionne == "Milieux offensifs":
        return df[df['Premier poste'].isin(['AMF', 'LCMF', 'RCMF'])]
    elif poste_selectionne == "Milieux centraux":
        return df[df['Premier poste'].isin(['DMF', 'LDMF', 'RDMF', 'LCMF', 'RCMF'])]
    elif poste_selectionne == "Latéraux":
        return df[df['Premier poste'].isin(['LWB', 'LB', 'RWB', 'RB'])]
    elif poste_selectionne == "Défenseurs centraux":
        return df[df['Premier poste'].isin(['CB', 'LCB', 'RCB'])]
    else:
        return df  # Si aucun poste n'est sélectionné, retourner tout le DataFrame

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