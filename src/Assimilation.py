from FSA import FSA
from Weight import Weight

class Assimilation:
    def __init__(self,lists,opaques=False):
        self.lists = lists
        self.opaques = opaques
        
    def prettyprint(self):
        print "The harmonic groups are:"
        for group in self.lists:
                print '/'+"/,/".join(group)+'/'
        if self.opaques == []:
            print "This harmony group only takes place in tiers"
        if self.opaques:
            print "The non-transparent elements of the harmony opaques are: /"+"/,/".join(self.opaques)+'/'
            
    def getHarmonics(self):
        return set([item for list in self.lists for item in list])
        
    def getNeutrals(self,symbols):
        harmonics = self.getHarmonics()
        return symbols - harmonics
        
    def harmonyFSA(self,symbols):
        fsa = FSA("Neutral",["Neutral"],["Neutral"],[])
        
        harmonics = self.getHarmonics()
        fsa.states += harmonics
        fsa.ends += harmonics
        
        for state in fsa.states:
            if state != "Neutral":
                fsa.addEdge("Neutral",state,state,[])
        for state1 in harmonics:
            for state2 in harmonics:
                fsa.addEdge(state1,state2,state2,["harm"])
        for list in self.lists:
            for edge in fsa.edges:
                if edge.to in list and edge.frm in list:
                    edge.weight = Weight([])
            
        for state in fsa.states:
            fsa.addEdge(state,state,".",[])
            fsa.addEdge(state,state,"_",[])
            for neut in self.getNeutrals(symbols):
                if self.opaques == False or neut in self.opaques:
                    fsa.addEdge(state,"Neutral",neut,[])
                else:
                    fsa.addEdge(state,state,neut,[])
        return fsa