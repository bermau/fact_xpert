#!/bin/env python3
"""Essai de connexion à un odbc.

Pour que le programme fontionne il faut créer une connexion avec la base:

CONNEXION = MyODBC_to_infocentre()
... le programme
del(CONNEXION)
"""

import pyodbc
import conf_file as Cf
import lib_nabm # utilitaires pour la NABM
import facturation
import datetime, sys


CONNEXION = '' # sera utilisé pour la connexion à la base

class MyODBC_to_infocentre(object):
    """Une classe pour gérer la connexion"""
    _db_connection = None
    _db_cur = None

    def __init__(self):
        self._db_connection = pyodbc.connect(Cf.CONNEXION_BASE_PROD)        
        self._db_cur = self._db_connection.cursor()

    def query(self, query, params):
        if params:
            return self._db_cur.execute(query, params)
        else:
            return self._db_cur.execute(query)
    def __del__(self):
        self._db_connection.close()
        sys.stderr.write("Connexion à la base refermée\n")

def prt(msg=''):
    """Print or save a msg"""
    print(msg)


def le_lendemain(jour_fr_str):
    """Retourne le jour suivant d'un jour en français
    >>> le_lendemain('28/02/2015')
    '01/03/2015'
    >>> le_lendemain('31/01/2015')
    '01/02/2015'
    """
 
    annee = int(jour_fr_str[6:10]) # On convertit la chaine de caractère en integer   
    mois = int(jour_fr_str[3:5])
    jour = int(jour_fr_str[0:2])
         
    jour = datetime.datetime(annee, mois, jour)
    duree_de_un_jour = datetime.timedelta(1) # la durée d'une journée
    demain = jour + duree_de_un_jour
    
    return demain.date().strftime('%d/%m/%Y')
    

def req_example_via_class(dos_id=None):
    """Un exemple de requête vers infocentre
    <<>>> a=req_example_via_class(25)
    (1, 2)
    """
    cursor = CONNEXION.query("SELECT 1,2",None)
    rows = cursor.fetchall()
    for line in rows:
        print(line)


def req_verbosing_invoice(req_id=None):
    """Un essai de requête vers infocentre
    <<>>> a=req_verbosing_invoice(req_id=6040831088) ; a[0][1]
    'IDEXT'
    
    """
##    if not isinstance(req_id,int):
##        req_id=int(req_id)
    cnxn = pyodbc.connect(Cf.CONNEXION_BASE_PROD)
    cursor = cnxn.cursor()
    cursor.execute("""SELECT R.ACCESSNUMBER,
       CONNEXION.ACTREF, 
       DBT.TESTCODE, 
       A.NBBILLU, A.BILLUREF, 
       DA.COEFFICIENT, DA.DEFACTNB, DA.BUID, 
       I.VISITDATE, I.AMOUNTDUE, I.CLOSINGDATE, I.LOGDATE, P.NAME, P.FIRSTNAME
FROM REQUESTS R 
     JOIN PATIENTS P 
          ON R.PATID=P.PATID
     JOIN INVOICES I
          ON I.ACCESSNUMBER=R.ACCESSNUMBER
     JOIN ACTS A
          ON A.INVOICEID=I.INVOICEID
     LEFT JOIN DICT_ACTS DA
          ON DA.ACTID=A.ACTID
     JOIN DICT_BILL_TESTS DBT
          ON DBT.BILLTESTID=A.BILLTESTID
WHERE R.ACCESSNUMBER = ?""", req_id  )

    rows = cursor.fetchall()  # lit toute la suite
    cursor.close()
    return rows

