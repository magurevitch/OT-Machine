from .fsa import FSA, FSAEdge

class Phonotactics:
    #fields: which side the stress counts from, where the placement of the primary stress is
    #how many short syllables are in a foot, phonology of an unstressed syllable,
    #phonology of a primary stress, of secondary stress, and of the bad edge
    def __init__(self,side,placement,foot,usphon,psphon,ssphon,bephon,canInsert,canDelete):
        self.side = side
        self.placement = placement
        self.foot = foot
        self.usphon = usphon
        if psphon:
            self.psphon = psphon.addBefore("'")
            ssphon = ssphon if ssphon else psphon
            self.ssphon = ssphon.addBefore(",")
        else:
            self.psphon = False
            self.ssphon = False
        self.bephon = bephon
        self.canInsert = canInsert
        self.canDelete = canDelete
    
    def syllableFSA(self):
        if "n" in self.side.lower() or self.placement in [False,0]:
            return FSA("I",["I"],["I"],[FSAEdge("I","I",".")])

        fsa = FSA("I",[],["P","EP"] if self.placement > 1 else ["P"],[])
        if self.foot > 0:
            fsa.states += ["S"]
            fsa.addString('P','S',(self.foot+1)*".",[])
            fsa.addEdge('S','P'+(self.foot+1)*"."+"1",'.')
        else:
            fsa.states += ["."]
            fsa.ends += ["."]
            fsa.addEdge("P",".",".")
            fsa.addEdge(".",".",".")

        if self.bephon:
            for state in fsa.states:
                fsa.addEdge(state,"B",".",[])
            fsa.states += ["B"]
            fsa.ends += ["B","P","EP"]
        else:
            fsa.ends = [state for state in fsa.states]
        fsa.states += ["I"]

        fsa.addString('I','P',self.placement*".",[])

        deletions = []
        if self.canDelete:
            deletions += [FSAEdge(e2.frm,"P",".",["pen"]) for e2 in fsa.edges for e1 in fsa.edges if e2.to == e1.frm and e1.to == "P"]
            deletions += [FSAEdge(e2.frm,"S",".",["pen"]) for e2 in fsa.edges for e1 in fsa.edges if e2.to == e1.frm and e1.to == "S"]
        if self.canInsert:
            if self.placement > 1:
                fsa.edges += [FSAEdge(e.frm,e.frm,".",["pen"]) for e in fsa.edges if e.to in ["P","S"]]
            else:
                fsa.edges += [FSAEdge(e.frm,e.frm,".",["pen"]) for e in fsa.edges if e.to == "S"]
                fsa.addString("I","P","..",["pen"])
                fsa.addEdge("I..1","I..1",".",["pen"])
        fsa.edges += deletions

        if self.placement > 1:
            for state in fsa.states:
                if "I" in state and state != "I" + self.placement*"." + str(self.placement - 1):
                    fsa.addEdge(state,"EP",".",[])
            fsa.states += ["EP"]
        for edge in fsa.edges:
            if edge.frm == "I":
                edge.label = ""
        if "r" in self.side or "R" in self.side:
            fsa.reverse()
        return fsa
    
    def phonotacticFSA(self):
        fsa = self.syllableFSA()

        if len(fsa.states) == 1:
            fsa.replace("I",self.usphon)
            
        for state in set(fsa.states):
            if "-" not in state:
                if "." in state:
                    fsa.replace(state,self.usphon)
                elif "P" in state:
                    fsa.replace(state,self.psphon)
                elif "B" in state:
                    fsa.replace(state,self.bephon)
                elif "S" in state:
                    fsa.replace(state,self.ssphon)
        fsa.relabelStates()
        return fsa.crunchEdges()