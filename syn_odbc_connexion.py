#!/bin/env python3
"""Essai de connexion à un odbc.

Pour que le programme fontionne il faut créer une connexion avec la base:

CONNEXION = MyODBC_to_infocentre()
... le programme
del(CONNEXION)

Ce programme sauve uniquement les fichiers en erreurs.
"""

import pyodbc
import conf_file as Cf
import bm_u 
import lib_nabm # utilitaires pour la NABM
import facturation
import datetime, sys
import lib_smart_stdout
import lib_synergy # utilitaires pour Synergy

# CONNEXION = '' # sera utilisé pour la connexion à la base
SAVE_PICKLE = False # True pour sauver les données en format pickle.
# Nom du fichier de sauvegarde de la sauvegarde intelligente.
SMART_NAME_EXPORT = "err_"+datetime.date.today().strftime("%Y_%m_%d")+".txt"
# Nom complet pour le rapport.
REPORT= Cf.EXPORT_REP + SMART_NAME_EXPORT


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

def sequence_of_dates(date, n):
    """Return a sequence of dates :
    >>> sequence_of_dates("02/03/2015", 5)
    ['02/03/2015', '03/03/2015', '04/03/2015', '05/03/2015', '06/03/2015']
    """
    la_liste = [ date ]
    curs = date
    for n in range(n - 1,0,-1):
        lendemain = le_lendemain(curs)
        curs = lendemain
        la_liste.append(lendemain)
    return la_liste
    
def quoted_joiner(lst):
    """
    >>> quoted_joiner([ 6048, 2015, 'UHCD'])
    "'6048', '2015', 'UHCD'"
    
"""
    quoted_strings_lst = [ "'"+str(code)+"'" for code in lst] 
    return ", ".join(quoted_strings_lst)

def get_range_of_id(date, from_id, to_id):
    """Retourne une séquence de dossiers pour un jour donné.

    >>> get_range_of_id('60201',117, 119 )
    ['6020100117', '6020100118', '6020100119']
    """
    return [ date+str(a).rjust(5,'0') for a in range(from_id,to_id+1) ]


def prt_lst(une_liste):
    """Print a list in a readable format."""
    for line in une_liste:
        print(line)

def save_as_pickle(rows, titre, arg1, arg2):
    if SAVE_PICKLE:
        import pickle
        file_name = "pickle/"+titre + "_" + str(arg1) + "_" + str(arg2.replace("/","")) + ".pickle"
        with open(file_name, mode='wb') as fichier:
             pickle.dump(rows, fichier)

def _demo_pickle():
    import pickle
    file_name=r'data.pickle'
    with open(file_name,mode='wb') as fichier:
        pickle.dump(les_res, fichier)

    print("récupération des données enregistrées dans le fichier .{}".format(file_name))
    with open(file_name, 'rb') as fichier:
        les_res_recup=pickle.load(fichier)

    print(les_res_recup)
    
    
    
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


