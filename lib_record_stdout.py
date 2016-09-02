"""Une classe pour enregistrer la sortie standard si nécessaire."""

# J'ai transformé cette classe avec un context manager, puis un décorateur.

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
        
    def __init__(self, filename='sortie2.txt'):
        print("Initialisation réalisée dasn __init__")
        import pdb
        pdb.set_trace()
        self.filename=filename
        self.important = False
        self.memory = StringIO()
        sys.stdout = self
                
    def write(self, s):
        """Ecrit sur la sortie standard et sur le buffer"""
        self.memory.write(s)
        self.old_stdout.write(s)

    def save_memory_to_file(self):
        with open(self.filename, 'a') as f:
            for line in self.memory.read():
                f.write(line)            
        print("SAVED in {}".format(self.filename))
    def stop_and_get(self):
        sys.stdout = self.old_stdout
        self.memory.seek(0)
        if self.important:
            self.save_memory_to_file()

# Sur les décorateurs avec arguments, 
# lire http://gillesfabio.com/blog/2010/12/16/python-et-les-decorateurs/
def record_if_important(filename='toto.txt'):
    """Enregistrement conditionnel de la sortie standard d'une fonction.

Enregistre la sortie standard si le résultat de la fonction est True.
"""
    def decorated(funct):
        print("Je décore la fonction : '{}()'".format(funct.__name__))
        def wrapper(*args, **kwargs): # indispensable pour récupérer les arguments
                                      # de la fonction
            print("Ceci est avant enregistrement")
            print("Je vais exécuter la fonction")
            a = list(args)
            print("Liste des arguments :", a)
            with  PersistentStdout(filename=filename) as buf:
                  buf.important = funct(*args, **kwargs)
            print("Ceci est après enregistrement")
            return buf.important
        return wrapper # et non pas wrapper()
    return decorated   # ni decorated()

@record_if_important()  
def fonction_qui_ecrit_et_fait_des_tests(msg):
    """Ecrit quelque chose. Renvoie True si c'est à sauvegarder."""
    print(msg)
    print("ceci est une ligne intéressante... ou non, en fonction\
    d'un test")
    return msg == "à enregistrer"   


if __name__ == '__main__':

    fonction_qui_ecrit_et_fait_des_tests("NON à enregistrer")
    fonction_qui_ecrit_et_fait_des_tests("NON enregistrer")

    fonction_qui_ecrit_et_fait_des_tests("à enregistrer")
    fonction_qui_ecrit_et_fait_des_tests("NON enregistrer")
    print("une petite ligne pour la route")
    
##    with  PersistentStdout() as buf:
##    # On imprime des tas de lignes à l'écran, qui sortent et sont stockées
##        print("Aujourdh'ui c'est l'été") # ceci est capturé et affiché
##        print('pas de passage ', end='')
##        print("à la ligne")
##        print()
##        buf.important = fonction_qui_ecrit_et_fait_des_tests("à enregistrer")
##        print("une petite pour la route")
##    print("Ceci est hors contexte et ne sera pas sauvé.")  
            
