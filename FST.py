from FSTEdge import FSTEdge
from FSA import FSA
from FSAEdge import FSAEdge

class FST(FSA):
    def addEdge(self,frm,to,original,changed,weight):
        self.edges += [FSTEdge(frm,to,original,changed,weight)]
        return self
        
    def Product(self,fsa):
        fsa.crunchEdges()

        start = (self.start, fsa.start)
        states = []
        ends = []
        stack = [start]
        edges = []
        while stack:
            (x,y) = stack.pop()
            if (x,y) not in states:
                states += [(x,y)]
                if x in self.ends and y in fsa.ends:
                    ends += [(x,y)]
                selfEdges = [e for e in self.edges if e.frm == x]
                fsaEdges = [e for e in fsa.edges if e.frm == y]
                for selfEdge in selfEdges:
                    for fsaEdge in fsaEdges:
                        if selfEdge.original == fsaEdge.label:
                            stack += [(selfEdge.to,fsaEdge.to)]
                            edges += [FSAEdge((x,y),(selfEdge.to,fsaEdge.to),selfEdge.changed,selfEdge.weight+fsaEdge.weight)]
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
        