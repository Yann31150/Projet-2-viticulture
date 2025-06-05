import streamlit as st
import pandas as pd
import numpy as np
import os

# Configuration de la page
st.set_page_config(
    page_title="Recherche de Vins",
    page_icon="🍷",
    layout="wide"
)

# Ajout du style CSS pour le fond bordeaux clair et la sidebar plus foncée
st.markdown("""
    <style>
        .stApp {
            background-color: #E6D5D0;
        }
        [data-testid="stSidebar"] {
            background-color: #D4B5B0;
        }
    </style>
        .stApp::before {
            content: "";
            position: fixed;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            width: 500px;
            height: 500px;
            background-image: url('image.png');
            background-size: contain;
            background-repeat: no-repeat;
            background-position: center;
            opacity: 0.1;
            z-index: -1;
        }
    </style>
""", unsafe_allow_html=True)

st.title("Recherche de Vins")

# Chargement des données
@st.cache_data
def load_wine_data():
    # Chemin vers le fichier CSV
    csv_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "venv", "vins_vinatis_flat_complet.csv")
    df = pd.read_csv(csv_path)
    return df

# Chargement des données
wines_df = load_wine_data()

# Barre de recherche
search_query = st.text_input("🔍 Rechercher un vin", placeholder="Entrez le nom d'un vin, un cépage, une région...")

st.header("Critères de sélection")

# Prix
prix_min, prix_max = st.slider(
    "Prix (€)",
    min_value=float(wines_df["prices_price"].min()),
    max_value=float(wines_df["prices_price"].max()),
    value=(float(wines_df["prices_price"].min()), float(wines_df["prices_price"].max())),
    step=5.0
)

# Type de vin
types_vin = wines_df["features_type"].dropna().unique()
type_vin = st.selectbox(
    "Type de vin",
    ["Tous"] + sorted(list(types_vin))
)

# Région
regions = wines_df["features_region"].dropna().unique()
region = st.selectbox(
    "Région",
    ["Toutes"] + sorted(list(regions))
)

# Cépages
cepages = wines_df["features_grape_variety"].dropna().unique()
cepages_list = []
for cepage in cepages:
    if isinstance(cepage, str) and cepage.startswith('['):
        # Convertir la chaîne en liste
        cepage_list = eval(cepage)
        cepages_list.extend(cepage_list)
    else:
        cepages_list.append(cepage)

cepages_list = sorted(list(set(cepages_list)))
selected_cepages = st.multiselect(
    "Cépages",
    cepages_list
)

# Vin bio
bio = st.checkbox("Vin bio uniquement")

st.header("Filtres supplémentaires")

# Millésime
vintages = wines_df["features_vintage"].dropna().unique()
vintages = sorted([int(v) for v in vintages if str(v).isdigit()], reverse=True)
annee = st.select_slider(
    "Millésime",
    options=vintages,
    value=(min(vintages), max(vintages))
)

# Note minimum
note_min = st.slider(
    "Note minimum",
    min_value=0.0,
    max_value=20.0,
    value=0.0,
    step=0.5
)

# Accords mets et vins
accords = st.multiselect(
    "Accords mets et vins",
    ["Viande rouge", "Viande blanche", "Poisson", "Fruits de mer", 
     "Fromage", "Dessert", "Apéritif"]
)

# Stockage des filtres dans la session
st.session_state['filters'] = {
    'search_query': search_query,
    'prix_min': prix_min,
    'prix_max': prix_max,
    'type_vin': type_vin,
    'region': region,
    'cepages': selected_cepages,
    'bio': bio,
    'annee_min': annee[0],
    'annee_max': annee[1],
    'note_min': note_min,
    'accords': accords
} 