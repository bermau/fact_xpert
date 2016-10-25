#!/usr/bin/python3
# -*- coding: utf-8 -*-
""" Unittest fact_xpert."""

# Dans ces tests, les fonctions doivent retourner False s'il y a une
# anomalie dans la facture et True s'il n'y en a pas.
#
# Le jeux de données des tests est dans data_for_tests.py

import unittest, os, sys, pdb
import lib_invoice

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
       """Crée l'environnemnt en ouvrant l'application et insère une chaine dans
la premier fenetre"""
       print("SetUp environment")
       autre_actes_ok = ['0323', '9105', '1208']
       
    def XX_tearDown(self):
        print("Tearing down environment.\n")

                         
    def common_set_of_tests(self, facture=acts_unknown_1515, model_type='MOD01',
                            nabm_version=43):
        """Une fonction pour aider à écrire des tests."""
        self.act_ref=Nabm()
        print("La facture étudiée est ", facture)
        self.invoice = lib_invoice.Invoice(model_type=model_type)
        self.invoice.load_invoice_list(facture)
        self.test = TestInvoiceAccordingToReference(self.invoice,
                                                    self.act_ref.NABM_DB,
                                                    nabm_version=nabm_version)
        self.test.attach_invoice_database()
        
    def test_01_toujours_correct(self):
        """Toujours OK"""
        self.assertTrue(True)
          
    def test_05_tout_correct(self):
        """Une facture entièrement correcte."""
        self.common_set_of_tests(facture= acts_ok)
        self.assertTrue(self.test.verif_tous_codes_dans_nabm())
        self.assertTrue(self.test.verif_actes_trop_repetes(nabm_version=43))         
   
    def test_06_actes_inconnus(self):
        """Une facture avec des actes inconnus."""
        self.common_set_of_tests(facture=acts_unknown_1515)
        self.assertFalse(self.test.verif_tous_codes_dans_nabm())
        self.assertTrue(self.test.verif_actes_trop_repetes(nabm_version=43))         

    def test_07_actes_trop_repetes(self):
        """Une facture avec des actes trop répétés."""
        self.common_set_of_tests(facture= acts_703_more_than_thrice)
        self.assertTrue(self.test.verif_tous_codes_dans_nabm())
        self.assertFalse(self.test.verif_actes_trop_repetes(nabm_version=43))         

    def test_08_err_repetition_inconnu(self):
        """Une facture avec répétitions non autorisées mais un acte inconnu."""
        facture = acts_703_more_than_thrice_plus_unknown
        self.common_set_of_tests(facture=facture)
        self.assertFalse(self.test.verif_tous_codes_dans_nabm())
        self.assertFalse(self.test.verif_actes_trop_repetes(nabm_version=43))         
        self.assertTrue(detecter_plus_de_trois_sero_hepatite_b(
             facture))
        self.assertTrue(detecter_plus_de_deux_proteines(facture))
        self.assertTrue(self.test.verif_hepatites_B())

    def test_09_err_hep_B(self):
        """Une facture avec des erreurs hépatite B."""
        facture = acts_with_more_than_3_hep_B_serologies
        self.common_set_of_tests(facture=facture)
        self.assertTrue(self.test.verif_tous_codes_dans_nabm())
        self.assertTrue(self.test.verif_actes_trop_repetes(nabm_version=43))
        result = detecter_plus_de_trois_sero_hepatite_b(facture)
        self.assertEqual(result, (False, ['0323', '0353', '0354', '0351']))
        self.assertTrue(detecter_plus_de_deux_proteines(facture))
        self.assertFalse(self.test.verif_hepatites_B())

    def test_10_trois_type_d_erreurs(self):
        """Une facture avec 3 types d'erreurs."""
        facture = acts_prots_false_hep_b_false_and_unknown_1517_1518
        self.common_set_of_tests(facture=facture)
        self.assertFalse(self.test.verif_tous_codes_dans_nabm())
        self.assertFalse(self.test.verif_actes_trop_repetes(nabm_version=43))
        # Je ne teste que le début du tupple.
        (rep, void) = detecter_plus_de_trois_sero_hepatite_b(
            facture)
        self.assertFalse(rep)
        (rep2, void2) = detecter_plus_de_deux_proteines(facture)
        self.assertFalse(rep2)

    def test_11_err_prot_sur_MOD02(self):
        """Facture avec une facture de type MOD02.
Erreur prot"""
        # facture = FACT6_PROT_ERR
        self.common_set_of_tests(facture=FACT6_PROT_ERR_MONTANT_ERR,
                                 nabm_version=42,
                                 model_type='MOD02'
                                 )
        self.assertTrue(self.test.verif_tous_codes_dans_nabm())
        self.assertFalse(self.test.verif_codes_et_montants(nabm_version=42))
        self.assertTrue(self.test.verif_hepatites_B())
        self.assertFalse(self.test.verif_proteines())
        
    def test_err_prot_et_hepatite_sur_MOD02(self):
        """Facture avec une facture de type MOD02.
Erreur prot et erreur hépatites"""
        # facture = FACT6_PROT_ERR
        self.common_set_of_tests(facture=FACT6_PROT_ERR_HEP_ERR_MONTANT_ERR,
                                 nabm_version=42,
                                 model_type='MOD02'
                                 )
        self.assertTrue(self.test.verif_tous_codes_dans_nabm())
        self.assertFalse(self.test.verif_codes_et_montants(nabm_version=42))
        self.assertFalse(self.test.verif_hepatites_B())
        self.assertFalse(self.test.verif_proteines())
        
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
