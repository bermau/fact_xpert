"""Exploitation des données de DataRecording.
Pseudographisme 
Rappel sur le codage :
0 : erreur à remplacer par un "espace"
1 : pas d'erreur : à rmeplacer par un X

On affichera un résultat du type :
        glob nabm repet sang hep_b prot mont incomp cotamin
  id     sum    G N R S H P M I C
   1     251    . . . . . . . . .
   2     173    . . . . . . . . .
   3      41    X . . . . . . . X
   4     158    . . . . . . . . .
   5      67    . . . . . . . . .
   6     194    X . . X . . . . .

Mais la clé contient el début et la fin de la clé initiale
   
"""

import conf_file
import data_recording
import pandas as pd
import sqlite3
from bm_u import title

def transcode(string):
    """replace 0 by ' ' and 1 by X"""
    if string == 0 or string =='0':
        return '.'
    elif string == '1':
        return 'X'
    else:
        return string    
        #  raise ValueError("Error transcoding : {}".format(string))

class PseudoGraph():
    
# Constantes pour affichage régulier
    FORMAT_C1= "{:>4}"
    LK_FMT = "{:>40}"
    END = '    '
    cols = [ line[0] for line in data_recording.Glob.dicoTables['rep'][4:] ]

    def __init__(self, long_key=True):
        self.long_key=long_key

            
    def prt_header(self):
        """Afficher les noms complets de colonnes et les noms réduits."""

        # noms des colonnes:
        print(self.FORMAT_C1.format('')
              +PseudoGraph.END+PseudoGraph.FORMAT_C1.format('')
              +PseudoGraph.END
              +' '.join(PseudoGraph.cols))

        # affiche l'entête réduit
        if self.long_key:
            print(self.LK_FMT.format(''), end = PseudoGraph.END)
        print(PseudoGraph.FORMAT_C1.format('id'), end = PseudoGraph.END)
        print(PseudoGraph.FORMAT_C1.format('sum'), end = PseudoGraph.END)

        # et Affiche les Initiales des dernières colonnes
        print(' '.join([mot[0].upper() for mot in PseudoGraph.cols]))


def resume_cle(msg, begin_len, end_len):
    """retourne le début et la fin"""
    return msg[9:9+begin_len]+"..."+ msg[-end_len:]

def pseudographe(long_key=True):
    
        
    DR = data_recording.DataRecorder(db_name="PRIVATE/result.sqlite")
    sql = "Select * from rep"
    DR.con.row_factory = sqlite3.Row
    cursor = DR.con.execute(sql)

    ps = PseudoGraph(long_key=True)
    ps.prt_header()
    for line in cursor:
        
        print(ps.FORMAT_C1.format(line['id']), end=ps.END)
        if long_key:
            print(ps.LK_FMT.format(resume_cle(line['cle'], 8, 30)), end=ps.END)
        try: 
            print(ps.FORMAT_C1.format(line['sum']), end=ps.END)
        except:
            print(ps.FORMAT_C1.format("XXXX"), end=ps.END)
        lst = [ transcode(str(line[i])) for i in ps.cols]
        print(' '.join(lst))
    

if __name__ == '__main__':
    pseudographe()
    
    



