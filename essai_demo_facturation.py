"""Demonstration du module de facturation.

Demande une saisie d'acte et lance l'expertise."""

import facturation
def lancer1():
    print("menu1")
def quitter():
    print("quitter")
    
class Menu():
    """Un petit menu pour gérer quelques paramètres"""
    def __init__(self):
        pass
    def print_menu(self):

        lst_menu = [
["1", "saisir séquence d'acte", lancer1],
#"2",["Saisir version de NABM", lancer2],
#"E", ["Lancer l'expertise", lancer3],
["Q", "Quitter",quitter],
]  
        dic_menu = dict()
        print(dic_menu)
        
        def menu():
##            print("""
##1) saisir séquence d'acte
##2) Saisir version de NABM
##E) Lancer l'expertise
##Q) Quitter
##""")
            for (lettre, texte, action) in lst_menu:
                print(lettre + ' ' + texte)
            rep = input ("Choix")
            return rep

        rep =''
        while rep != 'Q':
            rep= menu()
            print('OK')
            
        print("Sortie par Quitter")

if __name__ == '__main__':
    Menu().print_menu()
                  
  #   facturation.saisie_manuelle()
                  

