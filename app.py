import streamlit as st
import base64

# Configuration de la page
st.set_page_config(
    page_title="Projet Viticulture",
    page_icon="🍷",
    layout="wide"
)

# Fonction pour charger et afficher une image en base64
def load_image(image_path):
    with open(image_path, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode()
    return f"data:image/png;base64,{encoded_string}"

# CSS personnalisé
st.markdown("""
<style>
    /* Couleurs inspirées du vin */
    :root {
        --wine-red: #722F37;
        --wine-burgundy: #4E1609;
        --wine-gold: #C1A87D;
        --wine-cream: #F2E8DC;
    }
    
    .sidebar .sidebar-content {
        background-color: var(--wine-burgundy);
        color: var(--wine-cream);
    }
    
    h1 {
        color: var(--wine-red);
        font-family: 'Playfair Display', serif;
    }
    
    .main-text {
        color: #333;
        font-size: 18px;
        line-height: 1.6;
        margin: 20px 0;
    }
    
    .logo-container {
        text-align: center;
        padding: 20px;
    }
</style>
""", unsafe_allow_html=True)

# Menu latéral
with st.sidebar:
    st.title("🍷 Navigation")
    page = st.radio(
        "Choisissez une page",
        ["Présentation et KPI", "Filtrage des vins", "Recommandation"]
    )

# Contenu principal de la page de présentation
if page == "Présentation et KPI":
    st.title("Bienvenue sur notre Projet Viticulture")
    
    # Emplacement pour le logo (à remplacer par votre propre logo)
    st.markdown("""
    <div class="logo-container">
        <img src="chemin_vers_votre_logo.png" alt="Logo Viticulture" style="max-width: 300px;">
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="main-text">
        <h2>Notre Projet</h2>
        <p>
        Bienvenue dans notre projet dédié à l'univers passionnant de la viticulture. 
        Notre équipe a développé une plateforme innovante combinant expertise viticole 
        et intelligence artificielle pour vous offrir une expérience unique de découverte 
        et de recommandation de vins.
        </p>
        
        <h2>Notre Équipe</h2>
        <p>
        Notre équipe est composée de passionnés de data science et d'œnologie, 
        réunissant leurs compétences pour créer un outil intelligent de recommandation 
        de vins. Nous utilisons des algorithmes de machine learning sophistiqués pour 
        analyser les caractéristiques des vins et proposer des recommandations personnalisées.
        </p>
        
        <h2>Fonctionnalités Principales</h2>
        <ul>
            <li>Exploration détaillée de notre base de données de vins</li>
            <li>Système de filtrage avancé</li>
            <li>Recommandations personnalisées basées sur l'intelligence artificielle</li>
            <li>Visualisation interactive des données</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

elif page == "Filtrage des vins":
    st.title("Filtrage des vins")
    st.write("Cette section est en cours de développement...")

elif page == "Recommandation":
    st.title("Système de recommandation")
    st.write("Cette section est en cours de développement...") 