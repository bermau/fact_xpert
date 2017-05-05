#!/bin/env python3
"""Extraction des données venant de glimps.

données au format csv separé par des |"""

 
import pandas as pd



data = pd.read_csv('PRIVATE/extrait_mST69508_short.csv', sep='|',
                   encoding='ansi',
                   header=5)

print(data.head(10))

if __name__ == "__main__":
    pass