class Syn():
    """Ordres spécifiques Infocentre/Synergy."""


    def req_example_via_class_Syn(self, dos_id=None):
        """Un exemple de requête vers infocentre
        <<>>> a = Syn().req_example_via_class_Syn(25)
        (1, 2)
        """
        cursor = CONNEXION.query("SELECT 1,2",None)
        rows = cursor.fetchall()
        for line in rows:
            print(line)


    def req_verbosing_invoice(self, req_id=None):
        """Un essai de requête vers infocentre
        <<>>> a = Syn().req_verbosing_invoice(req_id=6040831088) ; a[0][1]
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

    def req_invoice(self, req_id=None):
        """Renvoie la facture courte d'un ID
        >>> a=Syn().req_invoice(req_id=9072132971) ; a[0][1]
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
        # save_as_pickle(rows,"ID", IPP, date)
        return rows


    def req_results_from_id(self, id=None):
        """Essai pour le DIM : retrouver des résultats depuis une ID pour créer un csv."""
            
        cnxn = pyodbc.connect(Cf.CONNEXION_BASE_PROD)
        cursor = cnxn.cursor()
        output=[]
        cursor.execute("""SELECT P.REFHOSPNUMBER,DT.TESTCODE,
                                 DT.SHORTTEXT, T.RESVALUE, DT.UNITS, R.REQDATE
    FROM TESTS T, REQUESTS R, PATIENTS P, DICT_TESTS DT
    WHERE R.PATID=P.PATID
    AND R.ACCESSNUMBER= ? 
    AND R.REQUESTID=T.REQUESTID
    AND DT.TESTID=T.TESTID
    AND T.RESVALUE IS NOT NULL""", id  )

        rows = cursor.fetchall()  # lit toute la suite
        cursor.close()
        return rows


    def req_ids_from_IPP_date(self, IPP, date):
        """Liste des numéros ID longs à partir d'un IPP pour une date donnée.

    Les arguments de date doivent être fournis au format français. 
    La requête retourne des dates en format ISO.
          
    """
        patid = IPP
        lendemain = le_lendemain(date)
        # Les ref à HOSPTITALIZATION sont inutiles.
        sql=r"""SELECT top 20 
      R.ACCESSNUMBER, P.NAME, P.FIRSTNAME, P. MAIDENNAME, H.HOSPITNUMBER, P. PATNUMBER
    FROM REQUESTS R
    RIGHT JOIN PATIENTS P
       ON R.PATID=P.PATID
    JOIN HOSPITALIZATIONS H
       ON R.HOSPITID=H.HOSPITID

    WHERE P.PATNUMBER = ? 
    AND R.COLLECTIONDATE BETWEEN ? AND ?
    ORDER BY R.ACCESSNUMBER
    """
