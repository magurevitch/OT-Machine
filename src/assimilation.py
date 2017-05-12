from fsa import FSA
from weight import Weight, zeroWeight

class Assimilation:
    def __init__(self,lists,opaques=False,dissimilation=False):
        self.lists = lists
        self.opaques = opaques
        self.dissimilation = dissimilation
        
    def prettyprint(self):
        if self.dissimilation:
            print "The following is a dissimilation"
        print "The harmonic groups are:"
        for group in self.lists:
                print '/'+"/,/".join(group)+'/'
        if self.opaques == []:
            print "This harmony group only takes place in tiers"
        if self.opaques:
            print "The non-transparent elements of the harmony opaques are: /"+"/,/".join(self.opaques)+'/'
            
    def getHarmonics(self,symbols):
        allSymbols = set(item for list in self.lists for item in list)
        return allSymbols & symbols
        
    def getNeutrals(self,symbols):
        harmonics = self.getHarmonics(symbols)
        return symbols - harmonics
        
    def harmonyFSA(self,symbols,traces):
        fsa = FSA("Neutral",["Neutral"],["Neutral"],[])
        
        harmonics = self.getHarmonics(symbols)
        fsa.states += harmonics
        fsa.ends += harmonics
        
        for state1 in harmonics:
            for state2 in harmonics:
                fsa.addEdge(state1,state2,state2,[] if self.dissimilation else ["harm"])
        for list in self.lists:
            for edge in fsa.edges:
                if edge.to in list and edge.frm in list:
                    edge.weight = Weight(["harm"]) if self.dissimilation and edge.to != edge.frm else zeroWeight
        for state in fsa.states:
            if state != "Neutral":
                fsa.addEdge("Neutral",state,state)
            
        for state in fsa.states:
            fsa.addEdge(state,state,".")
            for trace in traces:
                fsa.addEdge(state,state,trace)
            fsa.addEdge(state,state,"'")
            fsa.addEdge(state,state,",")
            for neut in self.getNeutrals(symbols):
                if self.opaques == False or neut in self.opaques:
                    fsa.addEdge(state,"Neutral",neut)
                else:
                    fsa.addEdge(state,state,neut)
        return fsa