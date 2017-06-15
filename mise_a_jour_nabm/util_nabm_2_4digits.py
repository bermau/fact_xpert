# file : util_nabm_2_4digits
"""Convertir la table de la nabm en format acceptée pour l'intégration dans
sqlite.

Méthode pour la conversion : récupérer le fichier excel de nabm.
Le traiter avec l'utilisatire d'amazilia (tableur openoffice).
- Récupérer les fichiers couples_incompabible.csv et le traiter avec le
programme util_incompat_2_4digits.


- Récupérer le fichier nabm.csv et le traiter avec ce fichier.
Le fichier nabm.csv entré est de type :
- séparé par des virgules,
- utf8,
- champs délimités par des doubles guillemets

Typiquement le début du csv d'entrée est :

$head -n 20 nabm.csv 
"CODE","CHAPITRE","SOUS-CHAPITRE","COEFFICIENT B","DATE CREATION","LIBELLE","ENTENTE PREALABLE","REMBOURSEMENT 100%","NBR MAXI DE CODE","N° REGLE SPECIFIQUE","REF INDICATION MEDICALE","ACTES RESERVES","INITIATIVE BIOLOGISTE","CONTINGENCE TECHNIQUE","R.M.O.","EXAMEN SANGUIN","DERNIERE DATE EFFET","CODES INCOMPATIBLES"
4084,0,0,500,22/10/2010,"DETERMINATION PRENATALE DU SEXE FOETAL SANG MATERNEL",,"1",1,,"1","1",,3,,"1",15/03/2011,
9905,0,0,5,14/02/1997,"COMPLEMENT A LA COTATION MINIMALE DE VALEUR B 5 (SANG)",,,,,,,"1",,,"1",19/01/2010,
...
9105,0,0,5,04/07/2002,"FORFAIT DE SECURITE POUR ECHANTILLON SANGUIN",,,,,,,"1",,,"1",11/11/2007,
9106,0,0,8,04/07/2002,"FORFAIT DE SECURITE POUR ECHANTILLONS BACTERIO, MYCO ET PARASITO",,,1,,,,"1",,,,01/04/2017,
9005,0,0,16,30/12/2008,"FORFAIT DE PRISE EN CHARGE PRE-ANALYTIQUE DU PATIENT",,,1,,,,"1",,,,20/04/2016,
...

9005,0,0,16,30/12/2008,"FORFAIT DE PRISE EN CHARGE PRE-ANALYTIQUE DU PATIENT",,,1,,,,"1",,,,20/04/2016,
9001,0,0,26,01/01/1996,"SUPPLEMENT POUR ACTES EN URGENCE NUIT",,,,,,,"1",,,,13/04/2014,"9002-9004"
9004,0,0,26,07/02/2001,"SUPPLEMENT POUR ACTES EN URGENCE (SAMEDI APRES 12H, DIMANCHE, FERIE)",,,,,,,"1",,,,13/04/2014,9001

On note :
- un header
- sur la ligne commençant par 900A, en fin de ligne, 2 codes d'exclusion entre guillemets.
- sur la ligne commençant par 9004, un seul code d'exception.
"""

import util_incompat_2_4digits as lib 
# Import d'un CSV de Excel.
import sys, csv
import pdb
from lib_bm_files import get_ouput_file_name


def print_lst(lst):
    for item in lst:
        print(item)
        
# Definition des formats pour l'entrée et la sortie
class InputCsv(csv.excel):
    delimiter = ","
    
class OutputCsv(csv.excel):
    delimiter = ";"

class FormatVerifyer():
    """Une classe pour vérifier le format d'entrée de données."""
       

def _test():
    """Execute doctests."""
    import doctest
    doctest.testmod(verbose=True)

if __name__=='__main__':
    
    _test()
    
    # déclarations
    file_name = "data_nabm/nabm.csv"
    output_file_name = get_ouput_file_name(file_name, '_ok')

    output_lines = []

    csv.register_dialect('format_entree', InputCsv())
    csv.register_dialect('format_sortie', OutputCsv())
    
    # lecture
    print("test d'importation d'un fichier CSV")
    print("ce fichier est dans " + file_name)

    file = open(file_name, "r")
    image = []
    try:
      #reader = csv.reader(file, 'excel-fr')
      #reader = csv.DictReader(file, 'excel-CTCB')
      reader = csv.reader(file, 'format_entree')
      for row in reader:   
          image.append(row)
    finally:
        file.close()    
    print_lst(image)

    # traitement
    ref_length = len(image[0])
    for ln_lst in  image[1:]:
        length = len(ln_lst)
        if length != ref_length:
            print("Error")
        else:
            del ln_lst[-1] # suppr colonne des incompatibilités
            ln_lst[0] = lib.to4digits(ln_lst[0])
    print_lst(image)        

    # écriture
    with open(output_file_name, 'w') as f:
        writer = csv.writer(f, 'format_sortie')
        writer.writerows(image)

    
