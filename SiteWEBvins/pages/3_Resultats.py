import streamlit as st
import pandas as pd
import os

# Configuration de la page
st.set_page_config(
    page_title="Résultats de Recherche",
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
""", unsafe_allow_html=True)

st.title("Résultats de Recherche")

# Chargement des données
@st.cache_data
def load_wine_data():
    csv_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "venv", "vins_vinatis_flat_complet.csv")
    df = pd.read_csv(csv_path)
    # Conversion de la colonne features_vintage en nombres entiers
    df['features_vintage'] = pd.to_numeric(df['features_vintage'], errors='coerce')
    return df

# Chargement des données
wines_df = load_wine_data()

# Récupération des filtres
if 'filters' in st.session_state:
    filters = st.session_state['filters']
    
    # Application des filtres
    filtered_df = wines_df.copy()
    
    # Filtre par recherche textuelle
    if filters['search_query']:
        mask = filtered_df['name'].str.contains(filters['search_query'], case=False, na=False)
        filtered_df = filtered_df[mask]
    
    # Filtre par prix
    filtered_df = filtered_df[
        (filtered_df['prices_price'] >= filters['prix_min']) &
        (filtered_df['prices_price'] <= filters['prix_max'])
    ]
    
    # Filtre par type de vin
    if filters['type_vin'] != "Tous":
        filtered_df = filtered_df[filtered_df['features_type'] == filters['type_vin']]
    
    # Filtre par région
    if filters['region'] != "Toutes":
        filtered_df = filtered_df[filtered_df['features_region'] == filters['region']]
    
    # Filtre par cépages
    if filters['cepages']:
        mask = filtered_df['features_grape_variety'].apply(
            lambda x: any(cepage in str(x) for cepage in filters['cepages'])
        )
        filtered_df = filtered_df[mask]
    
    # Filtre par millésime
    filtered_df = filtered_df[
        (filtered_df['features_vintage'] >= filters['annee_min']) &
        (filtered_df['features_vintage'] <= filters['annee_max'])
    ]
    
    # Filtre par note
    if filters['note_min'] > 0:
        filtered_df = filtered_df[filtered_df['note_sur_20'] >= filters['note_min']]
    
    # Affichage des résultats
    st.write(f"Nombre de résultats : {len(filtered_df)}")
    
    # Affichage des vins
    for _, wine in filtered_df.iterrows():
        with st.container():
            col1, col2 = st.columns([1, 3])
            with col1:
                if pd.notna(wine['image']):
                    st.image(wine['image'], width=150)
            with col2:
                st.subheader(wine['name'])
                st.write(f"**Prix :** {wine['prices_price']}€")
                st.write(f"**Région :** {wine['features_region']}")
                st.write(f"**Type :** {wine['features_type']}")
                if pd.notna(wine['features_vintage']):
                    st.write(f"**Millésime :** {int(wine['features_vintage'])}")
                if pd.notna(wine['features_grape_variety']):
                    st.write(f"**Cépages :** {wine['features_grape_variety']}")
                if pd.notna(wine['description']):
                    st.write(f"**Description :** {wine['description']}")
            st.markdown("---")
else:
    st.warning("Veuillez effectuer une recherche sur la page de recherche.") 