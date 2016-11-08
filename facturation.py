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
import lib_smart_stdout

from bm_u import title, Buffer

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

On utilise pour cela la commande attach dans Sqlite."""
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
##        
##    def conclude(self):
##        """Imprime le rapport et le sauve éventuellement."""
##        for line in self.buf:
##            print(line)
##        if self.error == []:
##            print("rapport vide")
##        else:
##            print("Rapport à sauvegarder : ", self.buf)

    def attach_invoice_database(self):
        """Attacher la base de la facture à la base de nomenclature."""
        # ILLOGIQUE : on devrait pouvoir attacher ce qui vient de invoice.
        self.ref.execute_sql("attach database 'tempo.sqlite' as inv")
        
        # self.ref.execute_sql("attach database ':memory:' as inv")
        sys.stderr.write("Invoice db attached\n")
        
    def affiche_etude_select_OK(self, sql , comment='', param=None):
        """Affiche une liste des lignes de Select éventuellement vide.
-> Liste des résultats ou None.

        """
        if param is None:    
            self.ref.execute_sql(sql)
        else:
            self.ref.execute_sql(sql, param=param)
        res_as_list =  self.ref.resultat_req()
        
        if len(res_as_list) == 0:
            return None # Mieux que False
        else:
            self.prt_buf("{} lignes{} :".format(str(len(res_as_list)),comment))
            for line in res_as_list:
                print(str(line)+',')
            print()
            return res_as_list
        
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

Puis affiche le nombre de B."""
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
        print('')
        print('Format pour AMZ : '+ " ".join([code[1] for code in res_lst if code[1] is not None]))
        
        if res_lst:
            total_B =sum([line[3] for line in res_lst
                          if line[3] is not None ])
            print("Somme des B d'après NABM : {}".format(str(total_B)))


    def conclude(self, noerror, buffer):
        """Write a conclusion and if necessary a buffer."""
        if noerror:
            print("OK")
        else:
            print("***** Incorrect *****")
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
            res_lst, msg_buf = A
            buf.extend_buf(msg_buf)
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
                buf.print(row['code'], row['nb_letters'], row['coef'])
                buf.print("Erreur : dans l'acte {} remplacer la valeur {} par la valeur {}"\
                      .format(row['code'],row['nb_letters'],row['coef'] ))
                noerror = False
            self.conclude(noerror, buf)
            return noerror

    def verif_actes_trop_repetes(self, nabm_version=43):
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
            if (int(row['MaxCode'])> 0) and (row['occurence']> int(row['MaxCode']) ): 
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
            self.invoice.act_list)
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
            self.invoice.act_list)
        
        # Note :  response = (bool, liste)
        if response[0] :
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

Retorune True s'il y a 0 ou 1 acte 9105, False suivi du nombre si plus de 1."""
        # noerror = True
        sql = """SELECT count(code) FROM inv.invoice_list WHERE code ="9105" """
        self.ref.execute_sql(sql)
        AA = self.ref.resultat_req()
        nb = AA[0][0]
        print("Nb de 9105 : {}".format(str(nb)))
        if nb > 1:
            # Le conseil suivant est un conseil par excès.
            advice("Par précaution, limiter le nombre de 9105 à 1.")
            return False, nb
        else:
            return True
        
        
    def verif_blood_minimum(self):
        """Test la présence indue d'actes de cotation minimum.

Ce actes sont ajoutés pour la la sommes des analyses réalisées sur du sang
sot au moins égale à B20.

Renvoie True si la règle est respectée, et False sinon."""
        # Principe :
        # dan la nabm : Sang vaut 1. 
        # Faire la somme des actes Sang=1
        # lst = ['9905', '9910']
        # lst.extend([str (item) for item in range (9915, 9927)]])
        # lst_cotation_minimale = ['9905', '9910', '9915', '9916', '9917', '9918', '9919', '9920',
        #        '9921', '9922', '9923', '9924', '9925', '9926']
        # Rechercher les actes de cotation minimale, si aucun ne rien faire (Return True)
        # Si présence, rechercher la liste de codes sang et en faire le calcul
        #     si calcul = B20 => True
        #     si calcul > B20, 1) Afficher les actes de cotation minmum, afficher la somme, retourner False
             
        return True

        


    def _sql_divers(self): 
        """Recherche de codes particulier.

Pour bien tester, j'ai besoin d'actes dont le max soit de
         1, 2 et 3, voire plus."""

        # (nabm_table, incompatibilities_table) = lib_nabm.get_name_of_nabm_tables(43)
        self.prt_buf("SQL Divers");
        sql = """Select * from nabm WHERE id='1610' """
        self.ref.execute_sql(sql)
        self.prt_buf(self.ref.resultat_req())
        # Je retiens comme exemples :
        # (557, 'LITHIUM (LI , LITHIEMIE , LI SERIQUE , LI ERYTHROCYTAIRE) (SANG)', 2)
        # (1374, 'VITAMINE B 12 (DOSAGE) (SANG)', 1),
        # (1137, 'C-PEPTIDE (SANG)', 3)
        # (703, 'INSULINE LIBRE (SANG)', 3)
        # (1154, 'TEST DIRECT DE COOMBS (ANTIGLOBULINE SPECIFIQUE)', 4)
        # (274, "MYCOBACTERIE : SENSIBILITE VIS A VIS D'UN ANTIBIO PAR ANTIBIO", 5)


