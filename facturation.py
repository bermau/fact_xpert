#!/bin/env/python3
# file: lib_facturation.py
# Utilitaires pour la gestion de la facturation

"""La table de référence est dans une base sqlite qui n'est jamais modifiée.
Elle peut même être protégée en écriture, ce qui garantit son intégrité.
La facture à vérifier est écrite dans une base sqlite temporaire.
La fonction SQL attache permet de réaliser des opérations entre les 2 bases."""

# Les mots PEU EFFICIENT indique les axes d'améliorations

import sys, os , datetime
import lib_sqlite
import sqlite3
import lib_nabm 
import conf_file as Cf
import lib_invoice
from lib_smart_stdout import record_if_false, record_if_true
import lib_fix_os
from bm_u import title, Buffer

DEBUG = False


def sub_title(msg):
    print("     **** "+msg+" ***")

def advice(msg):
    print(get_advice(msg))

def get_advice(msg):
    return "*** CONSEIL *** : " + msg + " ***"    

# ATTENTION : une fonction du même nom est dans syn_odbc_connexion
def quoted_joiner(lst):
    """
    >>> quoted_joiner([ 6048, 2015, 'UHCD'])
    "'6048', '2015', 'UHCD'"
    
"""
    quoted_strings_lst = [ "'"+str(code)+"'" for code in lst] 
    return ", ".join(quoted_strings_lst)


