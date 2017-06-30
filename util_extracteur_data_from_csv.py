#!/bin/env python3
"""Extraction des données de facturation de glims.

Données au format csv, separées par des |

Quelques références à :
- Analyse de données en Python/ Manipulation de données avec Pandas,
Numpy et IPython. Wes McKinney, Ed Eyrolles, 2015.
- http://pandas.pydata.org/pandas-docs/stable/10min.html
"""

# prochaine extraction : ne pas oublier :
# del = |
# supprimer service
# récupérer uniquement le code NABM

import pandas as pd
import numpy as np
from bm_u import title, prt_lst, readkey
import conf_file as Cf

HEADER_POS = 6 # numéro ("humain") de la ligne contenant les noms de colonnes)

# difficulté : la structure du fichier entrant est variable.
# Nom et ordre des colonnes à obtenir.

# L'ordre des différentes utilisé est variable (je ne sais pourquoi)
INPUT_COLUMNS = ['Objet/patient', 'N°Séjour', 'Date', 'Numdossier', 'Prescripteur', 'CdeNABM',
           'B', 'BNH',  'EUR',  'TB']
# Nom et ordre des colonnes à obtenir.
COLUMNS = ['Objet', 'Sejour', 'Date', 'Dossier', 'Prescripteur', 'CdeNABM',
           'B', 'BNH', 'TB', 'Eur']

def corriger_structure(df):
    """corrige la stucture du tableau d'entrées.

L'extraction de la facturation sous Glims souffre d'une limitation :
Les colonnes vides ne sont pas extraites.
Je préfère travailler avec un DataFrame contenant toujours le même nombre
de colonnes, quitte à ce que certaines soient totalement vides.

exemple de ligne d'entête : cas idéal : 
Objet/patient|N°Séjour|Date|Numdossier|Prescripteur|CdeNABM|B|BHN|Eur|TB

Cas possible :
Objet/patient|N°Séjour|Date|Numdossier|Prescripteur|CdeNABM|B|TB

Par ailleurs, il est nécessaire de vérifier l'ordre des 4 desnières colonnes.

"""
    return df.reindex_axis(INPUT_COLUMNS, axis=1)
            
def debug_structure():
    """"Une fonction pour aider à adapter ce programme à un nouveau fichier."""
    with open(filename, encoding=FILE_ENCODING) as f:
        title ("Aide pour la lecture du fichier")
        DEB_FICHIER = f.readlines()[0:10]
        for i, line in enumerate(DEB_FICHIER):
            print(i, line)
        title("La ligne d'intérêt est sans doute : ")
        HEADER=DEB_FICHIER[HEADER_POS-1]
        print(HEADER)
        title("La structure actuelle de l'objet data est: ")
        print(data.columns)

def invoice_extractor(grouped_data, mode='MOD02'):
    """generator of invoices (facture) """
    verbose= False
    index = 0
    for cle, res in grouped_data: # Pour chaque personne et chaque jour,
        if verbose:
            print("cle :", cle)
            print(res)
            print("_____________")
        lines_of_invoice = [] # invoice = bill = facture
        for line in res.values:
            if mode=='MOD01':
                lines_of_invoice.append(line[4])
            elif mode=='MOD02':
                # print(line)
                try :
                    # En entrée on a :
                    # ['objet', 'séjour','date', 'Dossier' 'prescripteur' 'acte',
                    # 'B', 'BNH', 'TB', 'Eur']
                    # En sortie on veut obtenir :
                    # ['dossier', 'acte', 'code_info', 'nombre', 'lettre' ]
                    if not np.isnan(line[6]):
                        lines_of_invoice.append([ line[3], line[5], '', int(line[6]), 'B'])
                    if not np.isnan(line[7]):
                        lines_of_invoice.append([ line[3], line[5], '', int(line[7]), 'BHN'])
                except :
                    print("Bad input : ")
                    print(line)
                    print("End of error")
                    raise Error
                
        yield (cle, lines_of_invoice)

def invoice_extractor_with_filter(grouped_data, mode='MOD02', filter='None'):
    """generator of invoices with a filter on the firt column"""
    verbose= False
    index = 0
    for cle, res in grouped_data: # Pour chaque personne et chaque jour,
     
        if verbose:
            print("cle :", cle)
            print(res)
            print("_____________")
        lines_of_invoice = [] # invoice = bill = facture
        
        if cle[0].startswith(filter):
            for line in res.values:
                if mode=='MOD01':
                    lines_of_invoice.append(line[4])
                elif mode=='MOD02':
                    # print(line)
                    try :
                        # En entrée on a :
                        # ['objet', 'séjour','date', 'Dossier' 'prescripteur' 'acte',
                        # 'B', 'BNH', 'TB', 'Eur']
                        # En sortie on veut obtenir :
                        # ['dossier', 'acte', 'code_info', 'nombre', 'lettre' ]
                        if not np.isnan(line[6]):
                            lines_of_invoice.append([ line[3], line[5], '', int(line[6]), 'B'])
                        if not np.isnan(line[7]):
                            lines_of_invoice.append([ line[3], line[5], '', int(line[7]), 'BHN'])
                    except :
                        print("Bad input : ")
                        print(line)
                        print("End of error")
                        raise Error
                    
        yield (cle, lines_of_invoice)

