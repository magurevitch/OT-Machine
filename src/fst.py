from .fsa import FSA, FSAEdge
from .fsm import FSM
from .weight import Weight, zeroWeight
from collections import deque

class FST(FSM):    
    def addEdge(self,frm,to,original,changed,weight=zeroWeight):
        self.edges += [FSTEdge(frm,to,original,changed,weight)]
        return self
        
    def product(self,fsa):
        start = (self.start, fsa.start)
        fsa_ = FSA(start,[],[],[])
        stack = deque([start])
        
        selfAsFromState = self.stateFrom()
        fsaAsFromState = fsa.stateFrom()
        
        while stack:
            (x,y) = stack.pop()
            if (x,y) not in fsa_.states:
                fsa_.states += [(x,y)]
                if x in self.ends and y in fsa.ends:
                    fsa_.ends += [(x,y)]
                
                partial = [FSAEdge((x,y),(selfEdge.to, fsaEdge.to),selfEdge.changed,selfEdge.weight + fsaEdge.weight)
                          for selfEdge in selfAsFromState[x]
                          for fsaEdge in [edge for edge in fsaAsFromState[y] if edge.label == selfEdge.original]
                          ]
                stack.extend([edge.to for edge in partial if edge.to != (x,y)])
                fsa_.edges += partial
        return fsa_.trim()
    
    def addString(self,frm,to,original,changed,wgt):
        length = max(len(original),len(changed))
        nuOriginal = list(original) + max(length-len(original),0) * [""] 
        nuChanged = list(changed) + max(length-len(changed),0) * [""] 
        temp = [str(frm) + original + changed + str(i) for i in range(1,length)]
        self.states += temp
        temp = zip([frm]+temp,temp+[to],nuOriginal,nuChanged)
        for (frm_,to_,original,changed) in temp:
            if to_ == to:
                self.addEdge(frm_,to_,original,changed,wgt)
            else:
                self.addEdge(frm_,to_,original,changed,[])
        return self
            
    @classmethod
    def selfLooping(cls,symbols):
        return cls(0,[0],[0],[FSTEdge(0,0,symbol,symbol,[]) for symbol in symbols])

class FSTEdge:
    def __init__(self,frm,to,original,changed,weight=zeroWeight):
        self.frm = frm
        self.to = to
        self.original = original
        self.changed = changed
        if isinstance(weight,Weight):
            self.weight = weight
        else:
            self.weight = Weight(weight)
            
    def graphviz(self):
        def graphvizstate(state):
            try:
                return '"' + str(state) + '"'
            except TypeError:
                strstate = map(str,state)
                return '"' + "".join(strstate) + '"'
        return '\n' + graphvizstate(self.frm) + " -> " + graphvizstate(self.to) + '[ label = "' + str(self.original) + " > " + str(self.changed) + "//" + str(self.weight) +  '" ];'
            
    def reverse(self):
        self.frm, self.to = self.to, self.frm
        
    def replaceState(self,old,new):
        self.frm = new if self.frm == old else self.frm
        self.to = new if self.to == old else self.to
        
    def tuple(self):
        return FSAEdge(self.frm,(self.to,),self.original,self.changed,self.weight)
        
    def __hash__(self):
        return hash((self.frm, self.to,self.original,self.changed,str(self.weight)))

    def __eq__(self, other):
        return (self.frm, self.to,self.original,self.changed,self.weight) == (other.frm, other.to,other.original,other.changed,other.weight)   