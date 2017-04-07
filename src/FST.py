from FSTEdge import FSTEdge
from FSAEdge import FSAEdge
from FSA import FSA
from FSM import FSM

class FST(FSM):    
    def addEdge(self,frm,to,original,changed,weight=[]):
        self.edges += [FSTEdge(frm,to,original,changed,weight)]
        return self
        
    def product(self,fsa):
        fsa.crunchEdges()

        start = (self.start, fsa.start)
        states = []
        ends = []
        stack = [start]
        edges = []
        
        selfAsFromState = self.stateFrom()
        fsaAsFromState = fsa.stateFrom()
        
        while stack:
            (x,y) = stack.pop()
            if (x,y) not in states:
                states += [(x,y)]
                if x in self.ends and y in fsa.ends:
                    ends += [(x,y)]
                
                selfEdges = selfAsFromState[x]
                fsaEdges = fsaAsFromState[y]
                
                for selfEdge in selfEdges:
                    for fsaEdge in fsaEdges:
                        if selfEdge.original == fsaEdge.label:
                            label = selfEdge.changed
                            toState = selfEdge.to, fsaEdge.to
                            stack += [toState]
                            edges += [FSAEdge((x,y),toState,label,selfEdge.weight+fsaEdge.weight)]
        return FSA(start,ends,states,edges).Trim()
    
    def addString(self,frm,to,original,changed,wgt):
        length = max(len(original),len(changed))
        original = original.ljust(length,'_')
        changed = changed.ljust(length, '_')
        temp = [str(frm) + original + changed + str(i) for i in range(1,length)]
        self.states += temp
        temp = zip([frm]+temp,temp+[to],original,changed)
        for item in temp:
            if item[1] == to:
                self.addEdge(item[0],item[1],item[2],item[3],wgt)
            else:
                self.addEdge(item[0],item[1],item[2],item[3],[])
        return self
            
    @classmethod
    def selfLooping(cls,symbols):
        return cls(0,[0],[0],[FSTEdge(0,0,symbol,symbol,[]) for symbol in symbols])        