from FSA import FSA

class Assimilation:
    def __init__(self,lists,tier=False):
        self.lists = lists
        self.tier = tier
        
    def prettyprint(self):
        print "The harmonic groups are:"
        for group in self.lists:
                print '/'+"/,/".join(group)+'/'
        if self.tier:
            print "The non-transparent elements of the harmony tier are: /"+"/,/".join(self.tier)+'/'
            
    def getHarmonics(self):
        return set([item for list in self.lists for item in list])
        
    def getNeutrals(self,langauge):
        symbs = langauge.getSymbols()
        harmonics = self.getHarmonics()
        return symbs - harmonics
        
    def harmonyFSA(self,language):
        fsa = FSA("Neutral",["Neutral"],["Neutral"],[])
        
        harmonics = self.getHarmonics()
        fsa.states += harmonics
        fsa.ends += harmonics
        
        for state in fsa.states:
            fsa.addEdge("Neutral",state,state,[])
        for state1 in harmonics:
            for state2 in harmonics:
                fsa.addEdge(state1,state2,state2,["harm"])
        for list in self.lists:
            for edge in fsa.edges:
                if edge.to in list and edge.frm in list:
                    edge.weight = []
            
        for state in fsa.states:
            fsa.addEdge(state,state,".",[])
            fsa.addEdge(state,state,"_",[])
            for neut in self.getNeutrals(language):
                if self.tier:
                    fsa.addEdge(state,state,neut,[])
                else:
                    fsa.addEdge(state,"Neutral",neut,[])
        return fsa