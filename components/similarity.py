from io import BytesIO
import pandas as pd
import numpy as np
from scipy.spatial.distance import cosine
from scipy import stats
import streamlit as st

# Fonction pour convertir le DataFrame en fichier Excel téléchargeable
def convert_df_to_excel(df):
    output = BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False)  # Écrire le DataFrame dans le fichier Excel
    processed_data = output.getvalue()  # Obtenir le contenu du fichier Excel
    return processed_data

# Fonction pour calculer le coefficient_possession
def calculate_coefficient(row):
    if row['Interceptions par 90'] != 0:
        return row['Interceptions PAdj'] / row['Interceptions par 90']
    else:
        return row['Tacles glissés PAdj'] / row['Tacles glissés par 90'] if row['Tacles glissés par 90'] != 0 else None

def read_coefficients(file_path, role):
    try:
        # Lire le fichier Excel dans un DataFrame
        df = pd.read_excel(file_path)

        # Vérifier si le rôle demandé existe dans les colonnes du DataFrame
        if role in df.columns:
            # Transformer la colonne en dictionnaire où les indices sont les caractéristiques
            coefficients_dict = df.set_index('Caractéristique')[role].to_dict()
            return coefficients_dict
        else:
            print(f"Le rôle {role} n'est pas trouvé dans le fichier.")
            return None
    except Exception as e:
        print(f"Erreur lors de la lecture des coefficients pour le rôle {role}: {e}")
        return None

def calculate_average_score_for_post(df, carac_list, player_name, roles, poste):
    coefficients_path = "data/Métriques.xlsx"  # Chemin vers le fichier Excel des coefficients
    score_totals = None  # Pour accumuler les scores sur les différents rôles
    role_count = 0  # Pour compter combien de rôles ont été utilisés

    for role in roles:
        coefficients_dict = read_coefficients(coefficients_path, role)

        if coefficients_dict is None:
            print(f"Coefficients pour le rôle {role} non trouvés ou erreur de lecture.")
            continue  # Passer à l'itération suivante si les coefficients ne sont pas trouvés

        if not df['Doublon'].str.contains(player_name).any():
            print(f"{player_name} n'est pas trouvé dans le DataFrame.")
            continue  # Passer à l'itération suivante si le joueur n'est pas trouvé

        player_data = df[df['Doublon'].str.contains(player_name)].iloc[0]
        player_vec = np.array([player_data[feat] * coefficients_dict.get(feat, 1) for feat in carac_list])
        
        # Calculer les scores de similarité pour le rôle actuel
        #df['Score'] = df.apply(lambda x: round((1 - cosine(player_vec, np.array([x[feat] * coefficients_dict.get(feat, 1) for feat in carac_list]))) * 100, 2), axis=1)
        
        df['Score'] = df.apply(lambda x: round((1 - cosine(np.power(player_vec, 2), np.power(np.array([x[feat] * coefficients_dict.get(feat, 1) for feat in carac_list]), 2))) * 100, 2), axis=1)
        
        if score_totals is None:
            score_totals = df['Score'].copy()  # Initialiser la somme des scores
        else:
            score_totals += df['Score']  # Ajouter les scores au total

        role_count += 1  # Incrémenter le compteur de rôles

    if role_count > 0:
        df['Score'] = score_totals / role_count  # Calculer la moyenne des scores
    else:
        df['Score'] = None  # Si aucun score n'a été calculé, laisser une valeur nulle

    # Créer un DataFrame exportable
    df_export = df[
        ['Doublon', 'Score', 'Âge', 'Équipe dans la période sélectionnée', 'Place', 'Team', 'Valeur marchande']].copy()
    df_export['Doublon'] = df_export['Doublon'].apply(lambda x: x.split(' - ')[0])

    return df_export

