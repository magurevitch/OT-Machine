from FSAEdge import FSAEdge
from Weight import Weight
from PriorityQueue import PriorityQueue
import copy
from FSM import FSM

import time

class FSA(FSM):    
    def addEdge(self,frm,to,label,weight=[]):
        self.edges += [FSAEdge(frm,to,label,weight)]
        return self
        
    def product(self,fsa):
        self.crunchEdges()
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
                        if selfEdge.label == fsaEdge.label:
                            label = selfEdge.label
                            if label != '_' or (selfEdge.weight == Weight([]) or fsaEdge.weight == Weight([])):
                                toState = (selfEdge.to, fsaEdge.to)
                                stack += [toState]
                                edges += [FSAEdge((x,y),toState,label,selfEdge.weight + fsaEdge.weight)]
        return FSA(start,ends,states,edges).Trim()
        
    def replace(self,state,fsa):
        fsa = copy.deepcopy(fsa)
        for state1 in fsa.states:
            fsa.replaceState(state1,str(state) + "-" + str(state1))
        self.states += fsa.states
        if state == self.start:
            self.start = fsa.start
        if state in self.ends:
            self.ends += fsa.ends
        potential = []
        for edge in self.edges:
            if edge.to == state:
                edge.to = fsa.start
            if edge.frm == state:
                edge.frm = fsa.ends[0]
                for end in fsa.ends[1:]:
                    potential += [FSAEdge(end,edge.to,edge.label,edge.weight)]
        self.edges += potential
        self.edges += fsa.edges
        return self
    
    def addString(self,frm,to,string,wgt):
        temp = [str(frm) + string + str(i) for i in range(1,len(string))]
        self.states += temp
        temp = zip([frm]+temp,string,temp+[to])
        for item in temp:
            if item[2] == to:
                self.addEdge(item[0],item[2],item[1],wgt)
            else:
                self.addEdge(item[0],item[2],item[1],[])
        return self
        
    def Trim(self):
        stack = copy.copy(self.ends)
        fsa = copy.copy(self)
        fsa.edges = []
        fsa.states = self.ends + [self.start]
        
        while stack != []:
            now = stack.pop()
            edges = [edge for edge in self.edges if edge.to == now]
            states = [edge.frm for edge in edges if edge.frm not in fsa.states]
            fsa.edges += edges
            fsa.states += states
            stack += states
        fsa.edges = list(set(fsa.edges))
        self = fsa
        return fsa
        
    def capEnd(self):
        if len(self.ends) > 1:
            self.states += ["END"]
            for end in self.ends:
                self.edges += [FSAEdge(end,"END","_",[])]
            self.ends = ["END"]
        
    def addBlanks(self):
        for state in self.states:
            if all([edge.label != "_" for edge in self.edges if edge.frm == state]):
                self.addEdge(state,state,"_",[])
        
    def crunchEdges(self):
        scoreBoard = {}
        for edge in self.edges:
            key = (edge.frm,edge.to,edge.label)
            if key in scoreBoard:
                if edge.weight < scoreBoard[key]:
                    scoreBoard[key] = edge.weight
            else:
                scoreBoard[key] = edge.weight
        self.edges = [FSAEdge(key[0],key[1],key[2],val) for (key,val) in scoreBoard.items()]
        return self
            
    def Dijkstra(self):
        self.capEnd()
        
        queue = PriorityQueue(self.states)
        queue.update(self.start,Weight([]),[""])

        stateFrom = self.stateFrom()

        while queue:
            current = queue.pop()
            if current.weight == Weight.infiniteWeight():
                return False
            if current.label in self.ends:
                return (current.weight,current.paths)
            for edge in stateFrom[current.label]:
                if edge.to in [item.label for item in queue.list[1:]]:
                    newWeight = current.weight + edge.weight
                    label = edge.label if edge.label != '_' else ""
                    paths = list(set([path + label for path in current.paths]))
                    if newWeight < queue.getWeight(edge.to):
                        queue.update(edge.to,newWeight,paths)
                    if newWeight == queue.getWeight(edge.to):
                        paths = list(set(paths + queue.getPaths(edge.to)))
                        queue.update(edge.to,newWeight,paths)
        return False
    
    def determinize(self):
        state_transitions = {}
        epsilon_closures = {}
        
        for edge in self.edges:
            label = (edge.label,edge.weight)
            if label == ("_",Weight([])):
                if edge.frm not in epsilon_closures:
                    epsilon_closures[edge.frm] = []
                epsilon_closures[edge.frm] += [edge.to]
            else:
                if edge.frm not in state_transitions:
                    state_transitions[edge.frm] = {}
                if label not in state_transitions[edge.frm]:
                    state_transitions[edge.frm][label] = []
                state_transitions[edge.frm][label] += [edge.to]
        for closure in epsilon_closures:
            for state in epsilon_closures[closure]:
                if state in epsilon_closures:
                    epsilon_closures[closure] += [s for s in epsilon_closures[state] if s not in epsilon_closures[closure]]
        startlist = [self.start]
        if self.start in epsilon_closures:
            startlist += epsilon_closures[self.start]
        start = tuple(set(startlist))
        fsa = FSA(start,[],[],[])
        stack = [start]
        empty = []
        while stack:
            current = stack.pop()
            if current not in fsa.states and current != ():
                toStates = {}
                for state in current:
                    if state in state_transitions:
                        for label in state_transitions[state]:
                            if label not in toStates:
                                toStates[label] = []
                            toStates[label] += state_transitions[state][label]
                fsa.states += [current]
                for label in toStates:
                    newState = toStates[label]
                    for state in toStates[label]:
                        if state in epsilon_closures:
                            newState += [s for s in epsilon_closures[state] if s not in newState]
                    newState = tuple(set(sorted(newState)))
                    if newState not in fsa.states:
                        stack += [newState]
                    fsa.addEdge(current, newState, label[0], label[1])
                    if any([state in self.ends for state in newState]):
                        if newState not in fsa.ends:
                            fsa.ends += [newState]
        return fsa
    
    def equivalent(self,other):
        fsa = self.determinize()
        fsb = other.determinize()
        
        aFrom = {state : {(e.label,e.weight):e.to for e in edges} for (state,edges) in fsa.stateFrom().items()}
        bFrom = {state : {(e.label,e.weight):e.to for e in edges} for (state,edges) in fsb.stateFrom().items()}
        
        stack = [fsa.start]
        bijection = {fsa.start : fsb.start}
        while stack:
            current = stack.pop()
            aStateDict = aFrom[current]
            bStateDict = bFrom[bijection[current]]
            if sorted(aStateDict.keys()) != sorted(bStateDict.keys()):
                return False
            for label in aStateDict:
                if aStateDict[label] in bijection:
                    bState = bijection[aStateDict[label]]
                    if bState != bStateDict[label]:
                        return False
                else:
                    bijection[aStateDict[label]] = bStateDict[label]
                    stack += [aStateDict[label]]
        return sorted([bijection[end] for end in fsa.ends]) == sorted(fsb.ends)
    
    def minimize(self):
        self = self.determinize()
        self.Reverse()
        self = self.determinize()
        self.Reverse()
        self = self.determinize()
        return self
    
    @classmethod
    def fromString(cls,string):
        start = 0
        ends = [len(string)]
        states = range(len(string)+1)
        edges = [FSAEdge(i,i+1,string[i],[]) for i in range(len(string))]
        edges += [FSAEdge(i,i,"_",[]) for i in states]
        return cls(start,ends,states,edges)

    @classmethod
    #This uses the recursive Thompson algorithm
    #It doesn't take actual regular expressions,but a made up version where {} are used to mean "penalty if don't have them"
    #* to mean "the symbol after can be included with penalty or excluded", and not anything with repetition
    # and the octothorpe # to mean penalty
    def fromRegex(cls,regex):
        fsa = cls(0,['f'],[0],[])
        def ThompsonRecurse(start,end,string):
            open = max(fsa.states) + 1
            if len (string) < 1:
                fsa.quotient([end,start])
            elif string[0] in '([{':
                if string[0] == '(':
                    fsa.edges += [FSAEdge(start,open,'_',[''])]
                elif string[0] == '{':
                    fsa.edges += [FSAEdge(start,open,'_',['pen'])]
                branches = []
                remainder = ""
                state = 0
                place = 0
                while place < len(string):
                    if string[place] in ')]}':
                        if state == 1:
                            branches += [remainder]
                            break
                        else:
                            remainder += string[place]
                            state -= 1
                    elif string[place] in '([{':
                        if state != 0:
                            remainder += string[place]
                        state += 1
                    elif string[place] in '\|/' and state == 1:
                        branches += [remainder]
                        remainder = ""
                    else:
                        remainder += string[place]
                    place += 1
                remainder = string[place+1:]
                if open not in fsa.states:
                    fsa.states += [open]
                for branch in branches:
                    ThompsonRecurse(start,open,branch)
                if remainder:
                    ThompsonRecurse(open,end,remainder)
                else:
                    fsa.quotient([end,open])
            elif len(string) == 1:
                fsa.edges += [FSAEdge(start,end,string,[])]
                if open not in fsa.states:
                    fsa.states += [open]
            elif string[0] == '*':
                fsa.edges += [FSAEdge(start,open,string[1],['pen'])]
                fsa.edges += [FSAEdge(start,open,'_',[])]
                if open not in fsa.states:
                    fsa.states += [open]
                ThompsonRecurse(open,end,string[2:])
            elif string[0] == '#':
                fsa.edges += [FSAEdge(start,open,string[1],['pen'])]
                if open not in fsa.states:
                    fsa.states += [open]
                ThompsonRecurse(open,end,string[2:])
            else:
                fsa.addEdge(start,open,string[0],[])
                if open not in fsa.states:
                    fsa.states += [open]
                ThompsonRecurse(open,end,string[1:])
            return
        ThompsonRecurse(0,'f',regex)
        fsa.states += ['f']
        
        fsa.minimize()
        
        return fsa
