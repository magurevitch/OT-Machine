from weight import Weight
from fsa import FSA, FSAEdge
from fst import FST, FSTEdge

class Phonology:
    #fields: what categories of sounds do you have, what sounds can be inserted, what changes might happen to a string, what sounds cannot be deleted
    #the phonotactics (their own object), and which order the weights are in for violations.
    def __init__(self,categories,inserts,changes,undel,phonotax,order,geminate,codas,vowels,harmonies,badstrings):
        self.categories = categories
        self.inserts = inserts
        self.changes = changes
        self.undel = undel
        self.phonotax = phonotax
        self.order = order
        self.geminate = geminate
        self.codas = codas
        self.vowels = vowels
        self.harmonies = harmonies
        self.badstrings = badstrings
        Weight.order = order
        
        #caching
        self.cachedMods = self.modificationFST()
        if self.phonotax.usphon:
            self.cachedPhonotax = self.categorizeFsa(self.phonotax.phonotacticFSA())
        self.cachedCodas = self.codasFST()
        self.cachedBad = self.badStrings()
        
    def prettyprint(self):
        print "The categories are:"
        for (cat,reps) in self.categories.iteritems():
            print cat + ": " + '/' + "/,/".join(reps) + '/'
        print "You can instert a:"
        for (cat,ins) in self.inserts.iteritems():
            if "a" in ins[1]:
                print "/" + ins[0] + "/ after a " + cat
            else:
                print "/" + ins[0] + "/ before a " + cat
        print "you can change:"
        for (bef,af) in self.changes.iteritems():
            print '/' + bef + "/ -> /" + "/,/".join(af) + '/'
        print "after", self.vowels, "you can change:"
        for (bef,af) in self.codas.iteritems():
            print '/' + bef + "/ -> /" + "/,/".join(af) + '/'
        print "You can't delete:" + ",".join(self.undel)
        print "you can save syllables by geminating: " + ",".join(self.geminate)
        self.phonotax.prettyprint()
        if self.harmonies:
            print "harmonies and assimilations are"
            for harmony in self.harmonies:
                harmony.prettyprint()
        if self.badstrings:
            print "The bad strings are " + ','.join(self.badstrings)


    def getCategories(self, symbol):
        categories = [cat for cat in self.categories if symbol in self.categories[cat]]
        return categories + [symbol]

    def modificationFST(self):
        fst = FST.selfLooping(list(self.getSymbols()) + ['_'])
        if self.undel:
            for sym in list(self.getSymbols()) + ["_"]:
                cats = self.getCategories(sym)
                if all(map(lambda x: x not in self.undel,cats)):
                    fst.addEdge(0,0,sym,'_',["del"])
        for original in self.changes:
            for changed in self.changes[original]:
                fst.addString(0,0,original,changed,["chg"])
        if self.geminate:
            for edge in tuple(fst.edges):
                cats = self.getCategories(edge.changed)
                if any(map(lambda x: x in self.geminate,cats)):
                    fst.addString(edge.frm,edge.to,edge.original,edge.changed + edge.changed,edge.weight + Weight(["ins"]))
        if self.inserts:
            for edge in tuple(fst.edges):
                cats = self.getCategories(edge.changed)
                for cat in cats:
                    if cat in self.inserts:
                        (symb,side) = self.inserts[cat]
                        string = ""
                        if "b" in side and edge.frm == 0:
                            string = symb + edge.changed
                        if "a" in side and edge.to == 0:
                            string = edge.changed + symb
                        if string != "":
                            fst.addString(edge.frm,edge.to,edge.original,string,edge.weight + Weight(["ins"]))
        return fst
        
    def codasFST(self):
        fst = FST("B",["A","E"],["B","A","E"],[])
        fst.addEdge("A","E",".","_",[])
        fst.addEdge("A","B",".",".",[])
        for symbol in list(self.getSymbols()) + ["_"]:
            if symbol in self.vowels or any([cat in self.vowels for cat in self.categories if symbol in self.categories[cat]]):
                fst.addEdge("B","A",symbol,symbol,[])
            else:
                fst.addEdge("B","B",symbol,symbol,[])
            fst.addEdge("A","A",symbol,symbol,[])
            if symbol in self.codas:
                fst.edges += [FSTEdge("A","A",symbol,changed,["chg"]) for changed in self.codas[symbol]]
        return fst
            
    def badString(self,string):
        fsa = FSA("S",["S"],["S"],[])
        fsa.addString("S","S",string,["bs"])
        for edge in tuple(fsa.edges):
            for symb in [sym for sym in self.getSymbols() if sym != edge.label]:
                fsa.addEdge(edge.frm,"S",symb,[])
        for state in fsa.states:
            fsa.addEdge(state,state,".",[])
        for edge in fsa.edges:
            if edge.label == string[0]:
                edge.to = "S" + string + "1"
            if edge.weight == Weight(["bs"]) and overlap(string,string):
                edge.to = "S" + string + str(overlap(string,string))
        fsa.ends = fsa.states
        return fsa
    
    def badStrings(self):
        fsa = FSA("I",["I"],["I"],[])
        for symb in list(self.getSymbols())+["."]:
            fsa.addEdge("I","I",symb,[])
        if(self.badstrings):
            fsa = fsa.multiproduct(map(lambda bs: self.badString(bs),self.badstrings))
        fsa = fsa.minimize()
        fsa.relabelStates()
        for state in fsa.states:
            fsa.addEdge(state,state,"_")
        return fsa
    
    # This generates the list of all surface forms that fit phonotactics, as a list of syllables, and list of penalties
    def phonologyFSA(self,string):
        fsa = FSA.fromString(string)
        
        fsa = self.cachedMods.product(fsa)
        
        fsa.edges += [FSAEdge(state,state,'.',[]) for state in fsa.states]
        fsa.edges += [FSAEdge(state,state,'_',[]) for state in fsa.states]
        fsa.crunchEdges()
        
        fsa = self.cachedPhonotax.product(fsa)
        
        fsa = fsa.determinize()
        fsa.edges = [edge for edge in fsa.edges
                     if edge.frm not in fsa.ends
                     if not(edge.frm == edge.to and edge.label == ".")
                     ]
        fsa.addEdge(fsa.start,fsa.start,"_",[])
        
        fsa = self.cachedCodas.product(fsa)
        
        symbols = set(edge.label for edge in fsa.edges) - set([".","_"])
        
        fsa = fsa.multiproduct(map(lambda x: x.harmonyFSA(symbols), self.harmonies) + [self.cachedBad])
        
        return fsa

    #This function takes the contenders, and finds the ones with the minimum penalty
    def best(self,string):
        fsa = self.phonologyFSA(string)
        
        (weight,winners) = fsa.dijkstra()
        
        if not winners:
            return ([],[])
        
        winners = [winner.replace("_","").strip(".") for winner in winners]
        winners = list(set(winners))
        
        return (str(weight),winners)
        
    def categorizeFsa(self,fsa):
        potential = []
        for edge in fsa.edges:
            if edge.label in self.categories:
                potential += [FSAEdge(edge.frm,edge.to,cat,edge.weight) for cat in self.categories[edge.label]]
            else:
                potential += [edge]
        fsa.edges = potential
        for state in fsa.states:
            fsa.addEdge(state,state,"_",[])
        return fsa
        
    def getSymbols(self):
        return set([item for list in self.categories.values() for item in list])
        
def overlap(A,B):
    for i in range(1,min(len(A),len(B))):
        if A[:i] == B[-i:]:
            return i
    return False