def etude_dossier_par_nom(nom='None'):
    for patient, inv in invoice_extractor_with_filter(grouped, mode='MOD02', filter = nom):
        if inv:
            title(patient)
            patient = reformat_cle(patient)
            data = model_etude_4(inv,  label=patient,  model_type='MOD02')
            new_data = reformat_conclusion(patient, data)



def reformat_conclusion(cle, data):
    """
Crée un dictionnaire à partir du format de la fonction facturation.model_etude_2.
version 2 : plus lisible :On code 0 si bon et 1 si mauvais.

format entrée : soit True, soit (False, {dicto des erreurs})
format de sortie : un dictionnaire simple. Exemples : 

    >>> reformat_conclusion("LAMBERT Paul", True) == {'cle': 'LAMBERT Paul', 'glob': True}
    True
    >>> reformat_conclusion("MICHEL Mère", (False, {'fleur':'lilas', 'arbre':'pommier'})) == {'cle': 'MICHEL Mère', 'glob': False, 'fleur':'lilas', 'arbre':'pommier'}
    True
    
"""
    if data is True:
        return {'cle': cle, 'glob': True}
    else:
        new_data=data[1]
        new_data['glob'] = data[0]
        new_data['cle'] = cle
        return new_data

def reformat_cle(cle):
    """ reformat la clée sur un seul champ
    >>> reformat_cle(('LAPIN, DE GARENNE, LIEVRE, (F) 31/12/1941', '01/08/2017'))
    'LAPIN, DE GARENNE, LIEVRE, (F) 31/12/1941, 01/08/2017'
    """

    return ','.join([str(item) for item in cle])

def _test():
    """Execute doctests."""
    import doctest
    (failures, tests) = doctest.testmod(verbose=True)
    print("{} tests performed, {} failed.".format(tests, failures))
    print()

class Reset():
    """Réinitialise pour une nouvelle étude."""

    def reset(self):
        """Vide la table rep"""  
        from data_recording import DataRecorder, Glob
        DR = DataRecorder(db_name=Glob.DB_FILE)
        DR.con.execute("delete from rep")
        DR.commit()

        import os
        try: 
            os.remove('PRIVATE/erreurs.txt')
        except:
            print("Fichier inexistant")  
if __name__=='__main__':

    # _test()

    if 0:
        AA= Reset()
        AA.reset()
        
    from facturation import model_etude_4
    
# importer les données et renommer les colonnes
# Attention : le header semble varier : peut être à 4 ou 5 en fonction de l'extraction !
    # filename = 'PRIVATE/extrait_anon_201705_17.csv' 
    filename = 'PRIVATE/factu_v7.csv'
    FILE_ENCODING = 'ISO-8859-15'
    # FILE_ENCODING = 'ansi'

    data = pd.read_csv(filename, sep='|',
                   encoding=FILE_ENCODING,
                   header= HEADER_POS-2) # lignes à sauter, la première étant notée 0 ?
                   # la suivante est le header.
    # imposer une structure et simplifier les noms
    data = corriger_structure(data)


    
    data.rename(columns={'Objet/patient':'Objet'}, inplace=True)
    data.rename(columns={'N°Séjour':'Sejour'}, inplace=True)
    data.rename(columns={'Numdossier':'Dossier'}, inplace=True)

    # traitement des données manquantes : cf. McKinney p. 156
    data = data.replace('-', np.nan)

    # imposer le format des colonnes
    data.Dossier = data.Dossier.apply(str) # convertion en str
    data.B = data.B.apply(float)
        
    # Les lignes contenant Total sont à exclure. note : utiliser & et non and.
    EXCLURE = "Total"
    data2 = data[(data.Dossier != EXCLURE) &
                 (data.Prescripteur != EXCLURE) &
                 (data.Objet != EXCLURE)]
    
    # grouper pour une même personne et un même jour
    # grouped = data2.groupby(['Objet', 'Date'])
    grouped = data2.groupby(['Objet', 'Date', 'Sejour', 'Prescripteur'])

    # Recherche d'un cas particulier :
    if 0: 
        title ('')
        title("Extraction d'un dossier par nom")
        etude_dossier_par_nom(nom='BARATHE')
    
    # création d'un itérateur de factures
    if 1: 
        print('')
        title("Extraction de tous les dossiers.")
        from data_recording import DataRecorder, Glob
        DR = DataRecorder(db_name=Glob.DB_FILE)
        i = 1
        for i, (patient, inv) in enumerate(invoice_extractor(grouped, mode='MOD02')):
            if 1:  # on peut écrire <9999
                patient = reformat_cle(patient)
                patient = "Cas {:04d},".format(i+1)+patient
                title(patient)
                data = model_etude_4(inv,  label=patient,  model_type='MOD02')
                new_data = reformat_conclusion(patient, data)
                DR.record_expertise(new_data)
                DR.commit()
            i += 1
        DR.close()
    
    if 0:
        print(); title("AU FINAL")
        DR.show_rep()

        

        
