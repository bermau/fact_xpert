#!/bin/env python3
"""Extraction des données venant de glimps.

données au format csv separé par des |

Quelques références au livre suivant :
Analyse de données en Python/ Manipulation de données avec Pandas,
Numpy et IPython. Wes McKinney, Ed Eyrolles, 2015.

"""

# exemples de http://pandas.pydata.org/pandas-docs/stable/10min.html
# importer les données du csv
# exclure les données 

import pandas as pd
import numpy as np

from lib_bm_utils import title

# importer les données et renommer les colonnes
data = pd.read_csv('PRIVATE/extrait_mST69508_short.csv', sep='|',
                   # encoding='ansi',
                   encoding='ISO-8859-15',
                   header=5)

title("Importation brute")
print(data.head(10))


data.columns = ['Prescripteur', 'Objet', 'Dossier',
                                     'CodeNABM', 'B', 'BHN', 'TB']

title("Après modif des noms de colonnes")
print(data.head(10))

title("fontion describe")
print(data.describe())

title("Les lignes contenant Total sont à exlure. ")
print(data[data.Dossier=='Total'])
title("et retirer ces lignes")

EXCLURE = "Total"
# ci dessous noter l'usage de & et non pas de and.
data2 = data[(data.Dossier != EXCLURE) &
             (data.Prescripteur != EXCLURE) &
             (data.Objet != EXCLURE)]
print(data2)

title("Remplacer les tirets par des NaN")# cf. McKinney p. 156
# méthode avec query : data.query('line_race != 0').
data3= data2.replace('-', np.nan)
print(data3)

title("Trier selon une colonne")
print(data3.sort_values(by = 'B'))

DOSSIER = '17042664  18/04/2017'
title("Selectionner les données du dossier "+ DOSSIER)
print(data3[data3.Dossier==DOSSIER])

title("Aggréger les données pour les exporter")
grouped = data3.groupby(['Objet', 'Dossier'])
for cle,res in grouped:
    print("\ncle :", cle)
    print("\nData", res)
    # on accède aux données ainsi 
    for l in res.values:
        print(l)
        print(type(l))
        print(l[2])
    print(res.iat[1,3])


if __name__ == "__main__":
    pass
