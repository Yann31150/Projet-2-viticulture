import requests
from bs4 import BeautifulSoup
import re
import json
import pandas as pd
from tqdm import tqdm
import time

# Fonction pour scraper une page et retourner un DataFrame des vins
def scrape_vinatis(page: int):
    url = f"https://www.vinatis.com/achat-vin?page={page}"
    vin = requests.get(url).text
    soup = BeautifulSoup(vin, "html.parser")
    scripts = soup.find_all("script")
    for script in scripts:
        if script.string and "product_elastic" in script.string:
            match = re.search(r"var\s+product_elastic\s*=\s*({.*?});", script.string, re.DOTALL)
            if match:
                data = json.loads(match.group(1))
                df = pd.DataFrame(data["products"])
                return df
    return pd.DataFrame()

# Boucle sur toutes les pages et collecte les infos
all_wines = []
N_PAGES = 150
for page in tqdm(range(1, N_PAGES+1), desc="Scraping pages Vinatis"):
    df = scrape_vinatis(page)
    if not df.empty:
        all_wines.append(df)
    time.sleep(1)  # Pour ne pas surcharger le serveur

# Fusionner tous les DataFrames
if all_wines:
    wines_df = pd.concat(all_wines, ignore_index=True)
else:
    wines_df = pd.DataFrame()

# Extraction des URLs d'images accessibles
if not wines_df.empty:
    # On suppose que la colonne 'id' contient l'ID du vin
    if 'id' in wines_df.columns:
        wines_df['image_url'] = wines_df.apply(lambda row: f"https://www.vinatis.com/{row['id']}-detail_default/{row['name'].lower().replace(' ', '-')}.png", axis=1)
    else:
        # Recherche d'une colonne contenant 'id' dans le nom
        id_col = [col for col in wines_df.columns if 'id' in col]
        if id_col:
            wines_df['image_url'] = wines_df.apply(lambda row: f"https://www.vinatis.com/{row[id_col[0]]}-detail_default/{row['name'].lower().replace(' ', '-')}.png", axis=1)
        else:
            wines_df['image_url'] = None
    # On garde les colonnes principales
    out_df = wines_df[['id', 'name', 'image_url']].dropna(subset=['image_url'])
    out_df.to_csv('vinatis_images_accessibles.csv', index=False)
    print(f"{len(out_df)} images accessibles trouvées. Exemple :")
    print(out_df.head())
else:
    print("Aucun vin trouvé.") 