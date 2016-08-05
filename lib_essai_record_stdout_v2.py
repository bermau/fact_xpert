"""Une classe pour enregistrer temporairement la sortie standard"""

import sys
from io import StringIO
 
class PersistentStdout(object):
    """Un buffer pour enregistrer la sortie standard.

Je l'ai transformé en contexte manager.
Le contexte manager nécessite l'usage :
for XXX as f:
   dans le contexte
Le contexte manager exécute automatiquement les fonctions __enter__ (en entrée)
et __exit__ (en sortie).
"""

    old_stdout = sys.stdout
  
    def __enter__(self):
   
        self.__init__()
        print("passe par __enter__")
        return self # permet la notation "with XX as f"
    
    def __exit__(self, *args, **kwargs):
        
        self.stop_and_get()
        print("sortie par __exit__")
        
    def __init__(self):
        print("Initialisation réalisée dasn __init__")
        self.important = False
        self.memory = StringIO()
        sys.stdout = self
        
    def write(self, s):
        """Ecrit sur la sortie standard et sur le buffer"""
        self.memory.write(s)
        self.old_stdout.write(s)

    def save_memory_to_file(self,filename='sortie.txt'):
        with open('sortie.txt', 'a') as f:
            for line in self.memory.read():
                f.write(line)            
        
    def stop_and_get(self):
        sys.stdout = self.old_stdout
        self.memory.seek(0)
        if self.important:
            self.save_memory_to_file()



def decor(funct):
    print("Je décore la fonction : '{}()'".format(funct.__name__))
    def wrapper(*args, **kwargs): # indispensable pour récupérer les arguments de
                                  # la fonction
        print("PRE")
        print("Je vais exécuter la fonction")
        a=list(args)
        print("Liste des arguments :", a)
        with  PersistentStdout() as buf:
              buf.important = funct(*args, **kwargs)
        print("POST")
        return buf.important
    return wrapper # et non pas wrapper()

@decor  
def fonction_qui_ecrit_et_fait_des_tests(msg):
    """Ecrit. Renvoie True si c'est à sauvegarder."""
    print(msg)

    print("ceci est une ligne intéressante... ou non, en fonction\
    d'un test")
    return msg == "à enregistrer"   

# Ci dessous j'essai de créer un décorateur
def mon_deco_recorder(function):
    def wrapper(*args, **kwargs):
        print("prétraitement")
        sys.stderr.write("entrée dans wrapper")
        with PersistentStdout() as buf:
            print("indicateur dans with")
            buf.important = function(*args, **kwargs)
            sys.stderr.write("sortie de with")
        # print("post traitement")
    sys.stderr.write("Dans le décorateur")   
    return wrapper 

def decorate(func):
    def wrapper(*args, **kwargs):
        # Pré-traitement
        func(*args, **kwargs)
        # Post-traitement
    return wrapper

print("début")
##<<<<<<< HEAD
####with  PersistentStdout() as buf:
##### On imprime des tas de lignes à l'écran, qui sortent mais sont stockées
####    print("Aujourdh'ui c'est l'été") # ceci est capturé et affiché
####    print('pas de passage ', end='')
####    print("à la ligne")
####    print()
####    buf.important = fonction_qui_ecrit_et_fait_des_tests("à enregistrer")
####    print("une petite pour la route")
####
####print("Ceci est hors contexte et ne sera pas sauvé.")  
####        
####print("\n\n autres méthode ")
##
##a= mon_deco_recorder(fonction_qui_ecrit_et_fait_des_tests("à enregistrer"))
##=======


fonction_qui_ecrit_et_fait_des_tests("NON à enregistrer")



with  PersistentStdout() as buf:
# On imprime des tas de lignes à l'écran, qui sortent mais sont stockées
    print("Aujourdh'ui c'est l'été") # ceci est capturé et affiché
    print('pas de passage ', end='')
    print("à la ligne")
    print()
    buf.important = fonction_qui_ecrit_et_fait_des_tests("à enregistrer")
    print("une petite pour la route")

print("Ceci est hors contexte et ne sera pas sauvé.")  
        