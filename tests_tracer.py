"""Enregistrement de la trace des tests

Le but est réaliser les tests de doctest en enregistrant le résultat
dans un fichier de log, avec la date d'exécution."""

import doctest
import datetime

import facturation 
import lib_nabm
import tests # ne fonctionne pas ainsi 

LOG = "tests_log.log"

with open(LOG, mode="a", encoding="UTF8") as output:
    output.write(datetime.datetime.now().strftime("%Y-%m-%d %H:%M")+" tests \n")

    fact = doctest.testmod(m=facturation)
    output.write("fact : " + str(fact) + "\n")

    lib_na = doctest.testmod(m=lib_nabm)
    output.write("lib_nabm : " + str(lib_na) + "\n")
    
    lib_tests = doctest.testmod(m=tests)
    output.write("tests : " + str(lib_tests) + "\n")

print("Report is in {}".format(LOG))
