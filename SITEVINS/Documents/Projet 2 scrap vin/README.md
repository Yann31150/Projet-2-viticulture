# Wine Scraper

Ce projet contient des scripts Python pour scraper les données de vins depuis différents sites web.

## Sites supportés

- Wineandco
- Vinatis
- Vinmalin
- Viniphile

## Installation

1. Cloner le repository :
```bash
git clone [URL_DU_REPO]
cd [NOM_DU_REPO]
```

2. Installer les dépendances :
```bash
pip install -r requirements.txt
```

## Utilisation

Chaque script peut être exécuté indépendamment :

```bash
python scrape_wineandco.py
python scrape_vinatis.py
python scrape_vinmalin.py
python scrape_viniphile.py
```

Les données sont exportées au format CSV.

## Structure des données

Les scripts extraient les informations suivantes pour chaque vin :
- Nom
- Prix
- Appellation
- Cépage
- Millésime
- Région
- Pays
- Description
- Image
- URL

## Dépendances

- Selenium
- Pandas
- Webdriver Manager
- Chrome WebDriver

## Note

Ce projet est à des fins éducatives uniquement. Assurez-vous de respecter les conditions d'utilisation des sites web cibles. 