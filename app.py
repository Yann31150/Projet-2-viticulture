import streamlit as st
import pandas as pd
import requests
from PIL import Image
from io import BytesIO

# =============================================
# Configuration de base
# =============================================
st.set_page_config(page_title="BouteillIA", layout="wide")

# =============================================
# Fonctions utilitaires
# =============================================
def display_bio_badge():
    """Affiche le badge bio"""
    st.markdown('<span style="background-color: #4CAF50; color: white; padding: 5px 10px; border-radius: 15px;">Vin Bio</span>', unsafe_allow_html=True)

def load_image(url):
    """Charge une image depuis une URL"""
    try:
        if pd.isna(url) or url == 'nan':
            return None
            
        # Nettoyer l'URL
        url = url.strip()
        if not url.startswith('http'):
            url = 'https://www.vinatis.com/' + url
            
        # Télécharger l'image
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            return Image.open(BytesIO(response.content))
        else:
            st.error(f"Erreur HTTP {response.status_code} pour l'URL: {url}")
            return None
    except Exception as e:
        st.error(f"Erreur lors du chargement de l'image: {str(e)}")
        return None

# =============================================
# Chargement des données
# =============================================
@st.cache_data
def load_data():
    """Charge les données des vins"""
    df = pd.read_csv('base_vin_final.csv')
    df['bio'] = df['bio'].apply(lambda x: 1 if pd.notna(x) and 'Certifié Eurofeuille' in str(x) else 0)
    
    # Si la colonne visuel n'existe pas, on la crée avec une image par défaut
    if 'visuel' not in df.columns:
        df['visuel'] = "https://www.vinatis.com/1-detail_default/default-wine.png"
    else:
        # Corriger le format des URLs des images
        df['visuel'] = df['visuel'].apply(lambda x: f"https://www.vinatis.com/{x}" if pd.notna(x) and not str(x).startswith('http') else x)
    
    # Convertir toutes les colonnes en string sauf prix
    for col in df.columns:
        if col != 'prix':  # Ne pas convertir la colonne prix
            df[col] = df[col].astype(str)
    
    # S'assurer que la colonne prix est en float
    df['prix'] = pd.to_numeric(df['prix'], errors='coerce')
    
    return df

# =============================================
# Interface utilisateur
# =============================================
def display_wine_info(vin, show_recommendations=False):
    """Affiche les informations d'un vin"""
    # Affichage de l'image
    if pd.notna(vin['visuel']) and vin['visuel'] != 'nan':
        image = load_image(vin['visuel'])
        if image:
            st.image(image, width=300, caption=vin['nom'])
        else:
            st.warning("Impossible de charger l'image")
    else:
        st.warning("Pas d'image disponible pour ce vin")
    
    # Informations du vin
    st.markdown(f"### {vin['nom']} - {vin['prix']}€")
    st.write(f"**Pays:** {vin['pays']}")
    st.write(f"**Région:** {vin['region']}")
    st.write(f"**Couleur:** {vin['couleur']}")
    st.write(f"**Degré d'alcool:** {vin['deg_alcool']}%")
    
    # Badge bio si applicable
    if vin['bio'] == '1':
        display_bio_badge()
    
    # Accords mets et vins
    if pd.notna(vin['accords']) and vin['accords'] != 'nan':
        accords = vin['accords'].replace('[', '').replace(']', '').replace("'", '')
        st.write(f"**Accords mets et vins:** {accords}")
    
    # Description
    if pd.notna(vin['desc']) and vin['desc'] != 'nan':
        st.write(f"**Description:** {vin['desc']}")
    
    # Bouton pour afficher les recommandations
    if not show_recommendations:
        if st.button(f"Voir les recommandations pour {vin['nom']}", key=f"reco_{vin['nom']}"):
            st.session_state.selected_wine = vin
            st.session_state.show_recommendations = True
            st.rerun()

def display_recommendations(selected_wine):
    """Affiche les vins recommandés"""
    st.markdown("### 🍷 Vins recommandés")
    
    # Créer une grille de 2 colonnes pour les recommandations
    col1, col2 = st.columns(2)
    
    # Afficher les 4 vins recommandés
    for i in range(1, 5):
        reco_col = 'reco' + str(i)
        if reco_col in df.columns and pd.notna(selected_wine[reco_col]):
            # Trouver le vin recommandé dans le DataFrame
            reco_wine = df[df['nom'] == selected_wine[reco_col]].iloc[0]
            
            # Alterner entre les colonnes
            with col1 if i % 2 == 1 else col2:
                st.markdown("---")
                display_wine_info(reco_wine, show_recommendations=True)
    
    # Bouton pour revenir aux résultats
    if st.button("Retour aux résultats"):
        st.session_state.show_recommendations = False
        st.rerun()