##        sql_suffisant=r"""SELECT top 20 
##      R.ACCESSNUMBER, P.NAME, P.FIRSTNAME, P. MAIDENNAME
##    FROM REQUESTS R
##    RIGHT JOIN PATIENTS P
##       ON R.PATID=P.PATID
##
##    WHERE P.PATNUMBER = ? 
##    AND R.COLLECTIONDATE BETWEEN ? AND ?
##    ORDER BY R.ACCESSNUMBER
##    """
        
        cursor = CONNEXION.query(sql,(patid, date, lendemain))
        rows = cursor.fetchall()

        # save_pickle(rows,"ID", IPP, date)
        return rows

    def req_ids_of_a_collectiondate(self, date, location_filter=None):
        """Liste les ID pour une date de prélèvement.
    date : format français
    location_filter : str ou list of str.
    Exemples :   
        location_filter = '6048',
        location_filter = ['6048','2001']
    On extrait aussi l'UF + filtre de service."""

        lendemain = le_lendemain(date)
        sql_start = r"""SELECT  TOP 500 
      R.ACCESSNUMBER, P.NAME, P.FIRSTNAME, P. MAIDENNAME, P.PATNUMBER, DL.LOCCODE
    FROM REQUESTS R
    RIGHT JOIN PATIENTS P
       ON R.PATID=P.PATID 
    LEFT JOIN LOCATIONS L
       ON R.REQUESTID=L.REQUESTID
     LEFT JOIN DICT_LOCATIONS DL
       ON L.LOCID=DL.LOCID
    WHERE R.COLLECTIONDATE BETWEEN ? AND ?"""
        
        if isinstance(location_filter, str) :
            
            sql=sql_start +r"""
    AND DL.LOCCODE = '{}' ORDER BY R.ACCESSNUMBER""".format(location_filter)
        elif  isinstance(location_filter, list) :
            sql=sql_start +r"""
    AND DL.LOCCODE in  ({}) ORDER BY R.ACCESSNUMBER""".format(quoted_joiner(location_filter))
        else:
            print("Filtre UF est faux : ", location_filter)
            sql=sql_start +r"""
    ORDER BY R.ACCESSNUMBER"""

        cursor = CONNEXION.query(sql, (date, lendemain))
        rows = cursor.fetchall()
        save_as_pickle(rows,"activite_par_collection", '',date)
        return rows



    def req_audit_trail_for_id(self, id_str):
        """Retourne l'enregistreur d'un dossier
        >>> Syn().req_audit_trail_for_id('6060248167')
        'JC'

        """
        sql = r"""SELECT STEPDATE,
    STEPTYPE, ATR_ACCESSNUMBER, INITUSER, LIS_SESSION, INITUSER2, VALIDATION
    FROM AUDIT_TRAIL
    WHERE ATR_ACCESSNUMBER = ?
    AND STEPTYPE=1
    """
        cursor = CONNEXION.query(sql, (id_str,))
        rows = cursor.fetchone()
        if rows:
           # print(rows)
           return(rows.INITUSER) 

    def req_full_audit_trail_for_id(self, id_str):
        """Retourne l'audit assez complet d'un dossier"""
        sql = r"""SELECT 
    STEPDATE, STEPTYPE, ATR_ACCESSNUMBER, INITUSER, LIS_SESSION, INITUSER2, VALIDATION
    FROM AUDIT_TRAIL
    WHERE ATR_ACCESSNUMBER = ?
    ORDER BY STEPTYPE
    """
        cursor = CONNEXION.query(sql, (id_str))
        rows = cursor.fetchall()
        for line in rows:
            print(line)    

    @lib_smart_stdout.record_if_true(filename=REPORT)
    def fac_de_IPP_date(self, IPP, date, nabm_version=None):
        """Expertise à partir d'une IPP et d'une date.

Etudie les factures cumulées d'un patient pour un jour donné
La date doit être au format français type 31/12/2016.

Retourne True en cas d'erreur, False Sinon"""

        def prt_list_tab(lst):
            """Imprime une liste tabulée"""
            for line in lst:
                a = [ str(mot) for mot in line ]
                print("\t".join(a))
        # verifier ou corriger les entrées
        IPP=lib_synergy.verif_IPP(IPP)
        prt("***************************************************************************")
        bm_u.title("Nouvelle étude d'IPP à une date donnée")
        if not bm_u.date_is_fr(date):
            print("Erreur saisie de date :", IPP, date)
        elif  nabm_version is None:
            nabm_version = lib_nabm.nabm_version_from_dt(lib_nabm.frdate2datetime(date))
            print("NABM sera déduite de la date : ", nabm_version)
            prt("Patient :   IPP : {} ". format(IPP))
            prt("Patient : venue : {} (date de prel)".format(date)) 
            dossiers_lst = self.req_ids_from_IPP_date(IPP, date)
            # print(dossiers_lst)

            if dossiers_lst:            
                save_as_pickle(dossiers_lst, "fac_ipp_dossiers_lst",IPP, date)

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
                     cumule.extend(self.req_invoice(req_id=request_id))        
                # lancer la vérification du module facturation
                res = facturation.model_etude_1(cumule, model_type='MOD02',
                                                nabm_version=nabm_version)
                # si l'étude du cumule montre une erreur, il faut identifier ceux qui ont enregistré.
                #     Le pb est que l'on ne l'enregistre pas !
                # l'audit est à faire sur les dossiers en erreur, c'est à dire ceux dont res vaut True
                if res:
                    print("Dossiers enregistrés par : ")
                    for dossier in  dossiers_lst:
                        print(dossier[0], "enregistré par", self.req_audit_trail_for_id(
                            dossier[0]))                         
                # note : res vaut True si model_etude_1 a trouvé une erreur.
                # print("Résultat de {}, le {} : {}".format(IPP, date, res))
                return res
            else:
                print("Requête vide")
                return True # (car erreur)
            
    def IPP_from_IEP_and_date(self, IEP,  date):
        """Retourne le numéro IPP à partir de l'IEP et de la date.
        L'exemple ci desosu retourne le dossier de BM
        >>> Syn().IPP_from_IEP_and_date('002135656', "04/06/2015")
        [('00000000000002135656', )]
        
        """
        IEP = lib_synergy.verif_IEP(IEP)

        lendemain = le_lendemain(date) 

        sql=r"""SELECT top 5  P.PATNUMBER
    FROM REQUESTS R
    RIGHT JOIN PATIENTS P
       ON R.PATID=P.PATID
     JOIN HOSPITALIZATIONS H
       ON R.HOSPITID=H.HOSPITID

    WHERE H.HOSPITNUMBER = ? 
    AND R.COLLECTIONDATE BETWEEN ? AND ?
    ORDER BY R.ACCESSNUMBER
    """
 
        
        cursor = CONNEXION.query(sql,(IEP, date, lendemain))
        rows = cursor.fetchall()
        return rows
    
    def fac_de_IEP_date(self, IEP, date, nabm_version=None):
        """Expertise à partir d'une IEP et d'une date.

Etudie les factures cumulées d'un patient pour un jour donné
la date doit être au format français type 31/12/2016.

Retourne True en cas d'erreur, False Sinon"""
        print("Res IPP")
        IPP = self.IPP_from_IEP_and_date(IEP, date)
        print(IPP)
        print("tutu")
        IPP = IPP[0][0]

        
        self.fac_de_IPP_date(IPP, date, nabm_version=nabm_version)




    def req_syn(self):
        """Une requête quelconque (pour mise au point)."""

        IPP = '00000000000002135656'
        IEP = '000000007190243'
        date= "16/10/2015"
        lendemain = le_lendemain(date)
        print(lendemain)
        sql=r"""SELECT top 20 
      R.ACCESSNUMBER, P.NAME, P.FIRSTNAME, P. MAIDENNAME, H.HOSPITNUMBER, P. PATNUMBER
    FROM REQUESTS R
    RIGHT JOIN PATIENTS P
       ON R.PATID=P.PATID
     JOIN HOSPITALIZATIONS H
       ON R.HOSPITID=H.HOSPITID

    WHERE H.HOSPITNUMBER = ? 
    AND R.COLLECTIONDATE BETWEEN ? AND ?
    ORDER BY R.ACCESSNUMBER
    """
        print(sql)

        import pdb
        # pdb.set_trace()
        
        cursor = CONNEXION.query(sql,(IEP, date, lendemain))
        rows = cursor.fetchall()
        print(rows)
        return rows
        

 

    def _demo_facturation_pour_IPP_un_jour(self):
        fac_de_IPP_date(IPP='00000000000002135656', date = '29/01/2014') # B hep
        fac_de_IPP_date(IPP='00000000000002135656', date = '21/07/2009') # B div

     
    def demo_etude_facturation_d_un_jour(self, french_date,  uf_filter=None,
                                          synthesis=None):
        """Etude de facturation pour un jour donnée.

    Pour un jour donnée (date en français), trouve les dossiers prélevés ce jour.
    Ces dossiers sont groupés par patient. Récupère les factures cumulées et les
    vérifie.
    uf_filter='6048'
    uf_filter=[ 6048, 2105, 'UHCD']
    Note : l'ordre de traitement diffère de l'ordre de création des dossiers."""
        collection_date = french_date
        # Recupération de la liste des ID à un jour donné
        # La sortie standard du niveau ci-dessous est redirigée dans un fichier
        with lib_smart_stdout.PersistentStdout(filename=REPORT) as buf:
            facturation.print_version_and_date()
            lst_id = self.req_ids_of_a_collectiondate(collection_date,
                                                 location_filter=uf_filter)
            save_as_pickle(lst_id,"demo_lst_id", '', french_date)  
            prt("Le {}, {} dossiers ont été prélevés sur le(s) \
    service(s) {} .\n".format(collection_date,str(len(lst_id)), uf_filter)) 
            prt_lst(lst_id)
            lst_IPP = [ item[4] for item in lst_id if item[4] is not None]
            prt("{} dossiers ont un IPP.\n".format(str(len(lst_IPP))))

            # Je veux : la liste des IPP des différents patients.
            aset_of_IPP = set(lst_IPP)
            prt("Ces dossiers concernent {} patients avec un IPP".format(
                str(len(aset_of_IPP))))
            print("Ci dessous, seuls les dossiers avec erreur sont enregistrés.")
            print("Note : l'ordre de traitement des dossiers n'est pas fixe.")
            buf.important = True # force l'enregistrement du buffer.
        # Pour chaque IPP, je veux l'étude de la facture le jour donné.
        # Je limite volontairement à quelques dossiers.      
        # sub_set= list(aset_of_IPP)[4:10] # pour la mise au point
        sub_set= list(aset_of_IPP)
        errors = 0
        for IPP in sub_set:
        # for ipp in aset_IPP: 
            if IPP is not None:
                res = self.fac_de_IPP_date(IPP, collection_date)
                if res: # True si erreur
                    errors = errors +1
        with lib_smart_stdout.PersistentStdout(filename=REPORT) as buf:
            bm_u.title("Conclusion finale")
            print("Nombre d'IPP en erreur ", errors)
            ipp_verif = len(sub_set)
            print("Nombre d'IPP vérifiées", ipp_verif)
            buf.important = True
        if synthesis is not None:
            global NB_ERREUR, NB_IPP
            NB_ERREUR += errors
            NB_IPP += ipp_verif

