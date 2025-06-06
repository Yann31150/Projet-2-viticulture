# Application de Recherche de Vins

Une application web interactive permettant de rechercher et découvrir des vins, avec des fonctionnalités de recommandation.

## Fonctionnalités

- Recherche de vins par nom, pays, région, couleur
- Filtrage par prix
- Affichage des informations détaillées des vins
- Recommandations de vins similaires
- Interface utilisateur intuitive

## Installation

1. Cloner le dépôt :
```bash
git clone [URL_DU_REPO]
cd [NOM_DU_REPO]
```

2. Créer un environnement virtuel et l'activer :
```bash
python -m venv venv
source venv/bin/activate  # Sur Unix/macOS
# ou
venv\Scripts\activate  # Sur Windows
```

3. Installer les dépendances :
```bash
pip install -r requirements.txt
```

4. Lancer l'application :
```bash
streamlit run app.py
```

## Dépendances

- Python 3.x
- Streamlit
- Pandas
- NumPy
- Pillow
- Requests

## Structure du Projet

- `app.py` : Application principale
- `base_vin_final.csv` : Base de données des vins
- `requirements.txt` : Liste des dépendances
- `README.md` : Documentation du projet

## Utilisation

1. Lancez l'application avec `streamlit run app.py`
2. Accédez à l'interface web via votre navigateur
3. Utilisez les filtres pour rechercher des vins
4. Cliquez sur un vin pour voir ses détails
5. Explorez les recommandations de vins similaires 