import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Configuration de la page
st.set_page_config(layout="wide", page_title="Analyse des Vins")

# Ajout du CSS personnalisé
st.markdown("""
    <style>
    .main-container {
        padding: 2rem;
        background-color: #f8f9fa;
        border-radius: 10px;
        margin: 1rem 0;
    }
    
    .logo-container {
        text-align: center;
        padding: 2rem;
    }
    
    .team-container {
        background-color: white;
        padding: 2rem;
        border-radius: 10px;
        margin: 1rem 0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    
    .kpi-container {
        background-color: white;
        padding: 2rem;
        border-radius: 10px;
        margin: 1rem 0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    </style>
""", unsafe_allow_html=True)

# Création de la barre latérale
with st.sidebar:
    st.title("Navigation")
    selected = st.radio(
        "Choisissez une section",
        ["Accueil", "Notre équipe", "Analyse des données"]
    )

# Contenu principal
st.title("🍷 Analyse du Marché Viticole")

# Logo (fictif)
st.markdown("""
    <div class='logo-container'>
        <img src="https://via.placeholder.com/200x200.png?text=Logo+Vin" alt="Logo"/>
    </div>
""", unsafe_allow_html=True)

# Présentation de l'équipe
st.markdown("<div class='team-container'>", unsafe_allow_html=True)
st.header("Notre Équipe")
st.write("""
Notre équipe passionnée de data scientists est dédiée à l'analyse du marché viticole. 
Nous combinons expertise en science des données et connaissance approfondie du monde du vin 
pour vous offrir des insights précieux.

* **Marie Dupont** - Data Scientist, experte en ML
* **Jean Martin** - Analyste de données, spécialiste en visualisation
* **Sophie Bernard** - Œnologue et Data Analyst
""")
st.markdown("</div>", unsafe_allow_html=True)

# Section KPI
st.markdown("<div class='kpi-container'>", unsafe_allow_html=True)
st.header("Indicateurs Clés de Performance")

# Mise en page en colonnes pour les KPI
col1, col2, col3 = st.columns(3)

with col1:
    st.metric(label="Note Moyenne", value="88/100", delta="2.3")
    
    # Graphique fictif 1
    fig1 = go.Figure(data=[go.Pie(labels=['Rouge', 'Blanc', 'Rosé'], 
                                 values=[45, 35, 20],
                                 hole=.3)])
    fig1.update_layout(title="Distribution des Types de Vins")
    st.plotly_chart(fig1, use_container_width=True)

with col2:
    st.metric(label="Prix Moyen", value="42.5 €", delta="-1.2")
    
    # Graphique fictif 2
    data = {'Région': ['Bordeaux', 'Bourgogne', 'Loire', 'Rhône'],
            'Notes': [87, 89, 86, 88]}
    fig2 = px.bar(data, x='Région', y='Notes', title="Notes Moyennes par Région")
    st.plotly_chart(fig2, use_container_width=True)

with col3:
    st.metric(label="Nombre de Vins", value="1,245", delta="12%")
    
    # Graphique fictif 3
    années = list(range(2015, 2023))
    prix = [35, 37, 40, 41, 43, 45, 44, 42.5]
    fig3 = px.line(x=années, y=prix, title="Évolution du Prix Moyen")
    fig3.update_layout(xaxis_title="Année", yaxis_title="Prix Moyen (€)")
    st.plotly_chart(fig3, use_container_width=True)

st.markdown("</div>", unsafe_allow_html=True) 