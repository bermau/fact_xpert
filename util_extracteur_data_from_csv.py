#!/bin/env python3
"""Extraction des données venant de glimps.

données au format csv separé par des |

Quelques références au livre suivant :
Analyse de données en Python/ Manipulation de données avec Pandas,
Numpy et IPython. Wes McKinney, Ed Eyrolles, 2015.
"""

# exmeples de http://pandas.pydata.org/pandas-docs/stable/10min.html

import pandas as pd

import matplotlib.pyplot as plt 


from bm_u import title

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

title("Les lignes contenant Total")
print(data[data.Dossier=='Total'])
title("et retirer ces lignes")
data2 = data[data.Dossier != 'Total' and data.Prescripteur !="Total"]
# data2 = data[data.Dossier != 'Total' and data.Prescripteur !="Total"]

print(data2)



title("Remplacer les tirets par des Na")# cf. McKinney p. 156
# méthode avec query : data.query('line_race != 0').

title("Trier selon une colonne")
print(data2.sort_values(by = 'B'))




if __name__ == "__main__":
    pass
