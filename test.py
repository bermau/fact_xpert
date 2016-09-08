#!/usr/bin/python3
# -*- coding: utf-8 -*-
""" Unittest fact_xpert."""

# Les 4 lignes suivantes sont issues du fichier parent de ce script
# Fonctionne sous Python  3.4.2 sous Linux Debian 8.1
# Fonctionne sous Python  3.4.3 sous Windows Seven
# ce fichier doit être compris dans /tests/ qui est situé avec les exécutables
# 
# v1 : jan 2016 : le test est fonctionnel sous Linux comme sous Windows
# v2 : mars 2016 : support une nouvelle architecture : /bin/, /test/, /input/,
# /output/

# Dans ces tests, les fonctions doivent retourner False s'il y a une
# anomalie dans la facture et True s'il n'y en a pas.
#
# Le jeux de données des tests est dans data_for_tests.py

import unittest, os, sys, pdb

dirname=os.path.dirname(__file__) # __file__ n'est pas défini sous IDLE 2.7. 
# if dirname=='':
#     dirname='.'
dirname=os.path.realpath(dirname)
updir=os.path.split(dirname)[0]
if updir not in sys.path:
    # updir=updir+r'/bin/'
    print("Ajout de {} à la variable PATH".format(updir)) 
    sys.path.append(updir)
                    
# à partir de maintenant on peut rechercher les modules situés
# au dessus de ce script
from data_for_tests import *
from facturation import *
from lib_nabm import *

# On définit une classe contenant les différents tests.
class CalculsTest(unittest.TestCase):
    """Cette classe contient les méthodes qui, si elles conmmencent par le mot
test, sont des tests unitaires."""
        
    @classmethod    
    def XXsetUpClass(self):
        """Crée l'environnement. Initialise des listes d'actes."""
        # Inutile pour l'instant.
        print("Setting Up Class environment")

    def setUp(self):
       """Crée l'environnemnt en ouvrant l'application et insère une chaine dans la premier fenetre"""
       print("SetUp environment")
       autre_actes_ok = ['0323', '9105', '1208']
       
    def XX_tearDown(self):
        print("Tearing down environment.\n")

                         
    def common_set_of_tests(self, facture=actes_inconnu_1515):
        """Une fonction pour aider à écrire des tests."""
        self.act_ref=Nabm() 
        self.invoice = Invoice()
        self.invoice.load_invoice_list(facture)
##        self.test = TestInvoiceAccordingToReference(self.invoice.INVOICE_DB,
##                                                    self.act_ref.NABM_DB,
##                                                    nabm_version=43)
        self.test = TestInvoiceAccordingToReference(self.invoice,
                                                    self.act_ref.NABM_DB,
                                                    nabm_version=43)
        self.test.attach_invoice_database()
    def test_01_toujours_correct(self):
        """Toujours OK"""
        print("Un message durant test01")
        self.assertTrue(True)
        print("Un autre message durant test01")
        
    def test_05_nabm(self):
        """Une facture entirèrement correcte."""
        self.common_set_of_tests(facture= actes_ok)
      
        self.assertTrue(self.test.verif_tous_codes_dans_nabm(nabm_version=43))
        self.assertTrue(self.test.verif_actes_trop_repetes(nabm_version=43))         
   
    def test_06_nabm(self):
        """Une facture avec des actes inconnus."""
        self.common_set_of_tests(facture= actes_inconnu_1515)
        self.assertFalse(self.test.verif_tous_codes_dans_nabm(nabm_version=43))
        self.assertTrue(self.test.verif_actes_trop_repetes(nabm_version=43))         

    def test_07_nabm(self):
        """Une facture avec des actes trop répétés."""
        self.common_set_of_tests(facture= actes_703_repete_plus_de_3_fois)
        self.assertTrue(self.test.verif_tous_codes_dans_nabm(nabm_version=43))
        self.assertFalse(self.test.verif_actes_trop_repetes(nabm_version=43))         

    def test_08_nabm(self):
        """Une facture avec répétitions autorisées mais un acte inconnu."""
        facture = actes_703_repete_3_fois_plus_inconnu
        self.common_set_of_tests(facture=facture)
        self.assertFalse(self.test.verif_tous_codes_dans_nabm(nabm_version=43))
        self.assertTrue(self.test.verif_actes_trop_repetes(nabm_version=43))         
        self.assertTrue(detecter_plus_de_trois_sero_hepatite_b(
             facture))
        self.assertTrue(detecter_plus_de_deux_proteines(facture))

        self.assertTrue(self.test.verif_hepatites_B())

    def test_09_nabm(self):
        """Une facture avec des erreurs hépatite B."""
        facture = actes_avec_plus_de_3_seros_hepatite
        self.common_set_of_tests(facture=facture)
        self.assertTrue(self.test.verif_tous_codes_dans_nabm(nabm_version=43))
        self.assertTrue(self.test.verif_actes_trop_repetes(nabm_version=43))
        result = detecter_plus_de_trois_sero_hepatite_b(facture)
        self.assertEqual(result, (False, ['0323', '0353', '0354', '0351']))
        self.assertTrue(detecter_plus_de_deux_proteines(facture))
        self.assertFalse(self.test.verif_hepatites_B())

    def test_10_nabm(self):
        """Une facture avec 3 types d'erreurs."""
        facture = actes_plus_2_prot_plus_3_hep_inconnu_1517_1518
        self.common_set_of_tests(facture=facture)
        self.assertFalse(self.test.verif_tous_codes_dans_nabm(nabm_version=43))
        self.assertFalse(self.test.verif_actes_trop_repetes(nabm_version=43))
        # Je ne sais pas comment ne tester que le début du tupple.
        (rep, void) = detecter_plus_de_trois_sero_hepatite_b(
            facture)
        self.assertFalse(rep)
        (rep2, void2) = detecter_plus_de_deux_proteines(facture)
        self.assertFalse(rep2)
                        
    
        
def test_suite():
    """retourne la liste des tests à traiter."""
    
    tests = [ unittest.makeSuite(CalculsTest) ]
    return unittest.TestSuite(tests)  
        
if __name__ == '__main__':
    """Programme de test de vérification de la NABM."""
    # rep=os.getcwd() 
    # print (os.path.dirname(rep))
    # os.chdir(r'..\bin')

    # import trt_vis_de_synergy
    # from filecmp import cmp    # pour comparer des fichiers.
    
    # lancer les unittest
    suite = unittest.TestLoader().loadTestsFromTestCase(CalculsTest)
    unittest.TextTestRunner(verbosity=2).run(suite)
