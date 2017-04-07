class Language:
    def __init__(self,phono,conjugations):
        self.phono = phono
        self.conjugations = conjugations
        
    def conjugate(self,word,conj):
        if conj in self.conjugations:
            for (name,form) in self.conjugations[conj]:
                underlying = form.replace('_',word)
                print name + ": " + underlying
                best = self.phono.best(underlying)
                print "surface forms:"
                for ps in best[1]:
                    print "  - " + ps
        else:
            print "conjugation not found"