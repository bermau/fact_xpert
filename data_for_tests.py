#!/bin/env/python3
# file: data_test.py
# Set of data for tests.

# 
actes_ok = ['0323', '9105', '1208']

actes_inconnus_512_1245_2145 = [
    '9105', '1104', '1610', '0126',
    '1127', '0174', '9005',
    '0996','0552', '1208', # err
    '0593', '0578', '0512','0352', '0353',
    '1245', # err
    '1806', '1207', '9105', '4340', '1465', '0322',
    '0323', '2145', # err
    '4332', '4355', '4362', '4362']

actes_repetes = [
    '9105', '1104', '1610', '0126', '1127', '0174', '9005',
    '0996','0552', '1208', '0593', '0578', '0352', '0353',
     '1806', '1207', '9105', '4340', '1465', '0322',
    '0323', '4332', '4355', '4362', '4362']

actes_inconnu_1515 = ['0323', '9105', '1515', '1208']

actes_703_repete_plus_de_3_fois = [ '0323','0703', '9105', '0703',
                                    '1208','0703', '0703',]
actes_703_repete_3_fois_plus_inconnu = [ '0323','0703', '9105',
                            '1806', # prot
                            '1789', # inc              
                            '1208','0703', '0703',]

actes_avec_plus_de_3_seros_hepatite =['0323', # hep
                                      '9105', '1208',
                                      '1806', # prot
                                      '1805', # prot
                                      '0353', # hep
                                      '0354', # hep
                                      '0351', # hep                                    '
                                     ]

actes_avec_plus_de_2_prots = ['0323', '9105', '1208'] # FAUX

actes_plus_2_prot_plus_3_hep_inconnu_1517_1518 = [
    '0322', # hep
    '0323', # hep
    '9105',
    '0352', # hep
    '0354', # hep
    '0354', # hep répétée
    '0324', # prot
    '1208',
    '1518', # inc
    '1808', # prot
    '1813', # prot
    '1517' # inc
    ,
    ] 
