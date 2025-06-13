import pandas as pd

# Chargement du fichier CSV
df = pd.read_csv("vinatis_data.csv")

# Ajout du préfixe à la colonne 'image'
df['image_url'] = "https://www.vinatis.com/" + df['image'].astype(str)

# Affichage des 5 premières URLs générées
print(df[['image', 'image_url']].head())

# Optionnel : sauvegarde dans un nouveau CSV
# df.to_csv("vinatis_data_with_image_urls.csv", index=False)