"""Une classe pour enregistrer la sortie standard si nécessaire."""

# J'ai transformé cette classe avec un context manager, puis un décorateur.

import sys
from io import StringIO
 
class PersistentStdout(object):
    """Un buffer pour enregistrer la sortie standard.

la sortie standard ne sera sauvée que si self.important est True.

Cette classe fonctionne en contexte manager.
Le contexte manager nécessite l'usage :
with XXX as f:
   dans le contexte
Le contexte manager exécute automatiquement les fonctions __enter__ (en entrée)
et __exit__ (en sortie).
"""

    old_stdout = sys.stdout
    
    def __init__(self, filename='essai_sortie.txt'):
        # sys.stderr.write("Dans PersistentStdout.__init__\n")
        self.filename=filename
        self.important = False
        self.memory = StringIO()
        sys.stdout = self  

    def __enter__(self):
        # sys.stderr.write("Dans PersistentStdout.passe par __enter__\n")
        return self # permet la notation "with XX as f"
    
    def __exit__(self, *args, **kwargs):
        self.stop_and_get()
        # sys.stderr.write("sortie par __exit__\n")
                
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
def record_if_true(filename='essai_sortie2.txt'):
    """Enregistrement conditionnel de la sortie standard d'une fonction.

Enregistre la sortie standard si le résultat de la fonction est True.
"""
    def decorated(funct):
        def wrapper(*args, **kwargs): # indispensable pour récupérer les arguments
                                      # de la fonction
            with PersistentStdout(filename=filename) as buf:
                  buf.important = funct(*args, **kwargs)
            return buf.important
        return wrapper # et non pas wrapper()
    return decorated   # ni decorated()

# Je me susi rendu compte que la logique de la fonction ci dessus était fausse.
# la fonction ci dessous est OK.
def record_if_false(filename='essai_sortie2.txt'):
    """Enregistrement conditionnel de la sortie standard d'une fonction.

Enregistre la sortie standard si le résultat de la fonction est False.
"""
    def decorated(funct):
        def wrapper(*args, **kwargs): # indispensable pour récupérer les arguments
                                      # de la fonction
            retour = None
            with PersistentStdout(filename=filename) as buf:
                  retour = funct(*args, **kwargs)
                  buf.important = (retour != True)             
            return retour
        return wrapper # et non pas wrapper()
    return decorated   # ni decorated()



@record_if_true(filename='essai_ma_sortie.txt')  
def fonction_qui_ecrit_et_fait_des_tests(msg):
    """Ecrit quelque chose. Renvoie True si c'est à sauvegarder."""
    print(msg)
    print("ceci est une ligne intéressante... ou non, en fonction \
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
    """Exemple de fonctionnement :
Si la fonction_qui_écrit_et_fait_des_tests, reçoit l'argument "à enregistrer",
alors elle retourne True et le décorateur @record_if_true écrit le
rapport dans le fichier indiqué."""
    fonction_qui_ecrit_et_fait_des_tests("NON à enregistrer (1)")
    fonction_qui_ecrit_et_fait_des_tests("à enregistrer")
    fonction_qui_ecrit_et_fait_des_tests("NON à enregistrer (2)")
    fonction_qui_ecrit_et_fait_des_tests("NON à enregistrer (3)")
    print("une petite ligne pour la route")
     

if __name__ == '__main__':
    # _demo_context_manager()  
    _demo_decorator()
