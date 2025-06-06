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