import io
import streamlit as st
import pandas as pd
from functions.functions_radar_compa import double_graph, prepare_carac, filter_inputs, filter_by_position, select_template, ui_rename_dict

def show():
    # Charger les données des joueurs
    df = pd.read_csv('data/Monde.csv')

    # Interface utilisateur pour sélectionner deux joueurs
    st.title("Radar Comparaison - Analyse des joueurs")

    top_5_ligues = ['Angleterre D1', 'Allemagne D1', 'Italie D1', 'France D1', 'Espagne D1']

    # Filtrage sur les ligues, minutes
    df_filtered, ligue_selectionnee, minimum_minutes = filter_inputs(df, top_5_ligues)

    # Filtrage poste
    df_filtered, postes = filter_by_position(df_filtered)

    df = prepare_carac(df_filtered)

    col1, col2 = st.columns(2)

    # Sélection du joueur 1 et sa couleur
    with col1:
        joueur_1 = st.selectbox("Sélectionner le joueur 1", df['Joueur'].unique(), key="joueur_1")
        joueur_2 = st.selectbox("Sélectionner le joueur 2", df['Joueur'].unique(), key="joueur_2")

    # Sélection du joueur 2 et sa couleur
    with col2:
        couleur_joueur_1 = st.color_picker("Couleur du joueur 1", "#0000FF")  # Couleur bleue par défaut
        couleur_joueur_2 = st.color_picker("Couleur du joueur 2", "#FF0000")  # Couleur rouge par défaut


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

    # Générer et afficher le radar
    fig = double_graph(
                df=df,
                name_1=joueur_1,
                name_2=joueur_2,
                carac=carac_list,
                championnat=ligue_selectionnee,  # Exemple de championnat
                minimum_minutes=minimum_minutes,
                couleur_dominante_1=couleur_joueur_1,
                couleur_dominante_2=couleur_joueur_2,
                postes=postes,
                black_version=False
            )
        
    # Afficher la figure
    st.pyplot(fig)

    buffer = io.BytesIO()
    fig.savefig(buffer, format='png', bbox_inches="tight")
    buffer.seek(0)

    st.download_button(
        label="Télécharger le radar en PNG",
        data=buffer,
        file_name=f"radar_pizza_{joueur_1}_vs{joueur_2}.png",
        mime="image/png"
    )

    st.markdown(f"**Nombre de joueurs dans l'échantillon :** {len(df)}")