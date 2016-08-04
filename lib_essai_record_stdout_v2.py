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
  
def fonction_qui_ecrit_et_fait_des_tests(msg):
    """Ecrit. Renvoie True si c'est à sauvegarder."""
    print(msg)
    return msg == "à enregistrer"

print("début")
with  PersistentStdout() as buf:
# On imprime des tas de lignes à l'écran, qui sortent mais sont stockées
    print("Aujourdh'ui c'est l'été") # ceci est capturé et affiché
    print('pas de passage ', end='')
    print("à la ligne")
    print()
    buf.important = fonction_qui_ecrit_et_fait_des_tests("à enregistrer")
    print("une petite pour la route")

print("Ceci est hors contexte et ne sera pas sauvé.")  
        
