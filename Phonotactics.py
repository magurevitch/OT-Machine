from FSA import FSA

class Phonotactics:
    #fields: which side the stress counts from, where the placement of the primary stress is
    #how many short syllables are in a foot, phonology of an unstressed syllable,
    #phonology of a primary stress, of secondary stress, and of the bad edge
    def __init__(self,side,placement,foot,usphon,psphon,ssphon,bephon):
        self.side = side
        self.placement = placement
        self.foot = foot
        self.usphon = usphon
        self.psphon = psphon
        self.ssphon = ssphon
        self.bephon = bephon
    
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
            
    def SyllableFSA(self):
        fsa = FSA("I",["I"],["I"],[])
        if self.placement in [False,0]:
            fsa.addEdge("I","I",".",[])
            return fsa
        fsa.states += ["P","S"]
        fsa.addString('P','S',(self.foot+1)*".",[])
        fsa.addEdge('S','P'+(self.foot+1)*"."+"1",'.',[])
        fsa.addString('I','P',self.placement*".",[])
        
        fsa.states += ["EP"]
        if self.placement > 1:
            for state in fsa.states:
                if "I" in state and state != "I" + self.placement*"." + str(self.placement - 1):
                    fsa.addEdge(state,"EP",".",[])
        
        if self.bephon:
            for state in fsa.states:
                if state != "EP":
                    fsa.addEdge(state,"B",".",[])
            fsa.states += ["B"]
            fsa.ends += ["B","P","EP"]
        else:
            fsa.ends = [state for state in fsa.states if "I" not in state]
        if "r" in self.side:
            fsa.Reverse()
        return fsa
    
    def PhonotacticFSA(self):
        fsa = self.SyllableFSA()
        
        if len(fsa.states) == 1:
            fsa.Replace("I",self.usphon)
        for state in set(fsa.states):
            if "-" not in state:
                if "." in state:
                    fsa.Replace(state,self.usphon)
                elif "P" in state:
                    fsa.Replace(state,self.psphon)
                elif "B" in state:
                    fsa.Replace(state,self.bephon)
                elif "S" in state:
                    if self.ssphon:
                        fsa.Replace(state,self.ssphon)
                    else:
                        fsa.Replace(state,self.psphon)
        return fsa