class TestInvoiceAccordingToReference():
    """Tests d'une facture selon une référence.

La base contenant la nomenclature n'est jamais modifiée.
A la base de référence (REF) contenant la nomenclature,
on attache une base temporaire contenant la facture, ce qui permet
d'utiliser des instruction SQL.

On utilise pour cela la commande attach dans Sqlite.

Attention aux arguments : REF_DB est l'objet python qui gère la base sqlite
contenant les données du référentiel. Par exemple REF_DB est lib_nabm.Nabm()"""

    def __init__(self, invoice, REF_DB, nabm_version):
        """Enregistrement de 2 connecteurs"""

        self.ref = REF_DB
        self.nabm_version = nabm_version
        (self.nabm_table,
         self.incompatibility_table) = lib_nabm.get_name_of_nabm_files(nabm_version)
        print((self.nabm_table,self.incompatibility_table))
        self.invoice = invoice
        self.report = []
        self.buf = [] # buffer pour toutes les impressions temporaires.
        self.error = 0 # Nombre de résultats anormaux.
        self.debug = True
        
    def prt_buf(self, msg):
        """Imprimer dans un buffer ou ailleurs."""
        # self.buf.append(msg)
        print(msg)

    def affiche_conclusion_d_un_test(self, rep):
        """Affiche la conclusion d'un test en clair à l'utilisateur."""
        if rep:
            print("correct")
        else:
            print("\n"+" "*40 + "******** incorrect ******")

    def attach_invoice_database(self):
        """Attacher la base de la facture à la base de nomenclature."""
        # ILLOGIQUE : on devrait pouvoir attacher ce qui vient de invoice.
        
        self.ref.execute_sql("attach database 'tempo.sqlite' as inv")
        
        # self.ref.execute_sql("attach database ':memory:' as inv")
        if DEBUG : sys.stderr.write("Invoice db attached\n")
        
    def affiche_etude_select(self, sql , comment='', param=None):
        """Affiche une liste des lignes de Select éventuellement vide.
-> None ou Liste des résultats et liste de commentaires.

        """
        buf = Buffer()
        if param is None:    
            self.ref.execute_sql(sql)
        else:
            self.ref.execute_sql(sql, param=param)
        res_as_list =  self.ref.resultat_req()
        
        if len(res_as_list) == 0:
            return None # Mieux que False
        else:
            buf.print("{} lignes{} :".format(str(len(res_as_list)),comment))
            for line in res_as_list:
                buf.print(str(line)+',')
            buf.print()
            return res_as_list, buf.msg_lst
                
    def affiche_liste_et_somme_theorique(self, nabm_version=43, verbose=None):
        """"Les actes sont-ils dans la nomenclature.

Puis affiche le nombre de B.
retourne le total de B """
        total_B = 0
        req = """
        SELECT
           inv.invoice_list.id,
           inv.invoice_list.code,
           N.libelle AS 'libelle_NABM',
           N.coef
        FROM inv.invoice_list
        LEFT JOIN {nabm_table} AS N 
        ON inv.invoice_list.code=N.code 
""".format(nabm_table=self.nabm_table)
        buf = Buffer()
        try:
                
            res_lst, comments = self.affiche_etude_select(req, comment=' dans la facture')
            if comments:
                buf.extend(comments)
                buf.show()
            if res_lst is None:
                return
            if verbose:
                print('')
                print('Format python :')
                print(res_lst)
                
            # print('Format pour AMZ : '+ " ".join([code[1] for code in res_lst if code[1] is not None]))
            # print()

            if res_lst:
                total_B =sum([line[3] for line in res_lst
                              if line[3] is not None ])
                print("Somme des B d'après NABM : {}".format(str(total_B)))
        except:
            total_B = None
        return total_B

    def conclude(self, noerror, buffer):
        """Write a conclusion and if necessary a buffer from Buffer"""
        if noerror:
            print("ok")
        else:
            print("INCORRECT <<<************")
            buffer.show()

    def verif_tous_codes_dans_nabm(self, nabm_table=None):
        """"Les actes sont-ils présents dans la nomenclature ?

Recherche des lignes absentes de la NABM.
S'il y a des lignes qui n'existent pas dans la nabm retourne False, sinon True"""
        buf = Buffer()
        noerror = True
        if nabm_table is None:
            nabm_table=self.nabm_table
        req = """
        SELECT
           inv.invoice_list.id,
           inv.invoice_list.code,
           N.libelle AS 'libelle_NABM',
           N.coef
        FROM inv.invoice_list
        LEFT JOIN {} AS N 
        ON inv.invoice_list.code=N.code
        WHERE N.libelle IS NULL
""".format(nabm_table)
        
        A = self.affiche_etude_select(req, comment=" hors NABM")
        if A is None:
            pass
        else:
            res_lst, msg_lst = A
            buf.extend(msg_lst)          
            noerror = False
        buf.show()
        self.conclude(noerror, buf)
        return noerror

            
    def verif_codes_et_montants(self, nabm_version=43):
        """Test de la valeur des codes.
possible si MOD02
-> True si valeur normales (pas d'anomale), sinon False."""
        buf = Buffer()
        if self.invoice.model_type !='MOD02':
            print("Vérification du montant impossible \
sur les factures de type MOD01.")
            # raise ValueError('Verification du montant impossible')
            return True # A améliorer.
        else:
            sql = """SELECT I.code, I.nb_letters, I.letter, N.coef
                     FROM inv.invoice_list AS I
                     LEFT JOIN {} AS N
                     ON I.code=N.code
                     WHERE I.nb_letters <> N.coef
                     OR I.letter <>N.lettre
                     """.format(self.nabm_table)
            self.ref.con.row_factory = sqlite3.Row
            cur = self.ref.con.cursor()
            cur.execute(sql)
            noerror = True
            for row in cur:
                buf.print("Acte\t|Fact.\t|Max\t|")
                buf.print(row['code'],"\t|"+str(row['nb_letters']), "\t|"+str(row['coef']),"\t|")
                buf.print("Erreur : dans l'acte {} remplacer la valeur {} par la valeur {}"\
                      .format(row['code'],row['nb_letters'],row['coef'] ))
                noerror = False
            self.conclude(noerror, buf)
            return noerror

    def verif_actes_trop_repetes(self, nabm_version=Cf.NABM_DEFAULT_VERSION):
        """Test de codes répétés.

-> True si pas d'anomalie, False sinon."""
        noerror = True
        buf = Buffer()
        req="""SELECT  I.code, count(I.code) AS 'occurence', N.MaxCode
               FROM inv.invoice_list AS I
               LEFT JOIN {ref_name} AS N ON I.code = N.code
               GROUP BY I.code    
               HAVING occurence> 1""".format(ref_name=self.nabm_table)
        
        # self.ref instance d'objet qui contient le connecteur con.
        self.ref.con.row_factory = sqlite3.Row
        cur = self.ref.con.cursor()
        cur.execute(req)
       
        for row in cur:
            buf.print("Le code {} est répété {} fois (maximum admis : {})".format(
                row['code'], row['occurence'], row['MaxCode']))
            if (int(row['MaxCode'])> 0) and (int(row['occurence'])> int(row['MaxCode']) ): 
                noerror = False
                buf.print(get_advice("Supprimer un ou des codes :\
{} (Maximum admis : {})". format(row['code'],row['MaxCode'])))            
        self.conclude(noerror, buf)
        return noerror

    
    def _buf_order_by_value(self, act_lst, max_allowed):
        """print acts ordered by value.
        > _buf_order_by_value(['0323', '0322', '0354', '0353'], 3)
        test remis à plus tard
        """
        buf = Buffer()
        req = """
        SELECT
           N.code, N.coef, N.libelle AS 'libelle_NABM'
        FROM {table} AS N
        WHERE N.code in ({my_list}) 
        ORDER BY N.coef DESC
        """.format(table=self.nabm_table, my_list=quoted_joiner(act_lst))

        # MODIFIER : 
        
        res_lst, msg_lst = self.affiche_etude_select(req,
                                    comment=' classées par valeurs décroissante')

        buf.extend(msg_lst)
        col0 = [ ligne[0] for ligne in res_lst ]
        les_plus_chers = col0[0:max_allowed]
        buf.print(get_advice("Garder : "  + str(les_plus_chers)))
        les_moins_chers = col0[max_allowed:]
        buf.print(get_advice("Eliminer : "  + str(les_moins_chers)))
        return buf

    def get_buf_recommandation_erreur_hepatites(self, act_lst):
        """Renvoie un buffer de messages d'une solution pour la règle des séro hépatites."""
        buf = Buffer()
        buf.print(get_advice("Suggestion de correction pour les sérologies hépatites."))
        buf.extend_buf(self._buf_order_by_value(act_lst, 3))
        return buf

    def get_buf_recommandation_erreur_proteines(self, act_lst):
        """Renvoie un buffer de messages d'une solution la règle des protéines."""
        buf = Buffer()
        buf.print(get_advice("Suggestion de correction pour les protéines."))
        buf.extend_buf(self._buf_order_by_value(act_lst, 2))
        return buf 
         
    def verif_hepatites_B(self):
        """Test s'il n'y a pas plus de 3 codes de la liste des hépatites.

Renvoie True si oui, et False s'il y a plus de 3 codes."""
        buf = Buffer()
        response = lib_nabm.detecter_plus_de_trois_sero_hepatite_b(
            self.invoice.act_lst)
        # ATTENTION:  response = (bool, liste)
        noerror = True
        if response[0] :
            pass 
        else:
            print("Règles de hépatites non respectée : {}\n".format(response[1]))
            buf.extend_buf(self.get_buf_recommandation_erreur_hepatites(response[1]))
            noerror = False
        self.conclude(noerror, buf)
        return noerror
        
    def verif_proteines(self):
        """Test s'il n'y a pas plus de 2 codes de la liste des protéines.

Renvoie True si oui, et False s'il y a plus de 2 codes."""
        
        buf = Buffer()
        noerror = True
        
        response = lib_nabm.detecter_plus_de_deux_proteines(
            self.invoice.act_lst)
        if response[0]:  # Note :  response = (bool, liste)
            pass
        else:
            buf.print("Règle des protéines non respectée.")
            buf.extend_buf(self.get_buf_recommandation_erreur_proteines(response[1]))
            noerror = False
        self.conclude(noerror, buf)
        return noerror
                      
    def verif_compatibilites(self):
        """Test la présence d'incompabilités.
Retourne True si aucune, et False s'il y a des incompatibilités."""
        noerror = True
        buf = Buffer()
        sql = """SELECT I.code, INC.incompatible_code
                 FROM inv.invoice_list AS I
                 JOIN {} AS INC
                 ON I.code=INC.code
                 """.format(self.incompatibility_table)
        self.ref.con.row_factory = sqlite3.Row
        cur = self.ref.con.cursor() # NE SERT à RIEN ICI ??
        cur.execute(sql)
        for row in cur:
            # print(row['code'], row['incompatible_code'])
            # PEU EFFICIENT : lance une seconde requête.
            cur2 = self.ref.con.cursor()
            sql2 = """SELECT * FROM inv.invoice_list
WHERE code = '{}' """ .format(str(row['incompatible_code']).rjust(4,"0"))
            cur2.execute(sql2)
            for row2 in cur2:                
                buf.print("\n          ***** Erreur d'incompatibilité    ****")
                # PEU EFFICIENT :  MAL ECRIT.
                buf.print("Acte {} {} {} codé par {} ". format(row2[2],
                                                             row2[5],
                                                             row2[4],
                                                             row2[3]))
                noerror = False
        if not noerror:
            buf.print(get_advice("Conserver l'acte le plus cher."))
        self.conclude(noerror, buf)
        return noerror
    
    def verif_9105_multiple(self):
        """Test la présence de plus de 1 acte 9105.

note : il existe une ambiguité sur l'autorisation de coter plusieurs fois
cet acte sur une même journée, en particulier si le patient est venu plusieurs
fois. Le logiciel de Fides semble refuser ces factures.

retourne True s'il y a 0 ou 1 acte 9105, False si plus de 1."""
        
        # noerror = True
        sql = """SELECT count(code) FROM inv.invoice_list WHERE code ="9105" """
        self.ref.execute_sql(sql)
        AA = self.ref.resultat_req()
        nb = AA[0][0]
        print("Nb de 9105 : {}".format(str(nb)))
        if nb > 1:
            # Le conseil suivant est un conseil par excès.
            advice("Par précaution, limiter le nombre de 9105 à 1.")
            return False
        else:
            return True
        
        
    def verif_minimum_sang(self):
        """Test la présence indue d'actes de cotation minimum.

Ces actes sont ajoutés pour que la somme des analyses réalisées sur du sang
soit au moins égale à B20. Attention il ne faut pas compter les actes de
type forfait Sang 9105 ou forfait préanalytique (9005)

Renvoie True si la règle est respectée, et False sinon."""
        # Principe :
        # dans la nabm : la colonne Sang indique 1 s'il s'agit d'un ex. sanguin.
        # Rechercher les actes de cotation minimale,
        # si aucun ne rien faire (Return True)       
        # Si présence, rechercher la liste de codes sang et en faire le calcul
        #   si calcul = B20 => True
        #   si calcul différent de B20, 1) Afficher les actes de cotation
        #                 minmum, afficher la somme, retourner False 
        # return True
        buf = Buffer()
        noerror = True 
        
        if lib_nabm.contient_acte_de_cotation_minimale(self.invoice.act_lst):         
