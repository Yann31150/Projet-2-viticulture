<<<<<<< HEAD
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
=======
# Wine Scraper

Ce projet contient des scripts Python pour scraper les données de vins depuis Vinatis et nettoyer les données.

## Sites supportés

- Vinatis

## Installation

1. Cloner le repository :
>>>>>>> 52c8fa171986a345393bbb19d7d49ad5a4870e4a
```bash
git clone [URL_DU_REPO]
cd [NOM_DU_REPO]
```

<<<<<<< HEAD
2. Créer un environnement virtuel et l'activer :
```bash
python -m venv venv
source venv/bin/activate  # Sur Unix/macOS
# ou
venv\Scripts\activate  # Sur Windows
```

3. Installer les dépendances :
=======
2. Installer les dépendances :
>>>>>>> 52c8fa171986a345393bbb19d7d49ad5a4870e4a
```bash
pip install -r requirements.txt
```

<<<<<<< HEAD
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
=======
## Utilisation

Chaque script peut être exécuté indépendamment :

```bash
python scrape_vinatis.py

```

Les données sont exportées au format CSV.

## Structure des données

Les scripts extraient les informations suivantes pour chaque vin :


## Dépendances

## Note

Ce projet est à des fins éducatives uniquement. Assurez-vous de respecter les conditions d'utilisation des sites web cibles. 
>>>>>>> 52c8fa171986a345393bbb19d7d49ad5a4870e4a
