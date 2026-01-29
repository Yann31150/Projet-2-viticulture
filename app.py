import streamlit as st
import pandas as pd
import requests
from PIL import Image
from io import BytesIO

st.set_page_config(page_title="BouteillIA", layout="wide")

# --- Fonctions utilitaires ---
def display_bio_badge():
    st.markdown('<span style="background-color: #4CAF50; color: white; padding: 5px 10px; border-radius: 15px;">Vin Bio</span>', unsafe_allow_html=True)

def load_image(url):
    try:
        if pd.isna(url) or url == 'nan':
            return None
        url = url.strip()
        if not url.startswith('http'):
            url = 'https://www.vinatis.com/' + url
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            return Image.open(BytesIO(response.content))
        else:
            st.error(f"Erreur HTTP {response.status_code} pour l'URL: {url}")
            return None
    except Exception as e:
        st.error(f"Erreur lors du chargement de l'image: {str(e)}")
        return None

# --- Chargement des données ---
@st.cache_data
def load_data():
    df = pd.read_csv('vins_vinatis_flat_complet.csv')
    df['bio'] = df['bio'].apply(lambda x: 1 if pd.notna(x) and 'Certifié Eurofeuille' in str(x) else 0)
    if 'visuel' not in df.columns:
        df['visuel'] = "https://www.vinatis.com/1-detail_default/default-wine.png"
    else:
        df['visuel'] = df['visuel'].apply(lambda x: f"https://www.vinatis.com/{x}" if pd.notna(x) and not str(x).startswith('http') else x)
    for col in df.columns:
        if col != 'prix':
            df[col] = df[col].astype(str)
    df['prix'] = pd.to_numeric(df['prix'], errors='coerce')
    return df

def display_wine_info(vin, show_recommendations=False):
    if pd.notna(vin['visuel']) and vin['visuel'] != 'nan':
        image = load_image(vin['visuel'])
        if image:
            st.image(image, width=200, caption=vin['nom'])
        else:
            st.warning("Impossible de charger l'image")
    else:
        st.warning("Pas d'image disponible pour ce vin")
    st.markdown(f"### {vin['nom']} - {vin['prix']}€")
    st.write(f"**Pays:** {vin['pays']}")
    st.write(f"**Région:** {vin['region']}")
    st.write(f"**Couleur:** {vin['couleur']}")
    st.write(f"**Degré d'alcool:** {vin['deg_alcool']}%")
    if vin['bio'] == '1':
        display_bio_badge()
    if pd.notna(vin['accords']) and vin['accords'] != 'nan':
        accords = vin['accords'].replace('[', '').replace(']', '').replace("'", '')
        st.write(f"**Accords mets et vins:** {accords}")
    if pd.notna(vin['desc']) and vin['desc'] != 'nan':
        st.write(f"**Description:** {vin['desc']}")
    if not show_recommendations:
        if st.button(f"Voir les recommandations pour {vin['nom']}", key=f"reco_{vin['nom']}"):
            st.session_state.selected_wine = vin
            st.session_state.show_recommendations = True
            st.rerun()

def display_recommendations(selected_wine):
    st.markdown("### 🍷 Vins recommandés")
    col1, col2 = st.columns(2)
    for i in range(1, 5):
        reco_col = 'reco' + str(i)
        if reco_col in df.columns and pd.notna(selected_wine[reco_col]):
            reco_wine = df[df['nom'] == selected_wine[reco_col]].iloc[0]
            with col1 if i % 2 == 1 else col2:
                st.markdown("---")
                display_wine_info(reco_wine, show_recommendations=True)
    if st.button("Retour aux résultats"):
        st.session_state.show_recommendations = False
        st.rerun()

df = load_data()

