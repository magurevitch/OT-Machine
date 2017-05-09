from weight import Weight, zeroWeight, infiniteWeight
from priority_queue import PriorityQueue
from fsm import FSM
from collections import deque

class FSA(FSM):    
    def addEdge(self,frm,to,label,weight=zeroWeight):
        self.edges += [FSAEdge(frm,to,label,weight)]
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

                partial = [FSAEdge((x,y),(selfEdge.to, fsaEdge.to),selfEdge.label,selfEdge.weight + fsaEdge.weight)
                          for selfEdge in selfAsFromState[x]
                          for fsaEdge in [edge for edge in fsaAsFromState[y] if edge.label == selfEdge.label]
                          if selfEdge.label != '_' or zeroWeight in [selfEdge.weight,fsaEdge.weight]
                          ]
                stack.extend([edge.to for edge in partial if edge.to != (x,y)])
                fsa_.edges += partial
        return fsa_.trim()
    
    def replace(self,state,fsa):
        def newState(state1):
            return str(state) + "-" + str(state1)
        self.states += [newState(state1) for state1 in fsa.states]
        if state == self.start:
            self.start = newState(fsa.start)
        if state in self.ends:
            self.ends += [newState(state1) for state1 in fsa.ends]
        potential = []
        for edge in self.edges:
            if edge.to == state:
                edge.to = newState(fsa.start)
            if edge.frm == state:
                edge.frm = newState(fsa.ends[0])
                potential += [FSAEdge(newState(end),edge.to,edge.label,edge.weight) for end in fsa.ends]
        self.edges += potential
        self.edges += [FSAEdge(newState(edge.frm),newState(edge.to),edge.label,edge.weight) for edge in fsa.edges]
        return self
    
    def addString(self,frm,to,string,wgt):
        temp = [str(frm) + string + str(i) for i in range(1,len(string))]
        self.states += temp
        temp = zip([frm]+temp,temp+[to],string)
        for (frm_,to_,label) in temp:
            if to_ == to:
                self.addEdge(frm_,to_,label,wgt)
            else:
                self.addEdge(frm_,to_,label)
        return self
        
    def trim(self):
        stack = deque()
        stack.append(set(self.ends))
        goodStates = set(self.ends + [self.start])
                
        while stack:
            now = stack.pop()
            states = set(edge.frm for edge in self.edges if edge.to in now and edge.frm not in goodStates)
            if states:
                stack.append(states)
            goodStates |= states
        self.states = list(goodStates)
        self.edges = [edge for edge in self.edges if edge.to in goodStates]
        return self
        
    def capEnd(self):        
        if len(self.ends) > 1:
            self.states += ["END"]
            for end in self.ends:
                self.edges += [FSAEdge(end,"END","_")]
            self.ends = ["END"]
        
    def addBlanks(self):
        for state in self.states:
            if all([edge.label != "_" for edge in self.edges if edge.frm == state]):
                self.addEdge(state,state,"_")
        
    def crunchEdges(self):
        scoreBoard = {}
        for edge in self.edges:
            key = (edge.frm,edge.to,edge.label)
            if key not in scoreBoard or edge.weight < scoreBoard[key]:
                scoreBoard[key] = edge.weight
        self.edges = [FSAEdge(frm,to,label,val) for ((frm,to,label),val) in scoreBoard.iteritems()]
        return self
            
    def dijkstra(self):
        if len(self.ends) == 0:
            return (False,False)
        
        queue = PriorityQueue(self.states)
        queue.update(self.start,zeroWeight,[""])

        stateFrom = self.stateFrom()

        while queue:
            current = queue.pop()
            if current.weight == infiniteWeight:
                return (False,False)
            if current.label in self.ends:
                return (current.weight,current.paths)
            for edge in stateFrom[current.label]:
                if edge.to in queue:
                    newWeight = current.weight + edge.weight
                    queueWeight = queue.getWeight(edge.to)
                    if newWeight <= queueWeight:
                        paths = [path + edge.label for path in current.paths]
                        if newWeight == queueWeight:
                            paths += queue.getPaths(edge.to)
                        queue.update(edge.to,newWeight,paths)
        return False
    
    def determinize(self):
        state_transitions = {}
        epsilon_closures = {}
        
        for edge in self.edges:
            label = (edge.label,edge.weight)
            if label == ("_",zeroWeight):
                epsilon_closures[edge.frm] = epsilon_closures.get(edge.frm,[]) + [edge.to]
            else:
                if edge.frm not in state_transitions:
                    state_transitions[edge.frm] = {}
                state_transitions[edge.frm][label] = state_transitions[edge.frm].get(label,[]) + [edge.to]
        for closure in epsilon_closures:
            for state in epsilon_closures[closure]:
                if state in epsilon_closures:
                    epsilon_closures[closure] += [s for s in epsilon_closures[state] if s not in epsilon_closures[closure]]
        startlist = [self.start]
        if self.start in epsilon_closures:
            startlist += epsilon_closures[self.start]
        start = tuple(set(startlist))
        fsa = FSA(start,[],[],[])
        stack = deque([start])
        empty = []
        while stack:
            current = stack.pop()
            if current not in fsa.states and current != ():
                toStates = {}
                for state in current:
                    if state in state_transitions:
                        for label in state_transitions[state]:
                            toStates[label] = toStates.get(label,[]) + state_transitions[state][label]
                fsa.states += [current]
                for label in toStates:
                    newState = toStates[label]
                    for state in toStates[label]:
                        if state in epsilon_closures:
                            newState += [s for s in epsilon_closures[state] if s not in newState]
                    newState = tuple(set(sorted(newState)))
                    if newState not in fsa.states:
                        stack.append(newState)
                    fsa.addEdge(current, newState, label[0], label[1])
                    if any([state in self.ends for state in newState]):
                        if newState not in fsa.ends:
                            fsa.ends += [newState]
        return fsa
    
    def equivalent(self,other):
        fsa = self.determinize()
        fsb = other.determinize()
        
        aFrom = {state : {(e.label,e.weight):e.to for e in edges} for (state,edges) in fsa.stateFrom().iteritems()}
        bFrom = {state : {(e.label,e.weight):e.to for e in edges} for (state,edges) in fsb.stateFrom().iteritems()}
        
        stack = [fsa.start]
        bijection = {fsa.start : fsb.start}
        while stack:
            current = stack.pop()
            aStateDict = aFrom[current]
            bStateDict = bFrom[bijection[current]]
            if set(aStateDict.keys()) != set(bStateDict.keys()):
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
        self.reverse()
        self = self.determinize()
        self.reverse()
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
        if not regex:
            return False
        
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
                fsa.addEdge(start,open,string[0])
                if open not in fsa.states:
                    fsa.states += [open]
                ThompsonRecurse(open,end,string[1:])
            return
        ThompsonRecurse(0,'f',regex)
        fsa.states += ['f']
        
        fsa = fsa.minimize()
        
        return fsa
    
    def multiproduct(self,fsas):
        start = (self.start,) + tuple(fsa.start for fsa in fsas)
        fsa_ = FSA(start,[],[],[])
        stack = deque([start])
    
        statesFrom = (self.stateFrom(True),) + tuple(fsa.stateFrom() for fsa in fsas)
        
        while stack:
            current = stack.pop()
            if current not in fsa_.states:
                fsa_.states += [current]
                if all([x in fsa.ends for (x, fsa) in zip(current,[self] + fsas)]):
                    fsa_.ends += [current]
                currentEdges = [sf[x] for (x, sf) in zip(current,statesFrom)]
            
                partial = reduce(lambda xs,ys:
                                 [FSAEdge(current,x.to +(y.to,),x.label,x.weight+y.weight)
                                  for x in xs
                                  for y in [edge for edge in ys if x.label == edge.label]
                                  if x.label != '_' or zeroWeight in [x.weight,y.weight]
                                  ], 
                                 currentEdges)
            
                stack.extend([edge.to for edge in partial if edge.to != current])
                fsa_.edges += partial
        return fsa_.trim()
    
