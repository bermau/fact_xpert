#!/bin/env python3
"""Extraction des données venant de glimps.

données au format csv separé par des |"""

# exmeples de http://pandas.pydata.org/pandas-docs/stable/10min.html

import pandas as pd

import matplotlib.pyplot as plt 


from bm_u import title

# importer les données et renommer les colonnes
data = pd.read_csv('PRIVATE/extrait_mST69508_short.csv', sep='|',
                   encoding='ansi',
                   header=5)

title("Importation brute")
print(data.head(10))


data.columns = ['Prescripteur', 'Objet', 'Dossier',
                                     'CodeNABM', 'B', 'BHN', 'TB']

title("Après modif des noms de colonnes")
print(data.head(10))

title("fontion describe")
print(data.describe())

title("Trier selon une colonne")
print(data.sort_values(by = 'B'))


if __name__ == "__main__":
    pass