def req_invoice(req_id=None):
    """Renvoie la facture courte d'un ID
    >>> a=req_invoice(req_id=9072132971) ; a[0][1]
    '9105'
    """
    sql="""SELECT R.ACCESSNUMBER,
       A.ACTREF, 
       DBT.TESTCODE, 
       A.NBBILLU, A.BILLUREF
FROM REQUESTS R 
     JOIN PATIENTS P 
          ON R.PATID=P.PATID
     JOIN INVOICES I
          ON I.ACCESSNUMBER=R.ACCESSNUMBER
     JOIN ACTS A
          ON A.INVOICEID=I.INVOICEID
     LEFT JOIN DICT_ACTS DA
          ON DA.ACTID=A.ACTID
     JOIN DICT_BILL_TESTS DBT
          ON DBT.BILLTESTID=A.BILLTESTID
 
WHERE R.ACCESSNUMBER = ?"""
    
    cursor = CONNEXION.query(sql,(req_id))
    rows = cursor.fetchall()
    # save_pickle(rows,"ID", IPP, date)
    return rows


def req_vers_syn():
    """Un essai de requête vers Synergy"""
    cnxn = pyodbc.connect(Cf.CONNEXION_BASE_PROD)
    cursor = cnxn.cursor()

    motif= "%Escheri%"
    cursor.execute("SELECT * FROM DICT_TEXTS WHERE TEXTTYPE=2 AND FULLTEXT LIKE ?",motif )

    rows = cursor.fetchall()  # lit toute la suite
    res=[]
    for row in rows:
            res.append(row[1]+"\t"+row[4]+"\t"+row[13])
    cursor.close()
    print()
    print()
    for line in res:
        print(line)
    return res


def req_results_from_id(id=None):
    """Essai pour le DIM : retrouver des résultats depuis une ID pour créer un csv."""
        
    cnxn = pyodbc.connect(Cf.CONNEXION_BASE_PROD)
    cursor = cnxn.cursor()
    output=[]
    cursor.execute("""SELECT P.REFHOSPNUMBER,DT.TESTCODE, DT.SHORTTEXT, T.RESVALUE, DT.UNITS, R.REQDATE
FROM TESTS T, REQUESTS R, PATIENTS P, DICT_TESTS DT
WHERE R.PATID=P.PATID
AND R.ACCESSNUMBER= ? 
AND R.REQUESTID=T.REQUESTID
AND DT.TESTID=T.TESTID
AND T.RESVALUE IS NOT NULL""", id  )

    rows = cursor.fetchall()  # lit toute la suite
    cursor.close()
    return rows


def req_main_results_from_id_A_REVOIR(id=None):
    """Essai pour le DIM : principaux résultats de chimie et hémato.

- retrouver des résultats depuis une ID.
- Comme on ne veut que que quelques résultats, je filtre sur certains
chapitres.

Cette fonction est appelée par self.essai_flux_pour_dim().
"""
    cnxn = pyodbc.connect(Cf.CONNEXION_BASE_PROD)
    cursor = cnxn.cursor()
    output=[]
    print("id reçu" , id)
    cursor.execute("""SELECT P.REFHOSPNUMBER,DT.TESTCODE, DT.SHORTTEXT, T.RESVALUE, DT.UNITS, R.REQDATE
FROM TESTS T, REQUESTS R, PATIENTS P, DICT_TESTS DT
WHERE R.PATID=P.PATID
AND R.ACCESSNUMBER= ?
AND DT.CHAPID in (12,14,16,22,23,24,25,28)
AND R.REQUESTID=T.REQUESTID
AND DT.TESTID=T.TESTID
AND T.RESVALUE IS NOT NULL""", id  )

    rows = cursor.fetchall()  # lit toute la suite
    cursor.close()
    return rows



def save_pickle(rows, titre, arg1, arg2):
    import pickle
    file_name = titre + "_" + str(arg1) + "_" + str(arg2.replace("/","")) + ".pickle"
    with open(file_name,mode='wb') as fichier:
         pickle.dump(rows, fichier)
         
def save_pickle_v2(rows, titre, *args):
    """Sauvegarde des données"""
    import pickle
    file_name = titre + "_" + str(args) + "_" + str(arg2.replace("/","")) + ".pickle"
    print(*args)

