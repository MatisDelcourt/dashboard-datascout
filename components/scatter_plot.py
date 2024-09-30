import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from functions.functions_scatter_plot import load_data, filter_inputs, filter_by_position, prepare_carac
import plotly.express as px

def show():
    # Charger les données
    df = load_data("data/Monde.csv")  # Assurez-vous d'adapter le chemin des fichiers

    # Interface utilisateur pour filtrer par ligue, poste, et minutes
    st.title("Scatter Plot - Analyse des joueurs")
    
    top_5_ligues = ['Angleterre D1', 'Allemagne D1', 'Italie D1', 'France D1', 'Espagne D1']

    # Filtrage sur les ligues, minutes
    df_filtered, ligue_selectionnee = filter_inputs(df, top_5_ligues)

    # Filtrage poste
    df_filtered = filter_by_position(df_filtered)

    # Ajout de caracteristiques
    df_filtered = prepare_carac(df_filtered)

    # Renommer la colonne 'Team' en 'Championnat'
    df_filtered = df_filtered.rename(columns={"Team": "Championnat"})

    # Sélection des caractéristiques pour les axes X et Y
    numeric_columns = ["Duels par 90", "Duels gagnés. %", "Actions défensives réussies par 90", "Duels défensifs par 90", "Duels défensifs gagnés. %", "Duels aériens par 90", "Duels aériens gagnés. %", "Tacles glissés PAdj", "Tirs contrés par 90", "Interceptions PAdj", "Fautes par 90", "Cartons jaunes par 90", "Cartons rouges par 90", "Attaques réussies par 90", "Buts par 90", "Buts hors penalty par 90", "xG par 90", "Buts de la tête par 90", "Tirs par 90", "Tirs à la cible. %", "Taux de conversion but/tir", "Passes décisives par 90", "Centres par 90", "Сentres précises. %", "Centres du flanc gauche par 90", "Centres du flanc gauche précises. %", "Centres du flanc droit par 90", "Centres du flanc droit précises. %", "Centres dans la surface de but par 90", "Dribbles par 90", "Dribbles réussis. %", "Duels offensifs par 90", "Duels de marquage. %", "Touches de balle dans la surface de réparation sur 90", "Courses progressives par 90", "Accélérations par 90", "Passes réceptionnées par 90", "Longues passes réceptionnées par 90", "Fautes subies par 90", "Passes par 90", "Passes précises. %", "Passes avant par 90", "Passes en avant précises. %", "Passes arrière par 90", "Passes arrière précises. %", "Passes latérales par 90", "Passes latérales précises. %", "Passes courtes / moyennes par 90", "Passes courtes / moyennes précises. %", "Passes longues par 90", "Longues passes précises. %", "Longueur moyenne des passes. m", "Longueur moyenne des passes longues. m", "xA par 90", "Passes décisives avec tir par 90", "Secondes passes décisives par 90", "Troisièmes passes décisives par 90", "Passes judicieuses par 90", "Passes intelligentes précises. %", "Passes quasi décisives par 90", "Passes dans tiers adverse par 90", "Passes dans tiers adverse précises. %", "Passes vers la surface de réparation par 90", "Passes vers la surface de réparation précises. %", "Passes pénétrantes par 90", "Passes en profondeur précises. %", "Réalisations en profondeur par 90", "Centres en profondeur. par 90", "Passes progressives par 90", "Passes progressives précises. %", "Coups francs par 90", "Coups francs directs par 90", "Coups francs directs à la cible. %", "Corners par 90", "Penalties pris", "Transformation des penalties. %", "Cartons reçus", "Passes réussies", "Passes vers l'avant réussies", "Passes arrière réussies", "Passes latérales réussies", "Passes longues réussies", "Passes dernier tiers réussies", "Passes vers la surface réussies", "Passes progressives réussies", "Duels gagnés", "Duels offensifs gagnés", "Duels défensifs gagnés", "Duels aériens gagnés", "Dribbles réussis", "Centres réussis", "G-xG", "Passes dangereuses", "Terrain gagné", "Passes derniers tiers", "Passes risquées", "Proportion passes avant", "Proportion passes latérales", "Proportion passes arrières", "Proportion passes risquées", "Proportion passes derniers tiers", "Proportion passes longues", "Proportion passes dangereuses", "Proportion passes vers la surface de réparation", "Actions décisives", "Actions décisives attendues"]
    numeric_columns = sorted(numeric_columns)
    x_stat = st.selectbox("Sélectionner la statistique pour l'axe X", numeric_columns)
    y_stat = st.selectbox("Sélectionner la statistique pour l'axe Y", numeric_columns)

    # Calcul des médianes pour les statistiques sélectionnées
    x_median = df_filtered[x_stat].median()
    y_median = df_filtered[y_stat].median()

    # Créer un scatter plot dynamique avec Plotly
    fig = px.scatter(
        df_filtered, 
        x=x_stat, 
        y=y_stat, 
        hover_name="Joueur",  # Afficher le nom du joueur au survol
        color="Championnat",  # Utiliser la colonne 'Team' pour colorer les points
        labels={x_stat: x_stat, y_stat: y_stat},  # Etiquettes personnalisées
        size_max=30,
        title=f"Relation entre {x_stat} et {y_stat}"
    )

    # Ajouter des lignes représentant les médianes
    fig.add_shape(
        type="line", line=dict(dash="dot", color="LightSkyBlue"),
        x0=x_median, x1=x_median, y0=df_filtered[y_stat].min(), y1=df_filtered[y_stat].max(),
        xref="x", yref="y"
    )
    
    fig.add_shape(
        type="line", line=dict(dash="dot", color="LightSkyBlue"),
        x0=df_filtered[x_stat].min(), x1=df_filtered[x_stat].max(), y0=y_median, y1=y_median,
        xref="x", yref="y"
    )

    # Ajuster manuellement la taille des cercles
    fig.update_traces(marker=dict(size=10))  # Par exemple, taille de 9

    # Afficher le scatter plot
    st.plotly_chart(fig)

    # Afficher le DataFrame filtré
    st.subheader("Données filtrées")
    st.dataframe(df_filtered)

    # Exemple : Affichage des filtres sélectionnés
    st.write(f"Ligue sélectionnée : {ligue_selectionnee}")
    st.write(f"Nombre de joueurs dans l'échantillon : {df_filtered.shape[0]}")