# somme des valeurs des B de type Sang.                     
# Il ne me semble pas normale que l'acte 9105  (forfait Sang) soit considéré comme Sang 
            sql ="""SELECT
        sum(N.coef)

        FROM {table} AS N
        WHERE N.code in ({my_list})
        AND N.Sang = 1
        AND N.code != 9105
        
        """.format(table=self.nabm_table, my_list=quoted_joiner(self.invoice.act_lst))

            cur = self.ref.con.cursor()
            cur.execute(sql)
            my_sum = cur.fetchone()[0]
            buf.print("Total des cotations sang : {}".format(my_sum))
            if my_sum != 20:
                noerror = False
            
        self.conclude(noerror, buf)
        return noerror

def get_affiche_liste_codes(code_liste):
    """Utilitaire qui retourne une liste épurée de codes.

    >>> get_affiche_liste_codes(['9105', '1104', '1610', '0126', ])
    '9105 1104 1610 0126'
    """
    return(" ".join([code for code in code_liste]))
        
DEBUG = False

record_if_true(filename='PRIVATE/erreurs.txt')
def model_etude_1(act_lst, label=None, model_type='MOD01',
                  nabm_version=Cf.NABM_DEFAULT_VERSION):
    """Une expertise mieux présentée.
Permet de spécifier la date de NABM à utiliser. 
Retourne True si erreur, False sinon."""
    if label:
        print(label)
    main_conclusion = True
    print_version_and_date()
    if DEBUG:
        print("ACTES etudiés", act_lst)
    
    act_ref = lib_nabm.Nabm()
    invoice = lib_invoice.Invoice(model_type=model_type)
    invoice.load_invoice_list(act_lst)