def req_ids_from_patid(IPP, date):
    """Liste des numéros ID long à partir d'un IPP pour une date donnée.

Les arguments de date doivnent être fournis au format français. 
La requête retourne des dates en format ISO.
      
"""
    patid = IPP
    lendemain = le_lendemain(date)    

    sql=r"""SELECT top 20 
  R.ACCESSNUMBER, P.NAME, P.FIRSTNAME, P. MAIDENNAME
FROM REQUESTS R
RIGHT JOIN PATIENTS P
   ON R.PATID=P.PATID
 JOIN HOSPITALIZATIONS H
   ON R.HOSPITID=H.HOSPITID

WHERE P.PATNUMBER = ? 
AND R.COLLECTIONDATE BETWEEN ? AND ?
ORDER BY R.ACCESSNUMBER
"""
    
    cursor = CONNEXION.query(sql,(patid, date,lendemain))
    rows = cursor.fetchall()
    # save_pickle(rows,"ID", IPP, date)
    return rows

def req_ids_of_a_collectiondate(date):
    """Liste les ID pour une date de prélèvement."""

    lendemain = le_lendemain(date)
    sql=r"""SELECT  TOP 500 
  R.ACCESSNUMBER, P.NAME, P.FIRSTNAME, P. MAIDENNAME, P.PATNUMBER
FROM REQUESTS R
RIGHT JOIN PATIENTS P
   ON R.PATID=P.PATID
   
WHERE R.COLLECTIONDATE BETWEEN ? AND ?
ORDER BY R.ACCESSNUMBER
"""
    cursor = CONNEXION.query(sql, (date, lendemain))
    rows = cursor.fetchall()
    # save_pickle(rows,"activite_par_collection", '',date)
    return rows


def fac_de_IPP_date(IPP, date):
    """Etudie les factures cumulées d'un patient pour un jour donné"""

    def prt_list_tab(lst):
        """Imprime une liste tabulée"""
        for line in lst:
            a = [ str(mot) for mot in line ]
            print("\t".join(a))
    prt()
    prt("************************************************************")
    prt("Patient :   IPP : {} ". format(IPP))
    prt("Patient : venue : {} (date de prel)".format(date)) 
    dossiers_lst = req_ids_from_patid(IPP, date)
    prt("NOM : {}    prénom : {}    NJF : {}".format(
        dossiers_lst[0][1],dossiers_lst[0][2],dossiers_lst[0][3] ))
    # Pour débugguer :          
    # dossiers_lst = [('9072132939', ), ('9072132971', )]
    request_id_lst = [ ligne[0] for ligne in dossiers_lst ]
    prt()
    prt("Liste des dossiers Synergy à traiter : \n{}".format(request_id_lst)) ; prt()
    cumule = []
    for request_id in request_id_lst:
         print ("Traitement du dossier {}".format(request_id))
         cumule.extend(req_invoice(req_id=request_id))
         # a = req_invoice(req_id=request_id)
    prt()
    # save_pickle(cumule,"cumule", IPP, date)
    # prt_lst(cumule)
    # Présentation de la facture cumulée (cumule) sous diverses formes
    prt_list_tab(cumule)

##    print("Cumule vaut : ")
##    print(cumule) 
##    actes_lst = [ ligne[1] for ligne in cumule if ligne[1] ]
##    print("IMPORTANT : élimination des actes HN")
##    print(" ".join(actes_lst))
##    print("Test de la règle des protéines:")
##    print(lib_nabm.detecter_plus_de_deux_proteines(actes_lst))
##    print("Test de la règle des sérologie:")
##    print(lib_nabm.detecter_plus_de_trois_sero_hepatite_b(actes_lst))

    # lancer la vérification du module facturation
    facturation.model_etude_1(cumule, model_type='MOD02')
    
def essai_sur_base():
    """Récupérer un nom de colonne"""
    
    cursor = CONNEXION.query(sql,None)
    row = cursor.execute("select count(*) as user_count from users").fetchone()
    print('{} users'.format(row.user_count))

