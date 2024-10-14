import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from mplsoccer import PyPizza
from scipy import stats
import io 

# Charger le CSV
# @st.cache
def load_data(file_path):
    return pd.read_csv(file_path)


def carac_abbreviation_to_real_name(carac, langue):
    carac_dict = dict()
    if langue == 'Français':
        with open('data/carac_names.csv', newline='') as f:
            for line in f:
                line = line.strip('\n')
                (key, val) = line.split(",")
                carac_dict[key] = val
    else:
        with open('data/carac_names_english.csv', newline='') as f:
            for line in f:
                line = line.strip('\n')
                (key, val) = line.split(",")
                carac_dict[key] = val
    return carac_dict[carac]

def get_carac_list(poste, graph="Allégé"):

    if poste == "Gardien":

        if graph == 'Allégé':
            carac_list = [

                "Buts concédés par 90",
                "Pourcentage d'arrêts",
                "Buts évités par 90",
                "Sorties par 90"

            ]
        elif graph == 'Complet':
            carac_list = [

                "Buts concédés par 90",
                "Pourcentage d'arrêts",
                "Buts évités par 90",
                "Sorties par 90"

            ]

    if poste == "Défenseur Central":

        if graph == 'Allégé':
            carac_list = [

                "Buts par 90",
                "xA par 90",

                # DÉFENSIF
                "Duels défensifs gagnés",
                "Duels aériens gagnés",

                "Interceptions par 90",

                "Fautes par 90",
                "Cartons jaunes par 90",

                # OFFENSIF
                "Attaques réussies",

                # PASSES
                "Passes en avant réussies",
                "Passes longues réussies"

            ]
        elif graph == 'Complet':
            carac_list = [

                "Buts par 90",
                "xA par 90",

                # DÉFENSIF
                "Duels défensifs par 90",
                "Duels défensifs gagnés%",
                "Duels aériens par 90",
                "Duels aériens gagnés%",

                "Interceptions par 90",

                "Fautes par 90",
                "Cartons jaunes par 90",

                # OFFENSIF
                "Attaques réussies",

                # PASSES
                "Passes en avant réussies",
                "Passes longues réussies"

            ]

    if poste == "Latéral":

        if graph == 'Allégé':
            carac_list = [

                # DÉCISIF
                "Buts par 90",
                "xA par 90",

                # DÉFENSIF
                "Duels défensifs gagnés",
                "Interceptions par 90",
                "Fautes par 90",

                # OFFENSIF
                "Dribbles réussis",
                "Duels offensifs gagnés",
                "Accélérations réussies",
                # Une course avec le ballon avec une augmentation significative de la vitesse.

                # PASSES
                "Centres réussis",

                # PASSES - AVANCÉ
                "Terrain gagné",  # ["Passes progressives réussies"] + ["Courses progressives"]
                "Passes derniers tiers",
                # ["Passes dans tiers adverse réussies"] + ["Réalisations en profondeur par 90"]
                "Création d'occasion",
                # ["Passes quasi décisives par 90"] + ["Passes vers la surface de réparation réussies"]

            ]
        elif graph == 'Complet':
            carac_list = [

                # DÉCISIF
                "Buts par 90",
                "xA par 90",

                # DÉFENSIF
                "Duels défensifs par 90",
                "Duels défensifs gagnés%",
                "Interceptions par 90",
                "Fautes par 90",

                # OFFENSIF
                "Dribbles par 90",
                "Dribbles réussis%",
                "Duels offensifs par 90",
                "Duels offensifs gagnés%",
                "Accélérations réussies",
                # Une course avec le ballon avec une augmentation significative de la vitesse.

                # PASSES
                "Centres réussis",

                # PASSES - AVANCÉ
                "Terrain gagné",  # ["Passes progressives réussies"] + ["Courses progressives"]
                "Passes derniers tiers",
                # ["Passes dans tiers adverse réussies"] + ["Réalisations en profondeur par 90"]
                "Création d'occasion",
                # ["Passes quasi décisives par 90"] + ["Passes vers la surface de réparation réussies"]

            ]

    if poste == "Milieu Défensif":

        if graph == 'Allégé':
            carac_list = [

                "Buts par 90",
                "xA par 90",

                # DÉFENSIF
                "Duels défensifs gagnés",
                "Duels aériens gagnés",

                "Interceptions par 90",

                "Fautes par 90",
                "Cartons jaunes par 90",

                # OFFENSIF
                "Attaques réussies",

                # PASSES
                "Passes réceptionnées par 90",
                "Passes en avant réussies",
                "Passes longues réussies",

                # PASSES - AVANCÉ
                "Terrain gagné",  # ["Passes progressives réussies"] + ["Courses progressives"]
                "Passes pénétrantes",  # "Passes en profondeur réussies" + "Passes intelligentes réussies"
            ]

        elif graph == 'Complet':
            carac_list = [

                "Buts par 90",
                "xA par 90",

                # DÉFENSIF
                "Duels défensifs par 90",
                "Duels défensifs gagnés%",
                "Duels aériens par 90",
                "Duels aériens gagnés%",

                "Interceptions par 90",

                "Fautes par 90",
                "Cartons jaunes par 90",

                # OFFENSIF
                "Attaques réussies",

                # PASSES
                "Passes réceptionnées par 90",
                "Passes en avant réussies",
                "Passes longues réussies",

                # PASSES - AVANCÉ
                "Terrain gagné",  # ["Passes progressives réussies"] + ["Courses progressives"]
                "Passes pénétrantes",  # "Passes en profondeur réussies" + "Passes intelligentes réussies"
            ]

    if poste == "Milieu Central":

        if graph == 'Allégé':
            carac_list = [

                # DÉCISIF
                "Buts par 90",
                "xA par 90",

                # DÉFENSIF
                "Duels défensifs gagnés",
                "Interceptions par 90",
                "Fautes par 90",

                # OFFENSIF
                "Dribbles réussis",
                "Duels offensifs gagnés",

                # TIRS
                "Tirs cadrés",
                "Passes réceptionnées par 90",

                # PASSES - AVANCÉ
                "Terrain gagné",  # ["Passes progressives réussies"] + ["Courses progressives"]
                "Passes pénétrantes",  # "Passes en profondeur réussies" + "Passes intelligentes réussies"
                "Création d'occasion",
                # ["Passes quasi décisives par 90"] + ["Passes vers la surface de réparation réussies"]

            ]

        elif graph == 'Complet':
            carac_list = [

                # DÉCISIF
                "Buts par 90",
                "xA par 90",

                # DÉFENSIF
                "Duels défensifs par 90",
                "Duels défensifs gagnés%",
                "Interceptions par 90",
                "Fautes par 90",

                # OFFENSIF
                "Dribbles par 90",
                "Dribbles réussis%",
                "Duels offensifs par 90",
                "Duels offensifs gagnés%",

                # TIRS
                "Tirs cadrés",
                "Passes réceptionnées par 90",

                # PASSES - AVANCÉ
                "Terrain gagné",  # ["Passes progressives réussies"] + ["Courses progressives"]
                "Passes pénétrantes",  # "Passes en profondeur réussies" + "Passes intelligentes réussies"
                "Création d'occasion",
                # ["Passes quasi décisives par 90"] + ["Passes vers la surface de réparation réussies"]
            ]

    if poste == "Milieu Offensif":

        if graph == 'Allégé':
            carac_list = [

                # DÉCISIF
                "Buts par 90",
                "xA par 90",

                # OFFENSIF
                "Dribbles réussis",
                "Duels offensifs gagnés",
                "Fautes subies",

                # TIRS
                "Tirs cadrés",

                # PASSES
                "Passes réceptionnées par 90",

                # PASSES - AVANCÉ
                "Terrain gagné",  # ["Passes progressives réussies"] + ["Courses progressives"]
                "Passes pénétrantes",  # "Passes en profondeur réussies" + "Passes intelligentes réussies"
                "Passes derniers tiers",
                # ["Passes dans tiers adverse réussies"] + ["Réalisations en profondeur par 90"]
                "Création d'occasion",
                # ["Passes quasi décisives par 90"] + ["Passes vers la surface de réparation réussies"]
                "2eme et 3eme PD",  # ["Secondes passes décisives par 90"] + ["Troisièmes passes décisives par 90"]
            ]

        elif graph == 'Complet':
            carac_list = [

                # DÉCISIF
                "Buts par 90",
                "xA par 90",

                # OFFENSIF
                "Dribbles par 90",
                "Dribbles réussis%",
                "Duels offensifs par 90",
                "Duels offensifs gagnés%",
                "Fautes subies",

                # TIRS
                "Tirs cadrés",

                # PASSES
                "Passes réceptionnées par 90",

                # PASSES - AVANCÉ
                "Terrain gagné",  # ["Passes progressives réussies"] + ["Courses progressives"]
                "Passes pénétrantes",  # "Passes en profondeur réussies" + "Passes intelligentes réussies"
                "Passes derniers tiers",
                # ["Passes dans tiers adverse réussies"] + ["Réalisations en profondeur par 90"]
                "Création d'occasion",
                # ["Passes quasi décisives par 90"] + ["Passes vers la surface de réparation réussies"]
                "2eme et 3eme PD",  # ["Secondes passes décisives par 90"] + ["Troisièmes passes décisives par 90"]
            ]

    if poste == "Ailier":

        if graph == 'Allégé':
            carac_list = [

                # DÉCISIF
                "Buts par 90",
                "xA par 90",

                # OFFENSIF
                "Dribbles réussis",
                "Duels offensifs gagnés",
                "Accélérations réussies",
                # Une course avec le ballon avec une augmentation significative de la vitesse.
                "Fautes subies",

                # TIRS
                "Tirs cadrés",

                # PASSES
                "Centres réussis",

                # PASSES - AVANCÉ
                "Terrain gagné",  # ["Passes progressives réussies"] + ["Courses progressives"]
                # "Passes pénétrantes",  # "Passes en profondeur réussies" + "Passes intelligentes réussies"
                "Passes derniers tiers",
                # ["Passes dans tiers adverse réussies"] + ["Réalisations en profondeur par 90"]
                "Création d'occasion",
                # ["Passes quasi décisives par 90"] + ["Passes vers la surface de réparation réussies"]
                "2eme et 3eme PD",  # ["Secondes passes décisives par 90"] + ["Troisièmes passes décisives par 90"]

                # DÉFENSIF
                "Actions défensives réussies par 90",
            ]

        elif graph == 'Complet':
            carac_list = [

                # DÉCISIF
                "Buts par 90",
                "xA par 90",

                # OFFENSIF
                "Dribbles par 90",
                "Dribbles réussis%",
                "Duels offensifs par 90",
                "Duels offensifs gagnés%",
                "Accélérations réussies",
                # Une course avec le ballon avec une augmentation significative de la vitesse.
                "Fautes subies",

                # TIRS
                "Tirs cadrés",

                # PASSES
                "Centres réussis",

                # PASSES - AVANCÉ
                "Terrain gagné",  # ["Passes progressives réussies"] + ["Courses progressives"]
                # "Passes pénétrantes",  # "Passes en profondeur réussies" + "Passes intelligentes réussies"
                "Passes derniers tiers",
                # ["Passes dans tiers adverse réussies"] + ["Réalisations en profondeur par 90"]
                "Création d'occasion",
                # ["Passes quasi décisives par 90"] + ["Passes vers la surface de réparation réussies"]
                "2eme et 3eme PD",  # ["Secondes passes décisives par 90"] + ["Troisièmes passes décisives par 90"]

                # DÉFENSIF
                "Actions défensives réussies par 90",
            ]

    if poste == "Buteur":

        if graph == 'Allégé':
            carac_list = [

                # DÉCISIF
                "Buts par 90",
                "xA par 90",

                # DÉFENSIF
                "Duels aériens gagnés",

                # OFFENSIF
                "Touches de balle dans la surface de réparation",
                "Dribbles réussis",
                "Duels offensifs gagnés",
                "Accélérations réussies",
                # Une course avec le ballon avec une augmentation significative de la vitesse.
                "Fautes subies",

                # TIRS
                "Tirs cadrés",

                # PASSES - AVANCÉ
                "Passes derniers tiers",
                # ["Passes dans tiers adverse réussies"] + ["Réalisations en profondeur par 90"]
                "Création d'occasion",
                # ["Passes quasi décisives par 90"] + ["Passes vers la surface de réparation réussies"]
                "2eme et 3eme PD",  # ["Secondes passes décisives par 90"] + ["Troisièmes passes décisives par 90"]
            ]

        elif graph == 'Complet':
            carac_list = [

                # DÉCISIF
                "Buts par 90",
                "xA par 90",

                # DÉFENSIF
                "Duels aériens par 90",
                "Duels aériens gagnés%",

                # OFFENSIF
                "Touches de balle dans la surface de réparation",
                "Dribbles par 90",
                "Dribbles réussis%",
                "Duels offensifs par 90",
                "Duels offensifs gagnés%",
                "Accélérations réussies",
                # Une course avec le ballon avec une augmentation significative de la vitesse.
                "Fautes subies",

                # TIRS
                "Tirs cadrés",

                # PASSES - AVANCÉ
                "Passes derniers tiers",
                # ["Passes dans tiers adverse réussies"] + ["Réalisations en profondeur par 90"]
                "Création d'occasion",
                # ["Passes quasi décisives par 90"] + ["Passes vers la surface de réparation réussies"]
                "2eme et 3eme PD",  # ["Secondes passes décisives par 90"] + ["Troisièmes passes décisives par 90"]
            ]

    if poste == "Spécifique":

        if graph == 'Défensif':
            carac_list = [

                # DÉFENSIF
                "Actions défensives réussies par 90",

                "Tacles glissés PAdj",
                "Interceptions par 90",
                "Tirs contrés PAdj",

                "Fautes par 90",
                "Cartons jaunes par 90",
                "Cartons rouges par 90",

            ]

        if graph == 'Duels':
            carac_list = [

                "Duels défensifs par 90",
                "Duels défensifs gagnés%",
                "Duels aériens par 90",
                "Duels aériens gagnés%",
                "Duels offensifs par 90",
                "Duels offensifs gagnés%",
            ]

        if graph == 'Projection':
            carac_list = [

                # OFFENSIF
                "Attaques réussies",
                "Touches de balle dans la surface de réparation",
                "Dribbles par 90",
                "Dribbles réussis%",
                "Courses progressives réussies",
                "Accélérations réussies",
                # Une course avec le ballon avec une augmentation significative de la vitesse.
                "Fautes subies",
            ]

        if graph == 'Finition':
            carac_list = [

                # TIRS
                "Buts par 90",
                "xG par 90",
                "Buts hors pénalty par 90",
                "Buts de la tête par 90",
                "Tirs par 90",
                "Tirs cadrés %",
                "Taux de conversion but/tir",
            ]

        if graph == 'Construction':
            carac_list = [

                # PASSES
                "Passes réceptionnées par 90",
                "Passes réussies",
                "Passes en avant réussies",
                "Passes longues réussies",
                "Passes en profondeur réussies",
                "Passes progressives réussies",

            ]

        if graph == 'Création':
            carac_list = [

                "Passes décisives par 90",
                "xA par 90",
                "2eme et 3eme PD",  # ["Secondes passes décisives par 90"] + ["Troisièmes passes décisives par 90"]
                "Passes quasi décisives par 90",
                "Passes intelligentes réussies",
                "Passes derniers tiers",
                # ["Passes dans tiers adverse réussies"] + ["Réalisations en profondeur par 90"]
                "Passes vers la surface de réparation réussies",
                "Centres réussis",

            ]

        if graph == 'Passes Adj':
            carac_list = [

                "Pondération passes en avant réussies",
                "Pondération passes latérales réussies",
                "Pondération passes arrières réussies",
                "Pondération passes en profondeur réussies",
                #"Pondération passes vers la surface de réparation réussies",
                "Pondération passes derniers tiers réussies",
                #"Pondération passes intelligentes réussies",
                "Pondération passes progressives réussies",
                #"Pondération passes dangereuses",

            ]

    if poste == "Personnalisé" and (graph == "Allégé" or graph == "Complet"):
        carac_list = [
            # DÉCISIF
            "Minutes jouées",
            "Buts par 90",
            "xG par 90",
            "G-xG",
            "Passes décisives par 90",
            "xA par 90",

            # TIRS
            "Tirs par 90",
            "Tirs cadrés %",
            "Tirs cadrés",
            "Taux de conversion but/tir",

            # DÉFENSIF
            "Actions défensives réussies par 90",
            "Duels défensifs gagnés PAdj",
            "Duels aériens gagnés",

            "Tacles glissés PAdj",
            "Interceptions PAdj",
            "Tirs contrés PAdj",

            # OFFENSIF
            "Passes réceptionnées par 90",
            "Attaques réussies",
            "Touches de balle dans la surface de réparation",
            "Dribbles réussis",
            "Duels offensifs gagnés",
            "Accélérations réussies",  # Une course avec le ballon avec une augmentation significative de la vitesse.
            "Fautes subies",

            # PASSES
            "Passes réussies",
            "Passes en avant réussies",
            'Passes longues réussies',
            "Centres réussis",  # (["Centres par 90"] * ["Сentres précises%"] / 100)

            # PASSES - AVANCÉ
            "Terrain gagné",  # ["Passes progressives réussies"] + ["Courses progressives"]
            "Passes pénétrantes",  # "Passes en profondeur réussies" + "Passes intelligentes réussies"
            "Passes derniers tiers",  # ["Passes dans tiers adverse réussies"] + ["Réalisations en profondeur par 90"]
            "Création d'occasion",
            # ["Passes quasi décisives par 90"] + ["Passes vers la surface de réparation réussies"]
            "2eme et 3eme PD",  # ["Secondes passes décisives par 90"] + ["Troisièmes passes décisives par 90"]
        ]

    if poste == "Tout":
        carac_list = [
            # DÉCISIF
            "Minutes jouées",
            "Buts par 90",
            "xG par 90",
            "G-xG",
            "Passes décisives par 90",
            "xA par 90",

            # TIRS
            "Tirs par 90",
            "Tirs cadrés %",
            "Tirs cadrés",
            #"Taux de conversion but/tir",

            # DÉFENSIF
            "Actions défensives réussies par 90",
            "Duels défensifs gagnés PAdj",
            "Duels aériens gagnés",

            "Tacles glissés PAdj",
            "Interceptions PAdj",
            "Tirs contrés PAdj",

            # OFFENSIF
            "Passes réceptionnées par 90",
            "Attaques réussies",
            "Touches de balle dans la surface de réparation",
            "Dribbles réussis",
            "Duels offensifs gagnés",
            "Accélérations réussies",  # Une course avec le ballon avec une augmentation significative de la vitesse.
            "Fautes subies",



            # PASSES
            "Passes réussies",
            "Passes en avant réussies",
            'Passes longues réussies',
            "Centres réussis",  # (["Centres par 90"] * ["Сentres précises%"] / 100)

            # PASSES - AVANCÉ
            "Terrain gagné",  # ["Passes progressives réussies"] + ["Courses progressives"]
            "Passes pénétrantes",  # "Passes en profondeur réussies" + "Passes intelligentes réussies"
            "Passes derniers tiers",  # ["Passes dans tiers adverse réussies"] + ["Réalisations en profondeur par 90"]
            "Création d'occasion",
            # ["Passes quasi décisives par 90"] + ["Passes vers la surface de réparation réussies"]
            "2eme et 3eme PD",  # ["Secondes passes décisives par 90"] + ["Troisièmes passes décisives par 90"]
        ]

    return carac_list