# bizarre : 
#    T = TestInvoiceAccordingToReference(invoice, act_ref.NABM_DB,
#                                        nabm_version=nabm_version

    T = TestInvoiceAccordingToReference(invoice, act_ref,
                                        nabm_version=nabm_version)
    T.attach_invoice_database()
    title("Explication des actes")
    T.affiche_liste_et_somme_theorique()
    title("Vérifications")
    
    print("\nCodes existants dans la NABM :      ", end='')    
    resp1 = T.verif_tous_codes_dans_nabm()
    main_conclusion = main_conclusion and resp1
    
    print("\nRépétition de codes :               ", end='')
    resp2 = T.verif_actes_trop_repetes()
    main_conclusion = main_conclusion and resp2

    print("\nForfait Sang multiple ? :           ", end='')
    T.verif_9105_multiple()

    print("\nRègle des sérologies hépatite B :   ", end='')
    resp3 = T.verif_hepatites_B()
    main_conclusion = main_conclusion and resp3

    print("\nRègle des protéines :               ", end='')
    resp4 = T.verif_proteines()
    main_conclusion = main_conclusion and resp4

    print("\nMontants :                          ", end='')
    resp5 = T.verif_codes_et_montants()
    main_conclusion = main_conclusion and resp5
    
    print("\nIncompatilibités :                  ", end='')
    resp6 = T.verif_compatibilites()   
    main_conclusion = main_conclusion and resp6
    
    print("\nConclusion générale : ", end='')
    T.affiche_conclusion_d_un_test(main_conclusion)

    return not main_conclusion
    #T.conclude(main_conclusion)

