import os
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd

DATASET_PATH = './'
styles = pd.read_csv(os.path.join(DATASET_PATH, "styles.csv"), error_bad_lines=False)

# Sélectionner les colonnes souhaitées
colonnes_voulues = ['gender', 'articleType']
df_filtre = styles[colonnes_voulues]

# Filtrer les lignes selon une colonne particulière (ici "gender")
df_filtre = df_filtre[df_filtre['gender'] == 'Men']

# Compter le nombre d'occurrences de chaque articleType pour les articles masculins
comptes = df_filtre['articleType'].value_counts()

colors = sns.color_palette('bright')

# Filtrer les comptes pour n'afficher que les pourcentages plus de 5%
comptes = comptes[comptes/comptes.sum() * 100 > 5]

plt.pie(comptes, labels=comptes.index, colors=colors, autopct='%0.0f%%')
plt.legend(loc='right', bbox_to_anchor=(1.25, 0.5), labelspacing=1.5)
plt.title("La répartition des vêtements pour Homme")

sns.catplot( x='masterCategory', y='gender', data=styles, hue='season')
plt.show()