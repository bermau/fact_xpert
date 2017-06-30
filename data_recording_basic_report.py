"""Exploitation des données de DataRecording.

Rappel sur le codage :
0 : erreur
1 : pas d'erreur
"""

import conf_file
import data_recording
import pandas as pd
from bm_u import title

def report():
        
    DR = data_recording.DataRecorder(db_name="PRIVATE/result.sqlite")

    sql = "Select * from rep"
    cursor = DR.con.execute(sql) # retourne un curseur

    rows = cursor.fetchall()

    DF = pd.DataFrame(rows, columns= [ item[0] for item in cursor.description ])

    title("Nombre de dossiers globalement en erreur")
    print(DF.glob.value_counts())

    lst_col = list(DF.columns.values)
    lst_col.remove('id')
    lst_col.remove('cle')
    lst_col.remove('sum')
    lst_col.remove('date')


    for col in lst_col:
        title("Occurences des valeurs pour la colonne'{}'".format(col) )
        # print(DF[[col]].value_counts())
        # DF[['id']] est une DataFrame
        # DF['id'] est une séries.
        print(pd.value_counts(DF[col].values,  sort = False).sort_index())

if __name__ == '__main__':
    report()



