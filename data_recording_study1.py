"""Exploitation des données de DataRecording.

Rappel sur le codage :
0 : erreur
1 : pas d'erreur
"""


import data_recording
import pandas as pd
from bm_u import title

DR = data_recording.DataRecorder(db_name="PRIVATE/result_exploitation.sqlite')

sql = "Select * from rep"
cursor = DR.con.execute(sql) # retourne un curseur

rows = cursor.fetchall()

DF = pd.DataFrame(rows, columns= [ item[0] for item in cursor.description ])

title("Nombre de dossiers globalement en ereur (1)")
print(DF.glob.value_counts())

for col in DF.columns:
    title("Occurences des valeurs pour la colonne'{}'".format(col) )
    # print(DF[[col]].value_counts())
    # DF[['id']] est une DataFrame
    # DF['id'] est une séries.
    print(pd.value_counts(DF[col].values,  sort = False).sort_index())



DF.to_excel('excel.xlsx', sheet_name='sortie') 