# Modèle 2 : plus compacte.
# J'inverse la logique de sortie

# @lib_smart_stdout.record_if_false(filename='PRIVATE/erreur2.txt')
def model_etude_2(act_lst, label=None, model_type='MOD01',
                  nabm_version=Cf.NABM_DEFAULT_VERSION):
    """Une expertise compacte avec sortie détaillée en cas d'erreur.
Permet de spécifier la date de NABM à utiliser. 

si pas d'erreur : return True,
si erreur : retourne False + liste erreur
"""

    if label:
        title(label)
    main_conclusion = True
    print_version_and_date()
    if DEBUG:
        print("ACTES etudiés", act_lst)
    
    act_ref = lib_nabm.Nabm()
    invoice = lib_invoice.Invoice(model_type=model_type)
    invoice.load_invoice_list(act_lst)
    
    T = TestInvoiceAccordingToReference(invoice, act_ref,
                                        nabm_version=nabm_version)
    T.attach_invoice_database()
    title("Explication des actes")
    T.affiche_liste_et_somme_theorique()
    title("Vérifications")
    
    print("Codes existants dans la NABM :      ", end='')    
    nabm = T.verif_tous_codes_dans_nabm()
    main_conclusion = main_conclusion and nabm
    
    print("Répétition de codes :               ", end='')
    repet = T.verif_actes_trop_repetes()
    main_conclusion = main_conclusion and repet

    print("Forfait Sang multiple ? :           ", end='')
    sang = T.verif_9105_multiple()
    main_conclusion = main_conclusion and sang
    # on ne garde le nombre que si sup à 1.
    if (sang != True): sang=sang[1] # simplification de la réponse
    
    print("Règle des sérologies hépatite B :   ", end='')
    hep_b = T.verif_hepatites_B()
    main_conclusion = main_conclusion and hep_b

    print("Règle des protéines :               ", end='')
    prot = T.verif_proteines()
    main_conclusion = main_conclusion and prot

    print("Montants :                          ", end='')
    mont = T.verif_codes_et_montants()
    main_conclusion = main_conclusion and mont
    
    print("Incompatilibités :                  ", end='')
    incomp = T.verif_compatibilites()   
    main_conclusion = main_conclusion and incomp

    print("Conclusion générale : ", end='')
    T.affiche_conclusion_d_un_test(main_conclusion)
    print("Valeur de Main_conlusion ", main_conclusion)

    ret_dict = {'nabm': nabm, 'repet':repet, 'sang':sang, 'hep_b':hep_b,
                'prot':prot, 'mont':mont, 'incomp':incomp}
    
    if main_conclusion: # Retourne True si pas d'erreur, 
        return main_conclusion
    else:
        return (main_conclusion, ret_dict) # False + erreurs si erreur.

