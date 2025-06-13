<<<<<<< HEAD
import pandas as pd
import numpy as np

def load_data():
    """Charge les données depuis le fichier CSV."""
    try:
        df = pd.read_csv('base_vin_final.csv')
        print(f"Données chargées avec succès. Shape: {df.shape}")
        print("\nAperçu des colonnes:")
        print(df.columns.tolist())
        print("\nAperçu des données:")
        print(df.head())
        return df
    except Exception as e:
        print(f"Erreur lors du chargement des données: {e}")
        return None

if __name__ == "__main__":
    df = load_data() 
=======
from scraper import scrape_vinatis
import pandas as pd
import time

# Liste pour stocker les dataframes de chaque page
dfs = []

# Nombre total de pages à scraper
TOTAL_PAGES = 145

# Scraper toutes les pages
for page in range(1, TOTAL_PAGES + 1):
    try:
        print(f"Scraping page {page}/{TOTAL_PAGES} ({(page/TOTAL_PAGES)*100:.1f}%)...")
        df = scrape_vinatis(page)
        dfs.append(df)
        # Ajouter un délai de 1 seconde entre chaque requête pour éviter de surcharger le serveur
        time.sleep(1)
    except Exception as e:
        print(f"Erreur lors du scraping de la page {page}: {str(e)}")
        continue

# Combiner tous les dataframes
final_df = pd.concat(dfs, ignore_index=True)

# Sauvegarder dans un fichier CSV
final_df.to_csv('vinatis_data.csv', index=False)
print(f"Données sauvegardées dans vinatis_data.csv - {len(final_df)} vins au total") 
>>>>>>> 52c8fa171986a345393bbb19d7d49ad5a4870e4a