def show():
    # Chemin vers votre fichier Excel
    file_path = 'data/Monde_2024.csv'

    # Charger le fichier Excel dans un DataFrame
    df = pd.read_csv(file_path)
    df["Buts attendus"] = df["xG"]
    df["Buts hors pénalty"] = df["Buts hors penaltyButs hors penalty"]
    df["Buts hors pénalty par 90"] = df["Buts hors penalty par 90"]
    df["Pénalties marqués"] = df["Penalties pris"] * df["Transformation des penalties, %"] / 100
    df["Passes décisives attendues"] = df["xA"]
    df["Minutes jouées"] = df["Minutes jouées  "]
    df["Duels défensifs gagnés%"] = df["Duels défensifs gagnés, %"]
    df["Duels offensifs gagnés%"] = df["Duels de marquage, %"]
    df["Passes vers la surface de réparation réussies"] = df["Passes vers la surface de réparation par 90"] * df[
        "Passes vers la surface de réparation précises, %"] / 100
    df["Duels aériens gagnés%"] = df["Duels aériens gagnés, %"]
    df["Duels gagnés%"] = df["Duels gagnés, %"]
    df["Duels disputés"] = df["Duels par 90"]
    df["Сentres précis%"] = df["Сentres précises, %"]
    df["Dribbles réussis%"] = df["Dribbles réussis, %"]
    df["Passes réussies %"] = df["Passes précises, %"]
    df["Passes réussies"] = df["Passes par 90"] * df["Passes réussies %"] / 100
    df["Passes latérales réussies"] = df["Passes latérales par 90"] * df["Passes latérales précises, %"] / 100
    df["Passes arrières réussies"] = df["Passes arrière par 90"] * df["Passes arrière précises, %"] / 100
    df["Passes dans tiers adverse réussies"] = df["Passes dans tiers adverse par 90"] * df[
        "Passes dans tiers adverse précises, %"] / 100
    df["Passes en profondeur réussies"] = df["Passes pénétrantes par 90"] * df["Passes en profondeur précises, %"] / 100
    df["Passes longues précises %"] = df["Longues passes précises, %"]
    df["Passes longues réussies"] = df["Passes longues par 90"] * df["Passes longues précises %"] / 100
    df["Passes en avant précises %"] = df["Passes en avant précises, %"]
    df["Сentres du flanc gauche précises%"] = df["Centres du flanc gauche précises, %"]
    df["Passes courtes moyennes par 90"] = df["Passes courtes / moyennes par 90"]
    df["Passes courtes moyennes réussies %"] = df["Passes courtes / moyennes précises, %"]
    df["Passes intelligentes précises %"] = df["Passes intelligentes précises, %"]
    df["Passes progressives réussies"] = df["Passes progressives par 90"] * df["Passes progressives précises, %"] / 100
    df["Passes intelligentes réussies"] = df["Passes judicieuses par 90"] * df["Passes intelligentes précises %"] / 100
    df["Passes en avant réussies"] = df["Passes avant par 90"] * df["Passes en avant précises %"] / 100
    df["Tirs cadrés %"] = df["Tirs à la cible, %"]
    df["Tirs cadrés"] = df["Tirs par 90"] * df["Tirs cadrés %"] / 100
    df["Coups francs cadrés"] = df["Coups francs directs par 90"] * df["Coups francs directs à la cible, %"] / 100
    df["Duels gagnés"] = df["Duels par 90"] * df["Duels gagnés%"] / 100
    df["Duels défensifs gagnés"] = df["Duels défensifs par 90"] * df["Duels défensifs gagnés%"] / 100
    df["Duels aériens gagnés"] = df["Duels aériens par 90"] * df["Duels aériens gagnés%"] / 100
    df["2eme et 3eme PD"] = df["Secondes passes décisives par 90"] + df["Troisièmes passes décisives par 90"]
    df["G-xG"] = df["Buts par 90"] - df["xG par 90"]
    df["Longueur moyenne des passes"] = df["Longueur moyenne des passes, m"]

    df["Création d'occasion"] = df["Passes quasi décisives par 90"] + df["Passes vers la surface de réparation réussies"]
    df["Passes pénétrantes"] = df["Passes en profondeur réussies"] + df["Passes intelligentes réussies"]

    df["Centres réussis"] = df["Centres par 90"] * df["Сentres précises, %"] / 100
    df["Pondération centres réussis"] = df["Centres réussis"] / df["Passes réceptionnées par 90"]
    df["Centres dans la surface de but réussis"] = df["Centres dans la surface de but par 90"]
    df["Pondération centres dans la surface de but réussis"] = df["Centres dans la surface de but réussis"] / df[
        "Passes réceptionnées par 90"]

    df["Passes derniers tiers"] = df["Passes dans tiers adverse réussies"] + df["Réalisations en profondeur par 90"]
    df["Actions décisives"] = df["Buts par 90"] + df["Passes décisives par 90"]
    df["Actions décisives attendues"] = df["xG par 90"] + df["xA par 90"]

    df["Attaques réussies"] = df["Attaques réussies par 90"]
    df["Pondération attaques réussies"] = df["Attaques réussies"] / df["Passes réceptionnées par 90"]
    df["Touches de balle dans la surface de réparation"] = df["Touches de balle dans la surface de réparation sur 90"]
    df["Pondération touches de balle dans la surface de réparation"] = df[
                                                                        "Touches de balle dans la surface de réparation"] / \
                                                                    df["Passes réceptionnées par 90"]
    df["Accélérations réussies"] = df["Accélérations par 90"]
    df["Pondération accélérations réussies"] = df["Accélérations réussies"] / df["Passes réceptionnées par 90"]
    df["Courses progressives réussies"] = df["Courses progressives par 90"]
    df["Pondération courses progressives réussies"] = df["Courses progressives réussies"] / df[
        "Passes réceptionnées par 90"]
    df["Fautes subies"] = df["Fautes subies par 90"]

    df["Pondération fautes subies"] = df["Fautes subies"] / df["Passes réceptionnées par 90"]
    df["Dribbles réussis"] = df["Dribbles par 90"] * df["Dribbles réussis%"] / 100
    df["Pondération dribbles réussis"] = (df["Dribbles par 90"] * df["Dribbles réussis%"] / 100) / df[
        "Passes réceptionnées par 90"]
    df["Duels offensifs gagnés"] = df["Duels offensifs par 90"] * df["Duels offensifs gagnés%"] / 100
    df["Pondération duels offensifs gagnés"] = (df["Duels offensifs par 90"] * df["Duels offensifs gagnés%"] / 100) / df[
        "Passes réceptionnées par 90"]

    df["Pondération tirs cadrés"] = df["Tirs cadrés"] / df["Passes réceptionnées par 90"]

    # Appliquer la fonction sur chaque ligne du DataFrame
    df['coefficient_possession'] = df.apply(calculate_coefficient, axis=1)

    df["Duels défensifs gagnés PAdj"] = df["Duels défensifs gagnés"] * df['coefficient_possession']
    df["Tirs contrés PAdj"] = df["Tirs contrés par 90"] * df['coefficient_possession']

    df["Touches de balle par but"] = df["Buts par 90"] / df["Passes réceptionnées par 90"]
    df["Touches de balle par passe décisive"] = df["Passes décisives par 90"] / df["Passes réceptionnées par 90"]

    df["Terrain gagné"] = df["Passes progressives réussies"] + df["Courses progressives réussies"]

    df["Pondération passes en avant réussies"] = df["Passes en avant réussies"] / df["Passes réceptionnées par 90"]
    df["Pondération passes latérales réussies"] = df["Passes latérales réussies"] / df["Passes réceptionnées par 90"]
    df["Pondération passes arrières réussies"] = df["Passes arrières réussies"] / df["Passes réceptionnées par 90"]
    df["Pondération passes en profondeur réussies"] = df["Passes en profondeur réussies"] / df[
        "Passes réceptionnées par 90"]
    df["Pondération passes vers la surface de réparation réussies"] = df["Passes vers la surface de réparation réussies"] / \
                                                                    df["Passes réceptionnées par 90"]
    df["Pondération passes derniers tiers réussies"] = df["Passes dans tiers adverse réussies"] / df[
        "Passes réceptionnées par 90"]
    df["Pondération passes intelligentes réussies"] = df["Passes intelligentes réussies"] / df[
        "Passes réceptionnées par 90"]
    df["Pondération passes progressives réussies"] = df["Passes progressives réussies"] / df["Passes réceptionnées par 90"]
    df["Pondération passes dangereuses"] = df["Création d'occasion"] / df["Passes réceptionnées par 90"]
    df["Pondération passes quasi décisives par 90"] = df["Passes quasi décisives par 90"] / df[
        "Passes réceptionnées par 90"]
    df["Pondération secondes passes décisives par 90"] = df["Secondes passes décisives par 90"] / df[
        "Passes réceptionnées par 90"]
    df["Pondération troisièmes passes décisives par 90"] = df["Troisièmes passes décisives par 90"] / df[
        "Passes réceptionnées par 90"]

    df["Proportion passes en avant réussies"] = df["Passes en avant réussies"] / df["Passes réussies"]
    df["Proportion passes latérales réussies"] = df["Passes latérales réussies"] / df["Passes réussies"]
    df["Proportion passes arrières réussies"] = df["Passes arrières réussies"] / df["Passes réussies"]
    df["Proportion passes en profondeur réussies"] = df["Passes en profondeur réussies"] / df["Passes réussies"]
    df["Proportion passes vers la surface de réparation réussies"] = df["Passes vers la surface de réparation réussies"] / \
                                                                    df["Passes réussies"]
    df["Proportion passes derniers tiers réussies"] = df["Passes dans tiers adverse réussies"] / df["Passes réussies"]
    df["Proportion passes intelligentes réussies"] = df["Passes intelligentes réussies"] / df["Passes réussies"]
    df["Proportion passes progressives réussies"] = df["Passes progressives réussies"] / df["Passes réussies"]
    df["Proportion passes dangereuses"] = df["Création d'occasion"] / df["Passes par 90"]

    df["Fautes commises"] = -(df["Fautes par 90"])
    df["Cartons jaunes reçus"] = -(df["Cartons jaunes par 90"])
    df["Cartons rouges reçus"] = -(df["Cartons rouges par 90"])

    df["Valeur marchande"] = df["Valeur sur le marché  "]

    carac_list = [
        "Buts par 90",
        "Touches de balle par but",
        "G-xG",
        "xA par 90",
        "Touches de balle par passe décisive",
        "Duels défensifs gagnés PAdj",
        "Duels défensifs gagnés%",
        "Duels aériens gagnés",
        "Duels aériens gagnés%",
        "Tacles glissés PAdj",
        "Interceptions PAdj",
        "Tirs contrés PAdj",
        "Fautes commises",
        "Cartons jaunes reçus",
        "Passes réceptionnées par 90",
        "Attaques réussies",
        "Touches de balle dans la surface de réparation",
        "Dribbles réussis",
        "Dribbles réussis%",
        "Duels offensifs gagnés",
        "Duels offensifs gagnés%",
        "Accélérations réussies",
        "Courses progressives réussies",
        "Fautes subies",
        "Tirs cadrés",
        "Taux de conversion but/tir",
        "Passes réussies",
        "Passes réussies %",
        "Passes en avant réussies",
        "Passes en avant précises %",
        "Passes longues réussies",
        "Passes longues précises %",
        "Passes en profondeur réussies",
        "Passes en profondeur précises, %",
        "Passes vers la surface de réparation réussies",
        "Passes vers la surface de réparation précises, %",
        "Passes dans tiers adverse réussies",
        "Passes dans tiers adverse précises, %",
        "Centres réussis",
        "Сentres précises, %",
        "Centres dans la surface de but réussis",
        "Passes intelligentes réussies",
        "Passes intelligentes précises %",
        "Passes progressives réussies",
        "Passes progressives précises, %",
        "Passes quasi décisives par 90",
        "Secondes passes décisives par 90",
        "Troisièmes passes décisives par 90"
    ]

    cat_list = ['Joueur',
    'Équipe',
    'Équipe dans la période sélectionnée',
    'Place',
    'Âge', 
    'Doublon',
    'Team',
    'Valeur marchande']

    df_test = df[cat_list + carac_list]

    # Dictionnaire des postes pour filtrer
    postes = {
    "CF": r"\bCF\b",
    "LW": r"\b(LW|LWF|LAMF|RW|RWF|RAMF)\b",  # Filtrage des postes offensifs en attaque latérale
    "AMF": r"\b(AMF|LAMF|RAMF)\b",  # Filtrage des postes de milieu offensif
    "CMF": r"\b(CMF|LCMF|RCMF)\b",  # Filtrage des postes de milieu central
    "DMF": r"\b(DMF|LDMF|RDMF)\b",  # Filtrage des postes de milieu défensif
    "WB": r"\b(LWB|LB|RWB|RB)\b",  # Filtrage des postes de wingback
    "CB": r"\b(CB|LCB|RCB)\b",  # Filtrage des défenseurs centraux
}

    # Extraire le premier poste de chaque joueur
    df_test['Premier poste'] = df_test['Place'].apply(lambda x: x.split(',')[0].strip() if pd.notnull(x) else '')

    # Stocker les DataFrames filtrés par poste
    poste_dfs = {}

    for poste, regex in postes.items():
        # Filtrer les joueurs ayant le premier poste en question
        df_poste = df_test[df_test['Premier poste'].str.contains(regex, regex=True, na=False)]
        
        # Stocker le DataFrame pour ce poste
        poste_dfs[f"df_{poste.lower()}"] = df_poste


    # Stocker les DataFrames pour les z-scores normalisés et percentiles
    zscore_dfs = {}

    for poste, regex in postes.items():
        # Filtrer les joueurs ayant le poste en question
        df_poste = poste_dfs[f"df_{poste.lower()}"]
        
        # Calculer les z-scores pour les caractéristiques numériques spécifiées
        df_zscore = df_poste.copy()
        df_zscore[carac_list] = df_poste[carac_list].apply(lambda x: stats.zscore(x, nan_policy='omit'))
        
        # Normaliser les z-scores entre 0 et 100
        df_zscore[carac_list] = df_zscore[carac_list].apply(lambda x: 100 * (x - x.min()) / (x.max() - x.min()))
        
        # Stocker les DataFrames
        zscore_dfs[f"df_zscore_{poste.lower()}"] = df_zscore

    df_zscore_cf = zscore_dfs['df_zscore_cf']
    df_zscore_lw = zscore_dfs['df_zscore_lw']
    df_zscore_amf = zscore_dfs['df_zscore_amf']
    df_zscore_cmf = zscore_dfs['df_zscore_cmf']
    df_zscore_dmf = zscore_dfs['df_zscore_dmf']
    df_zscore_wb = zscore_dfs['df_zscore_wb']
    df_zscore_cb = zscore_dfs['df_zscore_cb']

    dfs = {
        'df_zscore_cf': df_zscore_cf,
        'df_zscore_lw': df_zscore_lw,
        'df_zscore_amf': df_zscore_amf,
        'df_zscore_cmf': df_zscore_cmf,
        'df_zscore_dmf': df_zscore_dmf,
        'df_zscore_wb': df_zscore_wb,
        'df_zscore_cb': df_zscore_cb,
    }

    # Parcourir chaque DataFrame et vérifier les doublons dans la colonne 'Doublon'
    for name, df in dfs.items():
        print(f"Vérification des doublons dans {name}...")
        
        # Vérifier s'il y a des doublons
        doublons = df[df.duplicated(subset=['Doublon'], keep=False)]
        
        if doublons.empty:
            print(f"Aucun doublon trouvé dans {name}.")
        else:
            print(f"Doublons trouvés dans {name}: {doublons['Doublon'].unique()}")
            
            # Supprimer les doublons, en gardant la première occurrence
            df_clean = df.drop_duplicates(subset=['Doublon'], keep='first')
            
            # Mettre à jour le DataFrame dans le dictionnaire avec les doublons supprimés
            dfs[name] = df_clean
            print(f"Doublons supprimés dans {name}.")

        # Remplacer les NaN par 0
        df = df.fillna(0)
        dfs[name] = df  # Mettre à jour le DataFrame dans le dictionnaire

        # Vérifier le nombre de NaN restants pour s'assurer que tous sont remplacés
        if df.isnull().sum().sum() == 0:
            print(f"Tous les NaN ont été remplacés par des 0 dans {name}.")
        else:
            print(f"Il reste des NaN non remplacés dans {name}.")

    # Réattribuer les DataFrames modifiés à leurs variables respectives
    df_zscore_cf = dfs['df_zscore_cf']
    df_zscore_lw = dfs['df_zscore_lw']
    df_zscore_amf = dfs['df_zscore_amf']
    df_zscore_cmf = dfs['df_zscore_cmf']
    df_zscore_dmf = dfs['df_zscore_dmf']
    df_zscore_wb = dfs['df_zscore_wb']
    df_zscore_cb = dfs['df_zscore_cb']

    # Créer un dictionnaire pour les rôles en fonction des postes
    roles_dict = {
        "Buteurs": ["Attaquant Complet", "Attaquant de Pressing", "Attaquant Pivot", "Renard des Surfaces"],
        "Ailiers": ["Meneur de Jeu Excentré", "Ailier Défensif", "Ailier Intérieur", "Ailier de Débordement"],
        "Milieux offensifs": ["Milieu Relayeur", "Meneur de Jeu"],
        "Milieux centraux": ["Milieu Relayeur", "Meneur de Jeu", "Milieu Sentinelle", "Milieu Récupérateur", "Milieu Box-to-Box"],
        "Milieux défensifs": ["Milieu Sentinelle", "Milieu Récupérateur", "Milieu Box-to-Box"],
        "Latéraux": ["Arrière Latéral", "Latéral Offensif"],
        "Défenseurs centraux": ["Défenseur Relanceur", "Défenseur Stoppeur"]
    }

    # Dictionnaire des DataFrames liés aux postes
    df_dict = {
        "Buteurs": df_zscore_cf,
        "Ailiers": df_zscore_lw,
        "Milieux offensifs": df_zscore_amf,
        "Milieux centraux": df_zscore_cmf,
        "Milieux défensifs": df_zscore_dmf,
        "Latéraux": df_zscore_wb,
        "Défenseurs centraux": df_zscore_cb
    }

    # Sélection du poste
    poste_selectionne = st.selectbox("Sélectionner un poste", list(df_dict.keys()))
    roles = roles_dict[poste_selectionne]

    # Obtenir le DataFrame correspondant au poste sélectionné
    df_poste = df_dict[poste_selectionne]
    joueurs_poste = df_poste['Doublon'].unique()

    # Extraire uniquement le nom du joueur avant le premier " - "
    joueurs_poste_noms = [joueur.split(' - ')[0] for joueur in joueurs_poste]
    
    # Sélectionner un joueur
    joueur_nom_selectionne = st.selectbox("Sélectionner un joueur", joueurs_poste_noms)

    # Trouver l'entrée complète correspondante (exemple : "H. Kane - Bayern - 531")
    joueur_selectionne = next(joueur for joueur in joueurs_poste if joueur.startswith(joueur_nom_selectionne))

    # Case à cocher pour les U23
    u23_selectionne = st.checkbox("U23")

    # Case à cocher pour le Top 5 européen
    top5_selectionne = st.checkbox("Top 5 européen")

    # Calculer la moyenne des scores pour les différents rôles liés au poste
    df_similarity = calculate_average_score_for_post(df_poste, carac_list, joueur_selectionne, roles, poste_selectionne)

    if df_similarity is not None:
        # Appliquer le filtre U23
        if u23_selectionne:
            df_similarity = df_similarity[df_similarity['Âge'] <= 23]

        # Appliquer le filtre Top 5 européen
        if top5_selectionne:
            top_5_ligues = ['Angleterre D1', 'Allemagne D1', 'Italie D1', 'Espagne D1', 'France D1']
            df_similarity = df_similarity[df_similarity['Team'].isin(top_5_ligues)]

        # Renommer les colonnes
        df_similarity = df_similarity.rename(columns={
            'Doublon': 'Joueur',
            'Team': 'Championnat',
            'Place': 'Postes',
            'Équipe dans la période sélectionnée': 'Équipe'
        })

        # Trier par score décroissant
        df_similarity = df_similarity.sort_values(by='Score', ascending=False)

        # Exclure le joueur étudié du DataFrame
        df_similarity = df_similarity[df_similarity['Joueur'] != joueur_nom_selectionne]

        # Afficher seulement les 20 premières lignes
        st.dataframe(df_similarity.head(20).reset_index(drop=True))

        excel_data = convert_df_to_excel(df_similarity)

        st.download_button(
            label="Télécharger les résultats en Excel",
            data=excel_data,
            file_name="df_similarity.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )



