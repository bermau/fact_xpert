# Essai de connexion à une base mysql depuis python3 
# en utilisant le paquet python3-mysql-connector
# En 2016 sur Debian8.1, j'ai simplement installé le paquet python3-mysql-connector
# et suivi la page :
# http://apprendre-python.com/page-database-data-base-donnees-query-sql-mysql-postgre-sqlite

import mysql.connector 
from lib_bm_utils import titrer
import conf_file_amz

def deduireColomumnNameFromYear(year):
    """Return column name from year. Example :
2011 return 'y1'
2009 return 'y9'
2000 and 2010 return 'y10'
"""
    year=str(year)
    digit=str(year[-1])
    if digit=='0':
        digit='10'
    name='y'+digit
    return name


class ConnMysql(object):
    def __init__(self):
        self.conn = mysql.connector.connect(host="localhost",user="amazilia",
                                   password="cmpmd7MG",
                                   database="amazilia_prod")
        self.cursor=self.conn.cursor()

    def sendSelect(self,req):
        self.cursor.execute(req)
        rows = self.cursor.fetchall()
        for row in rows:
            for col in row :
                print(str(col)+'|',end='')
            print()
            # print('{0} : {1} - {2}'.format(row[0], row[1], row[4]))
    def sendUpdate(self,req):
        print("La requête sera ")
        print(req)
        self.cursor.execute(req)
        
    
    def afficherCodesAMettreAJour(self,annee):
        titrer("Affichons les  30 premiers codes à mettre à jour pour {}".format(annee))
        self.sendSelect("""
select *
FROM tests_per_year
LEFT JOIN activity_{year}
ON tests_per_year.lms_code=activity_{year}.code
LIMIT 30
    """.format(year=annee,))

    def updateCodesExistants(self,annee, colonne):
        titrer("Mise à jour des codes existants")
        # Mise à jour des codes existants
        self.sendUpdate("""UPDATE
 tests_per_year
 LEFT JOIN activity_{the_year}
ON tests_per_year.lms_code=activity_{the_year}.code
SET tests_per_year.{the_column}=activity_{the_year}.nb
""".format(the_year=annee,the_column=colonne))
     
    def afficherNouveauxCodes(self):
        titrer("Affichons maintenant les nouveaux codes")
        self.sendSelect("""
        Select description,code, y1, y2, y3, y4, A.nb, y6, y7, y8, y9, y10
        FROM activity_2015 AS A LEFT JOIN tests_per_year
        ON A.code=tests_per_year.lms_code
        WHERE tests_per_year.lms_code IS NULL
""")        
    def updateNouveauxCodes(self):
        self.sendUpdate("""
        INSERT INTO  tests_per_year ( description, lms_code, y1, y2, y3, y4, y5, y6, y7, y8, y9, y10)
        (SELECT description,code, y1, y2, y3, y4, activity_2015.nb, y6, y7, y8, y9, y10 FROM
        activity_2015 LEFT JOIN tests_per_year
        ON activity_2015.code=tests_per_year.lms_code
        WHERE tests_per_year.lms_code IS NULL)
        """)
    
if __name__ == '__main__':
    annee='2015'
    colonne=deduireColomumnNameFromYear(annee)
    print("La colonne a étudier est {}".format(colonne))

    C=ConnMysql()
    C.afficherCodesAMettreAJour(annee)

    
    C.cursor.close()