def get_range_of_id(date, from_id, to_id):
    """Retourne une séquence de dossier pour un jour donné.

    >>> get_range_of_id('60201',117, 119 )
    ['6020100117', '6020100118', '6020100119']
    """
    return [ date+str(a).rjust(5,'0') for a in range(from_id,to_id+1) ]

def essai_flux_pour_dim():
    """Création d'un fichier CSV d'essai pour le DIM."""
    import lib_utilitaires_synergy
    date = '60110'
    debut = 1627
    fin = 1636
    nom_fichier = 'res_' + date + str(debut).rjust(5,'0') + '_' \
                  + date + str(fin-1).rjust(5,'0') + '.csv'
    print("Le fichier de sortie sera : {}".format(nom_fichier))
    
    la_liste = lib_utilitaires_synergy.get_range_of_id(date,debut,fin)
    print(la_liste)
    with open(nom_fichier, 'w', encoding='utf-8') as fichier:
        for dossier in la_liste:
            print("je traite le dossier : {}".format(dossier))
            # les_res=req_results_from_id(id=dossier)
            les_res = req_main_results_from_id(id=dossier)
            for line in les_res:
                a= str(line[0]), str(line[1]), str(line[2]),str(line[3]), \
                   str(line[4]),line[5].strftime('%Y%m%d')
                b= ";".join(a)
                print(b)
                fichier.write(b + "\n")
def prt_lst(une_liste):
    for line in une_liste:
        print(line)

def _demo_pickle():
    import pickle
    file_name=r'data.pickle'
    with open(file_name,mode='wb') as fichier:
        pickle.dump(les_res, fichier)

    print("récupération des données enregistrées dans le fichier .{}".format(file_name))
    with open(file_name, 'rb') as fichier:
        les_res_recup=pickle.load(fichier)

    print(les_res_recup)
    
def _demo_facturation_pour_IPP_un_jour():
    fac_de_IPP_date(IPP='00000000000002135656', date = '29/01/2014') # B hep
    fac_de_IPP_date(IPP='00000000000002135656', date = '21/07/2009') # B div
 
def _demo_etude_facturation_d_un_jour(french_date):
    """Etude de Facturation pour un jour donnée.

Pour un jour donnée (date en français), trouve les dossiers prélevé ce jour.
Pour ces dossier, groupe par patient, récupère les factures et les vérifie.
L'ordre de traitement diffère de l'ordre de création des dossiers."""
    collection_date = french_date
    # Recupération de la liste des ID à un jour donné
    lst_id = req_ids_of_a_collectiondate(collection_date)
    prt("Le {}, {} dossiers ont été prélevés.\n".format(
        collection_date,str(len(lst_id)) ))
    # prt_lst(lst_id)
    prt()
    # Je veux : la liste des IPP des différents patients.
    lst_IPP = [ item[4] for item in lst_id if item[4] is not None]
    prt("{} dossiers ont un IPP.\n".format(str(len(lst_IPP))))
    aset_IPP = set(lst_IPP)
    prt("Ces dossiers concernent {} patients avec un IPP".format(
        str(len(aset_IPP))))
    # Pour chaque IPP, je veux l'étude de la facture le jour donné.
    # Je limite volontairement à quelques dossiers.
    for ipp in list(aset_IPP)[4:10]:
    #for ipp in aset_IPP: 
        if ipp is not None:
            fac_de_IPP_date(ipp, collection_date)

def _test():
    """Execute doctests."""
    import doctest
    (failures, tests) = doctest.testmod(verbose=False)
    print("{} tests performed, {} failed.".format(tests, failures))
    
if __name__=='__main__':
    CONNEXION = MyODBC_to_infocentre()
    #_test()
    
    
    _demo_etude_facturation_d_un_jour("01/09/2016")
    del(CONNEXION)