@record_if_false(filename='PRIVATE/erreur2.txt')
def model_etude_3(act_lst, label=None, model_type='MOD01',
                  nabm_version=Cf.NABM_DEFAULT_VERSION):
    """comme modèle 2 mais avec contamin . 

si pas d'erreur : return True,
si erreur : retourne False
   Parameters
   ----------
   act_lst : list of acts

   label : a comment to pritn

   model_type :  (MOD01 (default) our MOD02)

   nabm_version : version of NABM to use

   Returns
   -------
   True if no error.
   False i
   f error.

   Exammples
   ---------
   >>> import data_for_tests as dt
   >>> _model_etude_mise_a_point_cota_min(dt.FACT5_NABM43_PLUS_SANG, model_type='MOD02') #doctest: +ELLIPSIS
   ﻿VERSION : 0.15
   ...
   False
   >>> _model_etude_mise_a_point_cota_min(dt.FACT5, model_type='MOD02') #doctest: +ELLIPSIS
   ﻿VERSION : 0.15
   ...
   True
   
   
"""
    DEBUG = True 
    
    if label:
        title(label)
    main_conclusion = True
    print_version_and_date()
    if DEBUG:
        print("ACTES etudiés", act_lst)
    
    act_ref = lib_nabm.Nabm()
    invoice = lib_invoice.Invoice(model_type=model_type)
    invoice.load_invoice_list(act_lst)
    
    T = TestInvoiceAccordingToReference(invoice, act_ref,
                                        nabm_version=nabm_version)
    T.attach_invoice_database()

    title("Explication des actes")
    T.affiche_liste_et_somme_theorique()

    title("Vérifications")
    print("Codes existants dans la NABM :      ", end='')    
    nabm = T.verif_tous_codes_dans_nabm()
    main_conclusion = main_conclusion and nabm
    
    print("Répétition de codes :               ", end='')
    repet = T.verif_actes_trop_repetes()
    main_conclusion = main_conclusion and repet

    print("Forfait Sang multiple ? :           ", end='')
    sang = T.verif_9105_multiple()
    main_conclusion = main_conclusion and sang
    # on ne garde le nombre que si sup à 1.
    # if (sang != True): sang=sang[1] # simplification de la réponse
    
    print("Règle des sérologies hépatite B :   ", end='')
    hep_b = T.verif_hepatites_B()
    main_conclusion = main_conclusion and hep_b

    print("Règle des protéines :               ", end='')
    prot = T.verif_proteines()
    main_conclusion = main_conclusion and prot

    print("Montants :                          ", end='')
    mont = T.verif_codes_et_montants()
    main_conclusion = main_conclusion and mont
    
    print("Incompatilibités :                  ", end='')
    incomp = T.verif_compatibilites()   
    main_conclusion = main_conclusion and incomp
    
    print("Exces de minimum de cotation        ", end='')  
    cotamin = T.verif_minimum_sang() 
    main_conclusion = main_conclusion and cotamin

    ret_dict = {'nabm': nabm, 'repet':repet, 'sang':sang, 'hep_b':hep_b,
                'prot':prot, 'mont':mont, 'incomp':incomp, 'cotamin':cotamin}
    
    if main_conclusion: # Retourne True si pas d'erreur, 
        return main_conclusion
    else:
        return (main_conclusion, ret_dict) # False + erreurs si erreur.

    
