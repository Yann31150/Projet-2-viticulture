import streamlit as st

# Configuration de la page
st.set_page_config(
    page_title="BouteillIA",
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

# Centrage de tout le contenu dans la colonne centrale
col1, col2, col3 = st.columns([1,2,1])
with col2:
    st.image("image.png", width=200)
    st.title("BouteillIA")
    st.subheader("Votre sommelier virtuel, Disponible 24H/24")
    st.markdown("""
    Bienvenue sur BouteillIA, votre assistant personnel pour découvrir et choisir les meilleurs vins.

    Utilisez notre moteur de recherche intelligent pour trouver le vin parfait selon vos goûts et vos préférences.
    """)

# Footer centré
st.markdown("---")
col1, col2, col3 = st.columns([1,2,1])
with col2:
    st.markdown("© 2024 - BouteillIA") 