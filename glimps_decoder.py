

"""Extraire des structures d'un tableau régulier.
 
Extraction de champs de longueur fixe"""
 
 
struct = """
AAA 123 Ceci est le libellé 234.5
ALO 345 Ceci est une autre  124.5
"""

seps = [0, 5, 8, 28 ]

class Spliter():
    """Split a text as the Unix cut function
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

def _test():
    """Execute doctests."""
    import doctest
    (failures, tests) = doctest.testmod(verbose=True)
    print("{} tests performed, {} failed.".format(tests, failures))
 
if __name__ == "__main__":
    _test()
    
    
##    a = Spliter(struct, seps)
##    print(a.get_fields())

