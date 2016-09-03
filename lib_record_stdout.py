"""Une classe pour enregistrer la sortie standard si nécessaire."""

# J'ai transformé cette classe avec un context manager, puis un décorateur.

import sys
from io import StringIO
 
class PersistentStdout(object):
    """Un buffer pour enregistrer la sortie standard.

la sortie standard ne sera sauvé que si self.important est True.

Cette classe fonctionne en contexte manager.
Le contexte manager nécessite l'usage :
for XXX as f:
   dans le contexte
Le contexte manager exécute automatiquement les fonctions __enter__ (en entrée)
et __exit__ (en sortie).
"""

    old_stdout = sys.stdout
    
    def __init__(self, filename='sortie2.txt'):
        sys.stderr.write("Dans PersistentStdout.__init__\n")
        self.filename=filename
        self.important = False
        self.memory = StringIO()
        sys.stdout = self  

    def __enter__(self):
        sys.stderr.write("Dans PersistentStdout.passe par __enter__\n")
        return self # permet la notation "with XX as f"
    
    def __exit__(self, *args, **kwargs):
        self.stop_and_get()
        sys.stderr.write("sortie par __exit__\n")
                
    def write(self, s):
        """Ecrit sur la sortie standard et sur le buffer"""
        self.memory.write(s)
        self.old_stdout.write(s)

    def save_memory_to_file(self):
        with open(self.filename, 'a') as f:
            for line in self.memory.read():
                f.write(line)            
        sys.stderr.write("Info saved in {}\n".format(self.filename))
        
    def stop_and_get(self):
        sys.stdout = self.old_stdout
        self.memory.seek(0)
        if self.important:
            self.save_memory_to_file()

# Sur les décorateurs avec arguments, 
# lire http://gillesfabio.com/blog/2010/12/16/python-et-les-decorateurs/
def record_if_important(filename='sortie2.txt'):
    """Enregistrement conditionnel de la sortie standard d'une fonction.

Enregistre la sortie standard si le résultat de la fonction est True.
"""
    def decorated(funct):
        print("Dans decorated")
        # print("Je décore la fonction : '{}()'".format(funct.__name__))
        def wrapper(*args, **kwargs): # indispensable pour récupérer les arguments
                                      # de la fonction
            print("Dans decorated, dans wrapper")
            # a = list(args)
            print("Liste des arguments de : {} : {}".format(funct.__name__, list(args)))
            with PersistentStdout(filename=filename) as buf:
                  buf.important = funct(*args, **kwargs)
            print("Ceci est après enregistrement")
            return buf.important
        return wrapper # et non pas wrapper()
    return decorated   # ni decorated()

@record_if_important(filename='ma_sortie.txt')  
def fonction_qui_ecrit_et_fait_des_tests(msg):
    """Ecrit quelque chose. Renvoie True si c'est à sauvegarder."""
    print(msg)
    print("ceci est une ligne intéressante... ou non, en fonction\
d'un test")
    return msg == "à enregistrer"   

def _demo_context_manager():
    print("ligne 1 à ne pas retenir")
    with PersistentStdout() as buf:
        print("ligne 2 à retenir")
        print("ligne 3 à retenir")
        buf.important = True # on force la sauvegarde
    print("ligne 4 à ne pas retenir")  
        
def _demo_decorator():
    fonction_qui_ecrit_et_fait_des_tests("NON à enregistrer (1)")
    fonction_qui_ecrit_et_fait_des_tests("à enregistrer")
    fonction_qui_ecrit_et_fait_des_tests("NON à enregistrer (2)")
    fonction_qui_ecrit_et_fait_des_tests("NON à enregistrer (3)")
    print("une petite ligne pour la route")
     

if __name__ == '__main__':
    # _demo_context_manager()  
    _demo_decorator()
