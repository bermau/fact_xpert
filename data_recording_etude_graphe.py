"""Exploitation des données de DataRecording.

Rappel sur le codage :
0 : erreur
1 : pas d'erreur
"""

import conf_file
import data_recording
import pandas as pd
from bm_u import title

DR = data_recording.DataRecorder(db_name="PRIVATE/result.sqlite")
# DR = data_recording.DataRecorder(db_name="PRIVATE/result_expl.sqlite")

sql = "Select * from rep"
cursor = DR.con.execute(sql) # retourne un curseur

rows = cursor.fetchall()

DF = pd.DataFrame(rows, columns= [ item[0] for item in cursor.description ])

title("Nombre de dossiers globalement en ereur (1)")
print(DF.glob.value_counts())

lst_col = list(DF.columns.values)
lst_col.remove('id')
lst_col.remove('sum')



for col in DF.columns:
    title("Occurences des valeurs pour la colonne'{}'".format(col) )
    # print(DF[[col]].value_counts())
    # DF[['id']] est une DataFrame
    # DF['id'] est une séries.
    print(pd.value_counts(DF[col].values,  sort = False).sort_index())






# DF.to_excel('excel.xlsx', sheet_name=conf_file.EXPORT_REP+'/'+'sortie')
np_patients, nb_cols = DF.shape

# récup des données pour numpy
DF2= DF.copy()
lst_col2=list(DF2.columns)
lst_col2.remove('id')
lst_col2.remove('cle')
lst_col2.remove('date')

num_data = DF2.loc[:,lst_col2]
title("Données retenues")
print(num_data.shape)


# Graphique
# from matplotlib import pyplot as plt
import numpy as np
import matplotlib.pyplot as plt

fig, ax = plt.subplots()


image =np.array(num_data)
# passer le np.array en floattant
image2 = image.astype(np.float)
# progrès : DF.iloc[:, 2:]
# gray_r is for grey reverse
ax.imshow(image2, cmap=plt.cm.gray_r, interpolation='nearest')
ax.set_title('Erreurs de facturation')

ax.set_xlabel("Type d'erreur")
ax.set_ylabel("Cas")

# imposer des étiquettes d'axes
# yticks() retourne 2 listes : positions et labels.
# labs =['un', '','','','hibou','','labo']
# plt.yticks(plt.yticks()[0],labs)

# labs quelcoqnues :
if 0:
    labs = ["*"+str(item) for item in range(np_patients + 2) ]
if 1:
    labs = [ "" ]
    labs.extend(DF['id'].values)
    labs.extend('')
if 0:
    labs = [ "" ]
    labs.extend(DF['cle'].values)
    labs.extend('')    

plt.yticks(plt.yticks()[0],labs)

# idem pour les x_ticks :
if 1:
    xlabs = [ "" ]
    xlabs.extend(DF2.columns)
    xlabs.extend('')
    
plt.xticks(plt.xticks()[0],xlabs)

locs, labs= plt.yticks()
# on peut voir les étiquettes
print(locs)
print(labs)
for i, item in enumerate(labs):
    print(i, item)



    
# décaler légèreemnt les axes.
# Move left and bottom spines outward by 10 points
ax.spines['left'].set_position(('outward', 10))
ax.spines['bottom'].set_position(('outward', 10))

# Hide the right and top spines
# ax.spines['right'].set_visible(True)
#  ax.spines['top'].set_visible(False)
# Only show ticks on the left and bottom spines

ax.yaxis.set_ticks_position('left')
ax.xaxis.set_ticks_position('bottom')

plt.show()