def get_players_final(player_filter):
    players_final = player_filter

    players_final["Player"] = players_final["Joueur"]
    players_final["Squad"] = players_final["Équipe"]
    players_final["Age"] = players_final["Âge"]
    players_final["Buts attendus"] = players_final["xG"]
    players_final["Buts hors pénalty"] = players_final["Buts hors penaltyButs hors penalty"]
    players_final["Buts hors pénalty par 90"] = players_final["Buts hors penalty par 90"]
    players_final["Pénalties marqués"] = players_final["Penalties pris"] * players_final["Transformation des penalties, %"] / 100
    players_final["Passes décisives attendues"] = players_final["xA"]
    players_final["Minutes jouées"] = players_final["Minutes jouées  "]
    players_final["Duels défensifs gagnés%"] = players_final["Duels défensifs gagnés, %"]
    players_final["Duels offensifs gagnés%"] = players_final["Duels de marquage, %"]
    players_final["Passes vers la surface de réparation réussies"] = players_final["Passes vers la surface de réparation par 90"] * players_final["Passes vers la surface de réparation précises, %"] / 100
    players_final["Duels aériens gagnés%"] = players_final["Duels aériens gagnés, %"]
    players_final["Duels gagnés%"] = players_final["Duels gagnés, %"]
    players_final["Duels disputés"] = players_final["Duels par 90"]
    players_final["Pourcentage d'arrêts"] = players_final["Enregistrer, %"]
    players_final["Сentres précis%"] = players_final["Сentres précises, %"]
    players_final["Dribbles réussis%"] = players_final["Dribbles réussis, %"]
    players_final["Passes réussies %"] = players_final["Passes précises, %"]
    players_final["Passes réussies"] = players_final["Passes par 90"] * players_final["Passes réussies %"] / 100
    players_final["Passes latérales réussies"] = players_final["Passes latérales par 90"] * players_final["Passes latérales précises, %"] / 100
    players_final["Passes arrières réussies"] = players_final["Passes arrière par 90"] * players_final["Passes arrière précises, %"] / 100
    players_final["Passes dans tiers adverse réussies"] = players_final["Passes dans tiers adverse par 90"] * players_final["Passes dans tiers adverse précises, %"] / 100
    players_final["Passes en profondeur réussies"] = players_final["Passes pénétrantes par 90"] * players_final["Passes en profondeur précises, %"] / 100
    players_final["Passes longues précises %"] = players_final["Longues passes précises, %"]
    players_final["Passes longues réussies"] = players_final["Passes longues par 90"] * players_final["Passes longues précises %"] / 100
    players_final["Passes en avant précises %"] = players_final["Passes en avant précises, %"]
    players_final["Сentres du flanc gauche précises%"] = players_final["Centres du flanc gauche précises, %"]
    players_final["Passes courtes moyennes par 90"] = players_final["Passes courtes / moyennes par 90"]
    players_final["Passes courtes moyennes réussies %"] = players_final["Passes courtes / moyennes précises, %"]
    players_final["Passes intelligentes précises %"] = players_final["Passes intelligentes précises, %"]
    players_final["Passes progressives réussies"] = players_final["Passes progressives par 90"] * players_final["Passes progressives précises, %"] / 100
    players_final["Passes intelligentes réussies"] = players_final["Passes judicieuses par 90"] * players_final["Passes intelligentes précises %"] / 100
    players_final["Passes en avant réussies"] = players_final["Passes avant par 90"] * players_final["Passes en avant précises %"] / 100
    players_final["Tirs cadrés %"] = players_final["Tirs à la cible, %"]
    players_final["Tirs cadrés"] = players_final["Tirs par 90"] * players_final["Tirs cadrés %"] / 100
    players_final["Coups francs cadrés"] = players_final["Coups francs directs par 90"] * players_final["Coups francs directs à la cible, %"] / 100
    players_final["Duels gagnés"] = players_final["Duels par 90"] * players_final["Duels gagnés%"] / 100
    players_final["Duels défensifs gagnés"] = players_final["Duels défensifs par 90"] * players_final["Duels défensifs gagnés%"] / 100
    players_final["Duels aériens gagnés"] = players_final["Duels aériens par 90"] * players_final["Duels aériens gagnés%"] / 100
    players_final["2eme et 3eme PD"] = players_final["Secondes passes décisives par 90"] + players_final["Troisièmes passes décisives par 90"]
    players_final["G-xG"] = players_final["Buts par 90"] - players_final["xG par 90"]
    players_final["Longueur moyenne des passes"] = players_final["Longueur moyenne des passes, m"]


    players_final["Création d'occasion"] = players_final["Passes quasi décisives par 90"] + players_final["Passes vers la surface de réparation réussies"]
    players_final["Passes pénétrantes"] = players_final["Passes en profondeur réussies"] + players_final["Passes intelligentes réussies"]

    players_final["Centres réussis"] = players_final["Centres par 90"] * players_final["Сentres précises, %"] / 100
    players_final["Pondération centres réussis"] = players_final["Centres réussis"] / players_final["Passes réceptionnées par 90"]
    players_final["Centres dans la surface de but réussis"] = players_final["Centres dans la surface de but par 90"]
    players_final["Pondération centres dans la surface de but réussis"] = players_final["Centres dans la surface de but réussis"] / players_final["Passes réceptionnées par 90"]

    players_final["Passes derniers tiers"] = players_final["Passes dans tiers adverse réussies"] + players_final["Réalisations en profondeur par 90"]
    players_final["Actions décisives"] = players_final["Buts par 90"] + players_final["Passes décisives par 90"]
    players_final["Actions décisives attendues"] = players_final["xG par 90"] + players_final["xA par 90"]

    players_final["Attaques réussies"] = players_final["Attaques réussies par 90"]
    players_final["Pondération attaques réussies"] = players_final["Attaques réussies"] / players_final["Passes réceptionnées par 90"]
    players_final["Touches de balle dans la surface de réparation"] = players_final["Touches de balle dans la surface de réparation sur 90"]
    players_final["Pondération touches de balle dans la surface de réparation"] = players_final["Touches de balle dans la surface de réparation"] / players_final["Passes réceptionnées par 90"]
    players_final["Accélérations réussies"] = players_final["Accélérations par 90"]
    players_final["Pondération accélérations réussies"] = players_final["Accélérations réussies"] / players_final["Passes réceptionnées par 90"]
    players_final["Courses progressives réussies"] = players_final["Courses progressives par 90"]
    players_final["Pondération courses progressives réussies"] = players_final["Courses progressives réussies"] / players_final["Passes réceptionnées par 90"]
    players_final["Fautes subies"] = players_final["Fautes subies par 90"]

    players_final["Pondération fautes subies"] = players_final["Fautes subies"] / players_final["Passes réceptionnées par 90"]
    players_final["Dribbles réussis"] = players_final["Dribbles par 90"] * players_final["Dribbles réussis%"] / 100
    players_final["Pondération dribbles réussis"] = (players_final["Dribbles par 90"] * players_final["Dribbles réussis%"] / 100) / players_final["Passes réceptionnées par 90"]
    players_final["Duels offensifs gagnés"] = players_final["Duels offensifs par 90"] * players_final["Duels offensifs gagnés%"] / 100
    players_final["Pondération duels offensifs gagnés"] = (players_final["Duels offensifs par 90"] * players_final["Duels offensifs gagnés%"] / 100) / players_final["Passes réceptionnées par 90"]

    players_final["Pondération tirs cadrés"] = players_final["Tirs cadrés"] / players_final["Passes réceptionnées par 90"]

    coefficient_possession = players_final["Interceptions PAdj"] / players_final["Interceptions par 90"]
    players_final["Duels défensifs gagnés PAdj"] = players_final["Duels défensifs gagnés"] * coefficient_possession
    players_final["Tirs contrés PAdj"] = players_final["Tirs contrés par 90"] * coefficient_possession

    players_final["Touches de balle par but"] = players_final["Buts par 90"] / players_final["Passes réceptionnées par 90"]
    players_final["Touches de balle par passe décisive"] = players_final["Passes décisives par 90"] / players_final["Passes réceptionnées par 90"]

    players_final["Terrain gagné"] = players_final["Passes progressives réussies"] + players_final["Courses progressives réussies"]

    players_final["Pondération passes en avant réussies"] = players_final["Passes en avant réussies"] / players_final["Passes réceptionnées par 90"]
    players_final["Pondération passes latérales réussies"] = players_final["Passes latérales réussies"] / players_final["Passes réceptionnées par 90"]
    players_final["Pondération passes arrières réussies"] = players_final["Passes arrières réussies"] / players_final["Passes réceptionnées par 90"]
    players_final["Pondération passes en profondeur réussies"] = players_final["Passes en profondeur réussies"] / players_final["Passes réceptionnées par 90"]
    players_final["Pondération passes vers la surface de réparation réussies"] = players_final["Passes vers la surface de réparation réussies"] / players_final["Passes réceptionnées par 90"]
    players_final["Pondération passes derniers tiers réussies"] = players_final["Passes dans tiers adverse réussies"] / players_final["Passes réceptionnées par 90"]
    players_final["Pondération passes intelligentes réussies"] = players_final["Passes intelligentes réussies"] / players_final["Passes réceptionnées par 90"]
    players_final["Pondération passes progressives réussies"] = players_final["Passes progressives réussies"] / players_final["Passes réceptionnées par 90"]
    players_final["Pondération passes dangereuses"] = players_final["Création d'occasion"] / players_final["Passes réceptionnées par 90"]
    players_final["Pondération passes quasi décisives par 90"] = players_final["Passes quasi décisives par 90"] / players_final["Passes réceptionnées par 90"]
    players_final["Pondération secondes passes décisives par 90"] = players_final["Secondes passes décisives par 90"] / players_final["Passes réceptionnées par 90"]
    players_final["Pondération troisièmes passes décisives par 90"] = players_final["Troisièmes passes décisives par 90"] / players_final["Passes réceptionnées par 90"]

    players_final["Proportion passes en avant réussies"] = players_final["Passes en avant réussies"] / players_final["Passes réussies"]
    players_final["Proportion passes latérales réussies"] = players_final["Passes latérales réussies"] / players_final["Passes réussies"]
    players_final["Proportion passes arrières réussies"] = players_final["Passes arrières réussies"] / players_final["Passes réussies"]
    players_final["Proportion passes en profondeur réussies"] = players_final["Passes en profondeur réussies"] / players_final["Passes réussies"]
    players_final["Proportion passes vers la surface de réparation réussies"] = players_final["Passes vers la surface de réparation réussies"] / players_final["Passes réussies"]
    players_final["Proportion passes derniers tiers réussies"] = players_final["Passes dans tiers adverse réussies"] / players_final["Passes réussies"]
    players_final["Proportion passes intelligentes réussies"] = players_final["Passes intelligentes réussies"] / players_final["Passes réussies"]
    players_final["Proportion passes progressives réussies"] = players_final["Passes progressives réussies"] / players_final["Passes réussies"]
    players_final["Proportion passes dangereuses"] = players_final["Création d'occasion"] / players_final["Passes par 90"]

    players_final["Fautes commises"] = -(players_final["Fautes par 90"])
    players_final["Cartons jaunes reçus"] = -(players_final["Cartons jaunes par 90"])
    players_final["Cartons rouges reçus"] = -(players_final["Cartons rouges par 90"])

    return players_final