with st.sidebar:
    try:
        st.image("assets/logo_bouteillia.png", width=250)
    except Exception as e:
        st.warning(f"Logo non trouvé ou invalide : {e}")
    st.markdown("""
    ### 🍷 BouteillIA  
    _Le moteur intelligent de recommandation de vins._
    """)
    st.markdown("### Navigation")
    page = st.radio(
        label="",
        options=["🏠 Accueil", "🔍 Recherche", "📊 Résultats"],
        label_visibility="collapsed"
    )
    st.markdown("---")
    if st.button("🍇 Vin surprise"):
        st.session_state['random_wine'] = True
        random_wine = df.sample(n=1).iloc[0]
        st.session_state.selected_wine = random_wine
        st.session_state.show_recommendations = True
        st.session_state.page = "Résultats"
        st.rerun()
    st.caption('"Le vin est la réponse de la terre au soleil." — Marguerite Duras')

page = page.split(" ", 1)[1]

if page == "Accueil":
    st.markdown("""
    <h1 style='text-align: center;'>🍷 BouteillIA</h1>
    """, unsafe_allow_html=True)
    st.markdown("""
    <div style='text-align: center; font-size: 1.1em; margin-bottom: 2em;'>
    <b>Bienvenue sur BouteillIA 🍷🤖</b><br><br>
    Ce projet est né de la passion commune de Jean, Michel et Yann, trois apprenants en formation Data Analyst, unis par l'envie de mêler data science et plaisir œnologique.<br><br>
    Grâce à la puissance de l'intelligence artificielle, BouteillIA vous guide dans le monde complexe du vin pour vous aider à découvrir des bouteilles qui vous ressemblent.<br><br>
    Que vous soyez amateur curieux ou connaisseur averti, laissez-vous conseiller par notre moteur de recommandation intelligent.
    </div>
    """, unsafe_allow_html=True)
    st.write("""
    Découvrez notre sélection de vins soigneusement choisis. Utilisez la barre de navigation pour :
    - Explorer notre catalogue
    - Rechercher des vins selon vos critères
    - Voir les résultats de votre recherche
    """)
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Nombre de vins", len(df))
    with col2:
        st.metric("Pays représentés", len(df['pays'].unique()))

elif page == "Recherche":
    st.title("🍷 BouteillIA")
    st.header("Recherche de vins")
    col1, col2 = st.columns(2)
    with col1:
        pays_list = ["Tous"] + sorted([str(x) for x in df['pays'].dropna().unique()])
        couleur_list = ["Tous"] + sorted([str(x) for x in df['couleur'].dropna().unique()])
        nom_list = ["Tous"] + sorted([str(x) for x in df['nom'].dropna().unique()])
        recherche_nom = st.selectbox("Rechercher un vin par son nom", nom_list)
        pays = st.selectbox("Pays", pays_list)
        couleur = st.selectbox("Couleur du vin", couleur_list)
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
    if st.button("Rechercher"):
        resultats = df.copy()
        if recherche_nom != "Tous":
            resultats = resultats[resultats['nom'].astype(str) == recherche_nom]
        if pays != "Tous":
            resultats = resultats[resultats['pays'].astype(str) == pays]
        if couleur != "Tous":
            resultats = resultats[resultats['couleur'].astype(str) == couleur]
        if bio:
            resultats = resultats[resultats['bio'] == 1]
        resultats['prix'] = pd.to_numeric(resultats['prix'], errors='coerce')
        resultats = resultats[(resultats['prix'] >= prix_min) & (resultats['prix'] <= prix_max)]
        if selected_accords:
            mask = resultats['accords'].apply(lambda x: any(accord in str(x) for accord in selected_accords))
            resultats = resultats[mask]
        st.session_state.resultats = resultats
        st.session_state.page = "Résultats"
        st.rerun()

elif page == "Résultats":
    st.title("🍷 BouteillIA")
    st.header("Résultats de la recherche")
    if st.session_state.get("show_recommendations", False) and st.session_state.get("selected_wine", None) is not None:
        display_wine_info(st.session_state.selected_wine)
        display_recommendations(st.session_state.selected_wine)
    elif 'resultats' in st.session_state and not st.session_state.resultats.empty:
        resultats = st.session_state.resultats
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