def get_affiche_liste_codes(code_liste):
    """Utilitaire qui retourne une liste épurée de codes.

    >>> get_affiche_liste_codes(['9105', '1104', '1610', '0126', ])
    '9105 1104 1610 0126'
    """
    return(" ".join([code for code in code_liste]))
        
DEBUG = False

# @lib_smart_stdout.record_if_true(filename='erreur.txt')
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

    T = TestInvoiceAccordingToReference(invoice, act_ref.NABM_DB,
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

    print("\nForfait Sang multiple ? :           ", end='')
    T.verif_9105_multiple()
    
    print("\nConclusion générale : ", end='')
    T.affiche_conclusion_d_un_test(main_conclusion)

    return not main_conclusion
    #T.conclude(main_conclusion)
def _demo_1_for_simple_list():
    """Exemple d'utilisation.
On définit une liste python de codes, on en choisit un (a), on teste.
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
    """Données extraites de synergy.

Une démonstration.
La facture est sur le modèle suivant dit 'MOD02'.
Chaque ligne de facture contient le numéro de dossier, nom d'acte, la lettre type,
le nombre de lettres.
La facture vient par exmeple du programme syn_odbc_connexion.py
    
"""
    title("DEMO 2")
    import data_for_tests
    model_etude_1(data_for_tests.FACT6_PROT_ERR_MONTANT_ERR,
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
    version = "Programme : " + os.path.basename(__file__)
    print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M"), end='   ')
    print(version)

def saisie_manuelle():
    """Demande une saisie manuelle et l'expertise."""
    
    print("Mode de saisie : manuel")
    saisie = input("Saisir une liste de codes séparés par des espaces ")
    # saisie.replace("  "," ")
    act_lst = [ code.rjust(4,'0') for code in saisie.split(" ") if code not in ('', ' ')]
    print(act_lst)
    model_etude_1(act_lst)
def _test():
    """Execute doctests."""
    import doctest
    (failures, tests) = doctest.testmod(verbose=False)
    print("{} tests performed, {} failed.".format(tests, failures))

if __name__=='__main__':

    _test()
    #_demo_1_for_simple_list()
    # _demo_2_data_from_synergy()
    #_demo_3_several_records_from_synergy()
    # saisie_manuelle()
    pass

## Voila ce que je veux modifier : 
##Règle des protéines :               Règle des protéines non respectée.
##
##Suggestion de correction pour les protéines.
##3 lignes classées par valeurs décroissante :
##('1817', 20, 'PREALBUMINE (DOSAGE) (SANG)'),
##('1819', 14, 'TRANSFERRINE (SIDEROPHYLLINE) (DOSAGE) (SANG)'),
##('1806', 10, 'ALBUMINE (DOSAGE) (SANG)'),
##
##*** CONSEIL *** : Garder : ['1817', '1819'] ***
##*** CONSEIL *** : Eliminer : ['1806'] ***
##
##                                        ******** incorrect ******


