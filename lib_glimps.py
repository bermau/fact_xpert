"""tools for Glims.

Extraire des structures d'un tableau régulier.
Extraction de champs de longueur fixe.

Les données sont issues d'un copier coller de 
Dossier/ Cotation / visualisation facture."""
 

# TODO : je n'arrive pas à saisir des structure multilignes dans les docstring pour les
# doctest. Je suis obligé de redéfinir ces 2 structures générales
struct = """
AAA 123 Ceci est le libellé 234.5
ALO 345 Ceci est une autre  124.5
"""

seps_GLIMS = [2, 9, 20, 54, 61, 67]

class Spliter():
    """split a text as the Unix function cut
    >>> seps = [0, 4, 8, 28 ]
    >>> a = Spliter(struct, seps)
    >>> a.get_fields()
    [['AAA', '123', 'Ceci est le libellé', '234.5'], \
['ALO', '345', 'Ceci est une autre ', '124.5']]
    """
 
    lines = []
    def __init__(self, struct, seps):
        self.struct = struct
        self.seps = seps        
 
    def get_fields(self):
        lst_lines = [ line  for line in self.struct.rsplit("\n") if line ]
        ar = [] # array
        limit = len(self.seps) - 1
        import pdb
        # pdb.set_trace()        
        for line in lst_lines:
            ar_line = [] # line in the array
            # print("trt", line)
            for i in range(0, len(self.seps)):
                # print("i",i)
                if i == 0:
                    ar_line.append(line[self.seps[i]: self.seps[i+1]-1])
                elif i == limit :
                    ar_line.append(line[self.seps[i]:])
                else: #cas général
                    ar_line.append(line[self.seps[i]:self.seps[i+1]-1])
            ar.append(ar_line)        
        return ar

    def print_fields(self, fields_str):
        """Frint tabulated fields"""
        for line in fields_str:
        # print(line)
            for field in line:
                print(field + "\t", end = '')
            print()
            
def delimite_format(msg):
    """Elimine les données inutiles de l'écran de facturation recueillies par 
Dossier/ Cotation / visualisation facture.
    >>> import data_for_tests as dt
    >>> delimite_format(dt.GLIMS_01_MOD_00)
    ['   B     0514       PHOSPHATASES ALCALINES (PH. AL       7.0 B       1.89 ', \
'   B     0519       GAMMA GLUTAMYL TRANSFERASE (GA       7.0 B       1.89 ']
"""
    b = [ line for line in msg.split("\n") if line != '' ]
    return b[b.index('='*80)+1:b.index('='*79)]
  

def glims_to_MOD01_format(splitted_data):
    """Convert splitted data into a fact_xpert MOD01 array."""
    A = [ line[1]  for line in splitted_data ]
    return A

def glims_to_MOD02_format(splitted_data):
    """Convert splitted data into a fact_xpert MOD02 array."""
    A = [( '1230567890', line[1], '*'+line[2], int(line[3][:-2]), line[0])  for line in splitted_data ]
    return A

def _test():
    """Execute doctests."""
    import doctest
    (failures, tests) = doctest.testmod(verbose=True)
    print("{} tests performed, {} failed.".format(tests, failures))

def demo_for_splitter():
    """Demo to use Splitter"""

    seps = [0, 5, 8, 28 ]
    struct = """
AAA 123 Ceci est le libellé 234.5
ALO 345 Ceci est une autre  124.5
"""
    
    a = Spliter(struct, seps)
    print(a.get_fields())

def demo_for_glims():
    """Demo to use Splitter with data from Glims"""
    from  data_for_tests import GLIMS_DIDIER
    import lib_glimps
    
    ar_strings = []
    a = lib_glimps.Spliter(GLIMS_DIDIER, lib_glimps.seps_GLIMS)
    ar_strings = a.get_fields()
    format_MOD02 = lib_glimps.glims_to_MOD02_format(ar_strings)
    print(format_MOD02)

    # IL RESTE A ELIMINER les blancs :
    
    
if __name__ == "__main__":
    #_test()
    demo_for_glims()
   



