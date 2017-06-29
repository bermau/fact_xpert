"""Exploitation des données de DataRecording.

Export vers Excel
   
"""

import conf_file
import data_recording
import pandas as pd
from pandas import ExcelWriter

import sqlite3

if __name__ == '__main__':
    
    DR = data_recording.DataRecorder(db_name="PRIVATE/result.sqlite")
    sql = "Select * from rep"
    DR.con.row_factory = sqlite3.Row
    cursor = DR.con.execute(sql)

    rows = cursor.fetchall()
    DF = pd.DataFrame(rows, columns=[item[0] for item in cursor.description])

    # nattention : il faut que le chemin existe.        
    writer = ExcelWriter(conf_file.EXPORT_REP+'/'+'fact_excel.xlsx')
    DF.to_excel(writer, sheet_name='data_fact')
    
    writer.save()
    print("Le fichier a été sauvé dans {}".format(conf_file.EXPORT_REP+'/'+'fact_excel.xlsx'))


