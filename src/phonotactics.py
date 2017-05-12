from fsa import FSA, FSAEdge

class Phonotactics:
    #fields: which side the stress counts from, where the placement of the primary stress is
    #how many short syllables are in a foot, phonology of an unstressed syllable,
    #phonology of a primary stress, of secondary stress, and of the bad edge
    def __init__(self,side,placement,foot,usphon,psphon,ssphon,bephon,canInsert,canDelete):
        self.side = side
        self.placement = placement
        self.foot = foot
        self.usphon = usphon
        self.psphon = addBefore(psphon,"'")
        self.ssphon = addBefore(ssphon if ssphon else psphon,",")
        self.bephon = bephon
        self.canInsert = canInsert
        self.canDelete = canDelete
    
    def prettyprint(self):
        string = "This language has "
        if 'r' in self.side.lower() and self.placement != False:
            string += " primary stress on syllable " + str(self.placement) + " from the right."
        elif 'l' in self.side.lower() and self.placement != False:
            string += " primary stress on syllable " + str(self.placement)+ " from the left."
        else:
            print string + "no stress features"
            self.usphon.prettyprint()
            return
        if self.foot != 0 and self.foot != False:
            string += " There are " + str(self.foot) + " unstressed syllables between stresses."
        print string
        if self.psphon:
            print "Primary stressed syllables are"
            self.psphon.prettyprint()
        if self.ssphon:
            print "Secondary stressed syllables are"
            self.ssphon.prettyprint()
        if self.bephon:
            if 'r' in self.side.lower():
                print "The first syllable is"
            else:
                print "The last syllable is"
            self.bephon.prettyprint()
        if self.usphon:
            print "Unstressed syllables are"
            self.usphon.prettyprint()
        if self.canInsert:
            print "You can insert an unstressed syllable with a penalty"
        if self.canDelete:
            print "You can delete an unstressed syllable with a penalty"
            
    def syllableFSA(self):
        fsa = FSA("I",[],["I"],[])
        if "n" in self.side.lower() or self.placement in [False,0]:
            fsa.addEdge("I","I",".")
            fsa.ends = ["I"]
            return fsa
        fsa.states += ["P","S"]
        if self.foot > 0:
            fsa.addString('P','S',(self.foot+1)*".",[])
            fsa.addEdge('S','P'+(self.foot+1)*"."+"1",'.')
        else:
            fsa.states += ["."]
            fsa.ends += ["."]
            fsa.addEdge("P",".",".")
            fsa.addEdge(".",".",".")
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
        if self.bephon:
            for state in fsa.states:
                if state != "EP":
                    fsa.addEdge(state,"B",".",[])
            fsa.states += ["B"]
            fsa.ends += ["B","P","EP"]
        else:
            fsa.ends = [state for state in fsa.states if "I" not in state]
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
        return fsa.crunchEdges()
    
    
def addBefore(fsa,symb):
    if isinstance(fsa,FSA):
        fsa.addEdge("new",fsa.start,symb)
        fsa.states += ["new"]
        fsa.start = "new"
    return fsa