class FSAEdge:
    #weights are state the edge comes from, state it goes to, label, and weight
    def __init__(self,frm,to,label,weight=zeroWeight):
        self.frm = frm
        self.to = to
        self.label = label
        if isinstance(weight,Weight):
            self.weight = weight
        else:
            self.weight = Weight(weight)
        
    def prettyprint(self):
        if self.weight == zeroWeight:
            print "(" + str(self.frm) + "," + str(self.to) + "::" + str(self.label) + ")"
        else:
            print "(" + str(self.frm) + "," + str(self.to) + "::" + str(self.label) + "//" + str(self.weight) + ")"
            
    def graphviz(self):
        def graphvizstate(state):
            try:
                return '"' + str(state) + '"'
            except TypeError:
                strstate = map(str,state)
                return '"' + "".join(strstate) + '"'
        return '\n' + graphvizstate(self.frm) + " -> " + graphvizstate(self.to) + '[ label = "' + self.label + "//" + str(self.weight) +  '" ];'
            
    def reverse(self):
        self.frm, self.to = self.to, self.frm
        
    def replaceState(self,old,new):
        self.frm = new if self.frm == old else self.frm
        self.to = new if self.to == old else self.to
    
    def tuple(self):
        return FSAEdge(self.frm,(self.to,),self.label,self.weight)
        
    def __hash__(self):
        return hash((self.frm, self.to,self.label,str(self.weight)))

    def __eq__(self, other):
        return (self.frm, self.to,self.label,self.weight) == (other.frm, other.to,other.label,other.weight)