class Synthesis():
    """Une classe pour accumuler des résultats de synthèse."""
    def __init__(self):
        pass
    def add(self, quoi, nombre):
        self.quoi +=nombre
    
def demo_poll_simple():
    """Démonstration d'un sondage sur plusieurs jours"""
    global CONNEXION
    CONNEXION = MyODBC_to_infocentre()
    global NB_ERREUR, NB_IPP # très laid

   
    NB_ERREUR = 0
    NB_IPP = 0
    for date in sequence_of_dates("01/02/2016", 1):
        self.demo_etude_facturation_d_un_jour(date,  uf_filter='6048', synthesis=True)
        # input("Etude pour "+ date + "terminée.")
    print("Nombre d'erreur totales : {} pour {} IPP". format(str(NB_ERREUR),
                                                             str(NB_IPP)))
    del(CONNEXION)

def demo_poll():
    """Démonstration d'un sondage sur plusieurs jours, répétés"""
    global CONNEXION
    global NB_ERREUR, NB_IPP # très laid
    CONNEXION = MyODBC_to_infocentre()
    days = 4
    with open(file="sondage.txt", mode='a', encoding='UTF8') as rapport:
        # je prends le premier lundi de la première semaine pleine de chaque
        # mois
        for date_in_month in [#"04/01/2016",
                              #"01/02/2016",
                              #"07/03/2016",
                              #"04/04/2016", "02/05/2016", "06/06/2016",
                              "04/07/2016", "01/08/2016", "05/09/2016",
                              #"03/10/2016", "07/11/2016", "05/12/2016";
                              ]:
            
            NB_ERREUR = 0
            NB_IPP = 0
            for date in sequence_of_dates(date_in_month, days):
                Syn().demo_etude_facturation_d_un_jour(date,  uf_filter='6048',
                                                  synthesis=True)
                # input("Etude pour "+ date + "terminée.")
            rapport.write("Nombre d'erreur totales {} : {} pour {} IPP\n". \
                           format(date_in_month, str(NB_ERREUR), str(NB_IPP)))
    del(CONNEXION)