@record_if_true(filename='PRIVATE/erreurs.txt')
def model_etude_4(act_lst, label=None, model_type='MOD01',
                  nabm_version=Cf.NABM_DEFAULT_VERSION):
    """comme modèle 4 mais plus consis, et plus lisible en sortie.
    

si pas d'erreur : return False, (inversé par rapport à mod_3)
si erreur : retourne True 
    Parameters
    ----------
    act_lst : list of acts

    label : a comment to pritn
 
    model_type :  (MOD01 (default) our MOD02)
 
    nabm_version : version of NABM to use
 
    Returns
    -------
    False if no error.
    True if error.

    Exammples
    ---------
   
    >>> import data_for_tests as dt
    >>> model_etude_4(dt.FACT5_NABM43_PLUS_COTAMIN_EN_TROP, model_type='MOD02') #doctest: +ELLIPSIS
    VERSION : 0.15
    ...
    True

    >> model_etude_4(dt.FACT5, model_type='MOD02') #doctest: +ELLIPSIS
    VERSION : 0.15
    ...
    False
    
"""
    DEBUG = False

    ret_dict = {} # les réponses

    main_conclusion = False # Absence d'erreur car cette fonction
                            # est un détecteur d'erreur   
    if label: title(label)
    if DEBUG:
        print("ACTES etudiés : ", act_lst, "Fin DEBUG")
    act_ref = lib_nabm.Nabm()
    
    invoice = lib_invoice.Invoice(model_type=model_type)
    invoice.load_invoice_list(act_lst)
    T = TestInvoiceAccordingToReference(invoice, act_ref,
                                        nabm_version=nabm_version)
    T.attach_invoice_database()
    
    title("Vérifications")
    
    print("{:<40} : ".format("Forfait Sang multiple ? "), end='')  
    sang = not(T.verif_9105_multiple()) # renvoie un False si erreur (anciennement
    # {False, 3} ou [True si E ; donc inverses la logique pour la rendre humaine
    
    main_conclusion = main_conclusion or sang
    ret_dict['sang'] = sang

    # Les autres tests sont sur le même motif
    # a series of similar tests.
    legends = [ "Codes existants dans la NABM",
               "Répétition de codes",
               "Règle des sérologies hépatite B",
               "Règle des protéines",
               "Montants",
               "Incompatilibités", 
               "Exces de minimum de cotation",
               ]
    tests = [T.verif_tous_codes_dans_nabm,
             T.verif_actes_trop_repetes,
             T.verif_hepatites_B,
             T.verif_proteines,
             T.verif_codes_et_montants,
             T.verif_compatibilites,
             T.verif_minimum_sang             
             ]
    
    variables = ['nabm', 'repet', 'hep_b', 'prot', 'mont', 'incomp', 'cotamin']
     
    print("\n{:<40} : ".format("Somme des actes"), end='')
    ret_dict['sum'] = T.affiche_liste_et_somme_theorique()
    
    for legend, test, var in zip(legends, tests, variables):
        print("{:<40} : ".format(legend), end='')
        ret_dict [var] = not(test()) # LE test renvoie False si erreur or je veux l'inverse
        main_conclusion = main_conclusion or ret_dict [var]
        if DEBUG : print(main_conclusion, ret_dict)
    if DEBUG :
        print(main_conclusion, ret_dict)
        print(len(ret_dict))

    return (main_conclusion, ret_dict) # False + erreurs si erreur.


def _demo_1_for_simple_list():
    """Exemple d'utilisation.
On définit une liste python de codes, on en choisit un (a), on teste.

ME SEMBLE A ELIMINER
"""
    title("DEMO 1")
    import data_for_tests

    # On peut aussi utiliser les listes déja programmées comme en dédiésant
    model_1 = data_for_tests.acts_ok
    # model_1 a = lib_nabm.PROT_LST_REF
    # model_1 = data_for_tests.data_for_tests.acts_prots_false_hep_b_false_and_unknown_1517_1518
    # model_1 a = data_for_tests.acts_with_more_than_3_hep_B_serologies
    model_etude_1(model_1, model_type='MOD01')

