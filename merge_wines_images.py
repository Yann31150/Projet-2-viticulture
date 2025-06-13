import pandas as pd

# Lecture des fichiers CSV
print("Lecture des fichiers CSV...")
wines_df = pd.read_csv('vins_vinatis_150_pages.csv')
images_df = pd.read_csv('vinatis_images_accessibles.csv')

# Affichage des informations sur les données
print("\nInformations sur les données :")
print(f"Nombre de vins dans le fichier principal : {len(wines_df)}")
print(f"Nombre d'images disponibles : {len(images_df)}")

# Fusion des données sur l'ID
print("\nFusion des données...")
merged_df = pd.merge(wines_df, images_df[['id', 'image_url']], on='id', how='left')

# Statistiques sur la fusion
total_wines = len(merged_df)
wines_with_images = merged_df['image_url'].notna().sum()
print(f"\nRésultats de la fusion :")
print(f"Nombre total de vins : {total_wines}")
print(f"Nombre de vins avec images : {wines_with_images}")
print(f"Pourcentage de vins avec images : {(wines_with_images/total_wines)*100:.2f}%")

# Sauvegarde du fichier fusionné
output_file = 'vins_vinatis_complet.csv'
merged_df.to_csv(output_file, index=False)
print(f"\nFichier fusionné sauvegardé sous : {output_file}")

# Affichage d'un exemple
print("\nExemple de données fusionnées :")
print(merged_df[['id', 'name', 'image_url']].head()) 