def _test():
    """Execute doctests."""
    import doctest
    (failures, tests) = doctest.testmod(verbose=False)
    print("{} tests performed, {} failed.".format(tests, failures))
    
if __name__=='__main__':
    CONNEXION = MyODBC_to_infocentre()
    # OUTPUT_FILE=Cf.EXPORT_REP+"erreur2.txt"
    # _test()
    # Syn().fac_de_IPP_date(IPP='002135656', date = '16/10/2015') # BM en IPP
    # Syn().fac_de_IEP_date(  IEP='07190243', date = '16/10/2015') # BM en IEP 
    # Syn().fac_de_IEP_date(IEP='7694000', date= '20/04/2016') # cas 40
    Syn().fac_de_IEP_date(IEP='8060028', date= '08/09/2016') # cas 40
    # Syn().req_syn()
    # Syn().demo_etude_facturation_d_un_jour("02/06/2016",  uf_filter='6048')
    # Syn().demo_etude_facturation_d_un_jour("02/06/2016",  uf_filter=[ 6048, 2105, 'UHCD'])
    # Syn().demo_etude_facturation_d_un_jour("05/06/2016")
    # Syn().req_audit_trail_for_id('6060248167')
    # Syn().fac_de_IPP_date(IPP='0000000000001951052', date = '12/07/2016', nabm_version=43)
    # Syn().fac_de_IPP_date(IPP='100584102', date = '12/07/2016')
    # Syn().fac_de_IPP_date(IPP='1005841021', date = '12/07/2016') # requête vide, mais ne plante pas
    # Syn().fac_de_IPP_date(IPP='100584102', date = '33/07/2016') # ne plante pas.
    # Syn().fac_de_IPP_date(IPP='100584102', date = '12/07/2016')
    # Syn().fac_de_IPP_date(IPP='486423', date = '20/04/2016')

    # global NB_ERREUR, NB_IPP # très laid
    # demo_poll()


    del(CONNEXION)
