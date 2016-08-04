"""Une classe pour enregistrer temporairement la sortie standard"""

import sys
from io import StringIO
 
class PersistentStdout(object):
    """Un buffer pour enregistrer la sortie standard."""
    old_stdout = sys.stdout

    def __init__(self):

        self.memory = StringIO()  # la VO utilisait BytesIO()
        sys.stdout = self
        
    def write(self, s):

        self.memory.write(s)
        self.old_stdout.write(s)

    def stop_and_get(self):
        sys.stdout = self.old_stdout
        self.memory.seek(0)
        return self.memory.read()
  
def fonction_qui_ecrit_et_fait_des_tests(msg):
    """Ecrit. Renvoie True si c'est à sauvegarder."""
    print(msg)
    return msg == "à enregistrer"

buf = PersistentStdout()
# On imprime des tas de lignes à l'écran, qui sortent mais sont stockées
 
print("Aujourdh'ui c'est l'été") # ceci est capturé et affiché
print('pas de passage ', end='')
print("à la ligne")
print()


with open('sortie.txt', 'a') as f:
    if fonction_qui_ecrit_et_fait_des_tests("à enregistrer"):
        for line in buf.stop_and_get():
            f.write(line)
    if fonction_qui_ecrit_et_fait_des_tests("pas à enregistrer"):

        
