import streamlit as st
from functions.functions_radar_pizza import ui_rename_dict, filter_inputs, prepare_carac, display_pizza_chart, load_data, filter_inputs, filter_by_position, filter_players, select_template, display_pizza_chart

def show():
    # Charger les données des joueurs
    df = load_data("data/Monde_2024.csv")

    # Interface utilisateur pour filtrer par ligue et joueur
    st.title("Radar Pizza - Analyse des joueurs")

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

    # Liste des caractéristiques à afficher dans le radar pizza
    # Définir les templates
    templates = {
        'Danger': ["Actions décisives", "Actions décisives attendues", 
                   "xG par 90", "Buts par 90", "xA par 90", "Passes décisives par 90",
                   "Passes décisives avec tir par 90", "23Ast",
                   "Centres réussis", "Сentres précises. %",
                   "Tirs par 90", "Tirs à la cible. %", "Taux de conversion but/tir"],
        'Projection': ["Attaques réussies par 90", 'Courses progressives par 90', 'Accélérations par 90',
                       'Dribbles réussis', "Dribbles réussis. %", 'Duels offensifs gagnés',
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

    carac_list = select_template(templates, ui_rename_dict)

    joueurs_echantillon_prep = prepare_carac(joueurs_echantillon)

    # Affichage du radar pizza
    display_pizza_chart(joueurs_echantillon_prep, player_filter, carac_list, player_of_i, ui_rename_dict, joueurs_echantillon_prep)

    # Afficher la légende sous le graphique
    st.markdown(f"**Référentiel de comparaison :** {postes_to_compare} - {ligue_selectionnee if ligue_selectionnee != 'Toutes' else 'Toutes les ligues'}")
    st.markdown(f"**Nombre de joueurs dans l'échantillon :** {len(joueurs_echantillon_prep)}")
    st.markdown(f"**Nombre minimum de minutes jouées :** {joueurs_echantillon['Minutes jouées  '].min()} minutes")