# =============================================
# Chargement des données
# =============================================
df = load_data()

# =============================================
# Navigation et pages
# =============================================
st.sidebar.title("BouteillIA")
page = st.sidebar.radio("Navigation", ["Accueil", "Recherche", "Résultats"])
st.session_state.page = page

# Page d'accueil
if page == "Accueil":
    st.title("🍷 BouteillIA")
    st.subheader("Bienvenue")
    
    st.write("""
    Découvrez notre sélection de vins soigneusement choisis. Utilisez la barre de navigation pour :
    
    - Explorer notre catalogue
    - Rechercher des vins selon vos critères
    - Voir les résultats de votre recherche
    """)
    
    # Statistiques
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Nombre de vins", len(df))
    with col2:
        st.metric("Pays représentés", len(df['pays'].unique()))

# Page de recherche
elif page == "Recherche":
    st.title("🍷 BouteillIA")
    st.header("Recherche de vins")
    
    # Filtres de recherche
    col1, col2 = st.columns(2)
    
    with col1:
        # Nettoyer et trier les listes en gérant les NaN
        pays_list = ["Tous"] + sorted([str(x) for x in df['pays'].dropna().unique()])
        couleur_list = ["Tous"] + sorted([str(x) for x in df['couleur'].dropna().unique()])
        nom_list = ["Tous"] + sorted([str(x) for x in df['nom'].dropna().unique()])
        
        recherche_nom = st.selectbox("Rechercher un vin par son nom", nom_list)
        pays = st.selectbox("Pays", pays_list)
        couleur = st.selectbox("Couleur du vin", couleur_list)
        
        # Accords mets et vins
        all_accords = []
        for accords in df['accords'].dropna():
            accords_list = accords.replace('[', '').replace(']', '').replace("'", '').split(', ')
            all_accords.extend(accords_list)
        
        selected_accords = st.multiselect(
            "Accords mets et vins",
            options=sorted(list(set(all_accords))),
            help="Sélectionnez un ou plusieurs accords mets et vins"
        )
        
        bio = st.checkbox("Vins bio uniquement")
    
    # Slider de prix en pleine largeur
    prix_min = float(df['prix'].min())
    prix_max = float(df['prix'].max())
    prix_range = st.slider(
        "Prix (€)",
        min_value=prix_min,
        max_value=prix_max,
        value=(prix_min, prix_max),
        step=1.0,
        help="Sélectionnez une fourchette de prix"
    )
    prix_min, prix_max = prix_range
    
    # Recherche
    if st.button("Rechercher"):
        resultats = df.copy()
        
        # Application des filtres
        if recherche_nom != "Tous":
            resultats = resultats[resultats['nom'].astype(str) == recherche_nom]
        if pays != "Tous":
            resultats = resultats[resultats['pays'].astype(str) == pays]
        if couleur != "Tous":
            resultats = resultats[resultats['couleur'].astype(str) == couleur]
        if bio:
            resultats = resultats[resultats['bio'] == 1]
        resultats = resultats[(resultats['prix'] >= prix_min) & (resultats['prix'] <= prix_max)]
        
        if selected_accords:
            mask = resultats['accords'].apply(lambda x: any(accord in str(x) for accord in selected_accords))
            resultats = resultats[mask]
        
        st.session_state.resultats = resultats
        st.session_state.page = "Résultats"
        st.rerun()

# Page des résultats
elif page == "Résultats":
    st.title("🍷 BouteillIA")
    st.header("Résultats de la recherche")
    
    if 'resultats' in st.session_state and not st.session_state.resultats.empty:
        resultats = st.session_state.resultats
        
        # Vérifier si on doit afficher les recommandations
        if 'show_recommendations' in st.session_state and st.session_state.show_recommendations:
            display_recommendations(st.session_state.selected_wine)
        else:
            st.write(f"Nombre de vins trouvés : {len(resultats)}")
            
            for _, vin in resultats.iterrows():
                st.markdown("---")
                display_wine_info(vin)
    else:
        st.info("Aucun résultat à afficher. Veuillez effectuer une recherche.")
        if st.button("Retour à la recherche"):
            st.session_state.page = "Recherche"
            st.rerun()