def _demo_2_data_from_synergy():
    """Données extraites antérieurement de synergy.

Une démonstration.
La facture est sur le modèle suivant dit 'MOD02'.
Chaque ligne de facture contient le numéro de dossier, nom d'acte, la lettre type,
le nombre de lettres.
La facture vient par exemeple du programme syn_odbc_connexion.py
    
"""
    title("DEMO 2")
    import data_for_tests
    model_etude_3model_etude_1(data_for_tests.FACT6_PROT_ERR_MONTANT_ERR,
                  model_type='MOD02',
                  nabm_version=42)

def _demo_3_several_records_from_synergy():
    """ Traitement de plusieurs factures de suite.

But : Eviter de refermer la base si possible."""
    title("DEMO 3 : several_record_form_synergy")
    import data_for_tests    
    #model_etude_1(data_for_tests.FACT1, model_type='MOD02')
    model_etude_1(data_for_tests.FACT1_ERR_0578, model_type='MOD02')
    # la ligne suivant ne fonctionne pas : 
    model_etude_1(data_for_tests.FACT1_ERR_0578, model_type='MOD02',
                  nabm_version=41)
    #model_etude_1(data_for_tests.FACT2, model_type='MOD02')
    #model_etude_1(data_for_tests.FACT3, model_type='MOD02')
    model_etude_1(data_for_tests.FACT1_CA_578_rep, model_type='MOD02')
   
def print_version_and_date():
    """Print version and execution datetime"""
    fileprg = "Programme : " + os.path.basename(__file__)
    # version
    with open ('versions.txt') as f:
        line = f.readline().rstrip('\n')
        print(line)   
    # datetime    
    print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M"), end='   ')
    print(fileprg)

def __cota_mini():
    print()
    title("Forfait sang par excès")
    import data_for_tests    

    model_etude_4(data_for_tests.FACT5_NABM43_PLUS_SANG,
                  model_type='MOD02',
                  nabm_version=43)

    
def saisie_manuelle():
    """Demande une saisie manuelle et l'expertise."""
    
    print("Mode de saisie : manuel")
    saisie = input("""Saisir une liste de codes actes séparés par des espaces
Formats acceptés : 512 0512
""")
    # saisie.replace("  "," ")
    act_lst = [ code.rjust(4,'0') for code in saisie.split(" ") if code not in ('', ' ')]
    print(act_lst)
    model_etude_1(act_lst)
    
def _test():
    """Execute doctests."""
    import doctest
    (failures, tests) = doctest.testmod(verbose=True)
    print("{} tests performed, {} failed.".format(tests, failures))
    print()
    title("Tests terminés")



if __name__=='__main__':
    import data_for_tests as dt

    # But : que model retourne un tuple True/False + dictionnaire
    # Il s'agit d'un détecteur d'erreur.
    # Je veux une expression "humaine" : 
    # 0 ou False indique une absence d'erreur de facturation
    # un nombre non égal à éro ou True indique une erreur de facturation
    
    # AA = model_etude_4(dt.FACT5_NABM43_PLUS_COTAMIN_EN_TROP, model_type='MOD02')

    AA = model_etude_4(dt.FACT5_NABM44_AVEC_MINIMUM_SANG_OK, model_type='MOD02')
    print(AA) 
    #_test()
  
    #import doctest
    #doctest.run_docstring_examples(model_etude_4, globals(), True, __name__)

    
##    _demo_1_for_simple_list()
##    _demo_2_data_from_synergy()
##    _demo_3_several_records_from_synergy()
    # saisie_manuelle()
##        import data_for_tests    
##    model_etude_2(data_for_tests.FACT1, model_type='MOD02')
##    model_etude_2(data_for_tests.FACT1_ERR_0578, model_type='MOD02')
    
   # __cota_mini()
    

