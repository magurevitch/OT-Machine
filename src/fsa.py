from .weight import Weight, zeroWeight, infiniteWeight
from .priority_queue import PriorityQueue
from .fsm import FSM
from collections import deque
import functools

class FSA(FSM):    
    def addEdge(self,frm,to,label,weight=zeroWeight):
        self.edges += [FSAEdge(frm,to,label,weight)]
        return self
    
    def addEdges(self,edges):
        for edge in edges:
            self.addEdge(*edge)
        
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
                          if selfEdge.label or zeroWeight in [selfEdge.weight,fsaEdge.weight]
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
    
    def addBefore(self,symb):
        return FSA("new",self.ends,self.states+["new"],self.edges+[FSAEdge("new",self.start,symb)])
    
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
        
    def capEnd(self):        
        if len(self.ends) > 1:
            self.states += ["END"]
            for end in self.ends:
                self.edges += [FSAEdge(end,"END","")]
            self.ends = ["END"]
        
    def crunchEdges(self):
        scoreBoard = {}
        for edge in self.edges:
            key = (edge.frm,edge.to,edge.label)
            if key not in scoreBoard or edge.weight < scoreBoard[key]:
                scoreBoard[key] = edge.weight
        self.edges = [FSAEdge(frm,to,label,val) for ((frm,to,label),val) in scoreBoard.items()]
        return self
            
    def dijkstra(self):
        if len(self.ends) == 0:
            return (False,False)
        
        queue = PriorityQueue(self.states)
        queue.update(self.start,zeroWeight,[""])

        stateFrom = self.stateFrom()
        
        winning_weight = False
        winning_paths = []

        while queue.list:
            current = queue.pop()
            if current.weight == infiniteWeight:
                break
            if current.label in self.ends:
                if not(winning_weight) or current.weight == winning_weight:
                    winning_weight = current.weight
                    winning_paths += current.paths
            for edge in stateFrom[current.label]:
                if edge.to in queue:
                    newWeight = current.weight + edge.weight
                    queueWeight = queue.getWeight(edge.to)
                    if not(winning_weight) or newWeight < winning_weight:
                        if newWeight < queueWeight:
                            paths = [path + edge.label for path in current.paths]
                            queue.update(edge.to,newWeight,paths)
                        elif newWeight == queueWeight:
                            paths = [path + edge.label for path in current.paths]
                            queue.addToPaths(edge.to,paths)
                    if winning_weight and newWeight <= winning_weight and edge.to in self.ends:
                        paths = [path + edge.label for path in current.paths]
                        winning_paths += paths
        return (winning_weight, winning_paths)
    
    def determinize(self):
        state_transitions = {}
        epsilon_closures = {}
        
        for edge in self.edges:
            label = (edge.label,edge.weight)
            if label == ("",zeroWeight):
                epsilon_closures[edge.frm] = epsilon_closures.get(edge.frm,[]) + [edge.to]
            else:
                if edge.frm not in state_transitions:
                    state_transitions[edge.frm] = {}
                state_transitions[edge.frm][label] = state_transitions[edge.frm].get(label,[]) + [edge.to]

        start = tuple(set([self.start] + epsilon_closures.get(self.start,[])))
        fsa = FSA(start,[],[],[])
        stack = deque([start])
        while stack:
            current = stack.pop()
            if current not in fsa.states + [()]:
                toStates = {}
                for state in current:
                    if state in state_transitions:
                        for label in state_transitions[state]:
                            toStates[label] = toStates.get(label,[]) + state_transitions[state][label]
                fsa.states += [current]
                for label in toStates:
                    newState = toStates[label]
                    for state in newState:
                        if state in epsilon_closures:
                            newState += [s for s in epsilon_closures[state] if s not in newState]
                    newState = tuple(set(sorted(newState,key=str)))
                    if newState not in fsa.states:
                        stack.append(newState)
                    fsa.addEdge(current, newState, label[0], label[1])
                    if newState not in fsa.ends:
                        if [0 for state in newState if state in self.ends]:
                            fsa.ends += [newState]
        return fsa
    
    def traverse(self):
        stack = deque([self.start])
        statesFrom = self.stateFrom()
        scoreboard = {state:set() for state in self.states}
        scoreboard[self.start] = set([""])
        antiloop = {state:set() for state in self.states}
        
        while stack:
            current = stack.pop()
            for edge in statesFrom[current]:
                if(edge.to not in antiloop[edge.frm]):
                    scoreboard[edge.to].update([string + edge.label for string in scoreboard[edge.frm]])
                    antiloop[edge.to].add(edge.frm)
                    antiloop[edge.to].update(antiloop[edge.frm])
                    stack.append(edge.to)
            
        
        return [string for end in self.ends for string in scoreboard[end]]
    
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
        return sorted([bijection[end] for end in fsa.ends],key = str) == sorted(fsb.ends,key = str)
    
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
        edges = [FSAEdge(i,i+1,string[i]) for i in range(len(string))]
        edges += [FSAEdge(i,i,"") for i in states]
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
            if len(string) < 1:
                fsa.quotient([end,start])
            elif len(string) == 1:
                fsa.addEdge(start,end,string)
            else:
                queue = deque()
                currentChunk = ""
                open = start
                penalty = False
                for letter in string:
                    parenthasis = queue.pop() if letter in "]})" else False
                    if not queue:
                        if letter in "\|/":
                            fsa.quotient([end,open])
                            open = start
                        elif letter == '*':
                            fsa.addEdge(open, max(fsa.states) + 1, "")
                            penalty = True
                        elif letter == '#':
                            penalty = True
                        elif letter in "[{(":
                            queue.append(letter)
                        elif letter in "]})":
                            newOpen = max(fsa.states) + 1
                            fsa.states += [newOpen]
                            if penalty:
                                fsa.addEdge(open,newOpen,"",['pen'])
                                open = newOpen
                                newOpen += 1
                                fsa.states += [newOpen]
                            if parenthasis == '(':
                                fsa.addEdge(open,newOpen,"")
                            elif parenthasis == '{':
                                fsa.addEdge(open,newOpen,"",['pen'])
                            ThompsonRecurse(open, newOpen, currentChunk)
                            open = newOpen
                            penalty = False
                            currentChunk = ""
                        else:
                            newOpen = max(fsa.states) + 1
                            fsa.states += [newOpen]
                            fsa.addEdge(open, newOpen, letter, ['pen'] if penalty else [])
                            open = newOpen
                            penalty = False
                    else:
                        currentChunk += letter
                        if letter in "[{(":
                            queue.append(letter)
                fsa.quotient([end,open])

        ThompsonRecurse(0,'f',regex)
        fsa.states += ['f']
        
        fsa = fsa.minimize()
        
        fsa.relabelStates()
        
        return fsa
    
    def multiproduct(self,fsas):
        fsas = list(fsas)
        start = (self.start,) + tuple(fsa.start for fsa in fsas)
        fsa_ = FSA(start,[],[],[])
        stack = deque([start])
    
        statesFrom = (self.stateFrom(True),) + tuple(fsa.stateFrom() for fsa in fsas)
        while stack:
            current = stack.pop()
            if current not in fsa_.states:
                fsa_.states += [current]
                fsas = list(fsas)
                if all([x in fsa.ends for (x, fsa) in zip(current,[self] + fsas)]):
                    fsa_.ends += [current]
                currentEdges = [sf[x] for (x, sf) in zip(current,statesFrom)]
                partial = functools.reduce(lambda xs,ys:
                                 [FSAEdge(current,x.to +(y.to,),x.label,x.weight+y.weight)
                                  for x in xs
                                  for y in [edge for edge in ys if x.label == edge.label]
                                  if x.label or zeroWeight in [x.weight,y.weight]
                                  ], 
                                 currentEdges)
            
                stack.extend([edge.to for edge in partial if edge.to != current])
                fsa_.edges += partial
        return fsa_.trim()
    
    def toRegex(self):
        copy = FSA(self.start,self.ends,self.states,self.edges)
        copy.capEnd()
        #note: check to see why I need to relabel states
        copy.relabelStates()
        for state in [state for state in copy.states if state not in [copy.start] + copy.ends]:
            copy.removeState(state)
        return "[" + "|".join(edge.label for edge in copy.edges) + "]"
    
    #This function ignores self-loops
    def removeState(self,state):
        self.states.remove(state)
        edgesIn = [edge for edge in self.edges if edge.to == state]
        edgesOut = [edge for edge in self.edges if edge.frm == state]
        otherEdges = [edge for edge in self.edges if edge not in edgesIn + edgesOut]
        
        def createLabel(list):
            newList = []
            option = 0
            
            for item in list:
                if item[0] in " ,'":
                    if item[1] > zeroWeight and option < 2:
                        option = 1
                    else:
                        option = 2                    
                elif item[1] > zeroWeight:
                    newList += ["#" + item[0]]
                else:
                    newList += [item[0]]
                    
            if len(newList) == 0:
                return ""
            if option == 1:
                return "{" + "|".join(newList) + "}"
            if option == 2:
                if [True for item in newList if item[0] == '#']:
                    newList = [item[1:] for item in newList]
                    return ("*" + newList[0]) if len(newList) == 1 else ("[#" + "|#".join(newList) + "]")
                else:
                    return "(" + "|".join(newList) + ")"
            if len(newList) == 1:
                return newList[0]
            return "[" + "|".join(newList) + "]"
                    
        temp = {}
        for edge in edgesIn:
            if edge.frm not in temp:
                temp[edge.frm] = []
            temp[edge.frm] += [(edge.label,edge.weight)]
        edgesIn = [FSAEdge(frm,state,createLabel(list)) for (frm,list) in temp.items()]
        temp = {}
        for edge in edgesOut:
            if edge.to not in temp:
                temp[edge.to] = []
            temp[edge.to] += [(edge.label,edge.weight)]
        edgesOut = [FSAEdge(state,to,createLabel(list)) for (to,list) in temp.items()]
        newEdges = [FSAEdge(a.frm,b.to,a.label+b.label,a.weight+b.weight) for a in edgesIn for b in edgesOut]
        self.edges = otherEdges + newEdges
    
class FSAEdge:
    def __init__(self,frm,to,label,weight=zeroWeight):
        self.frm = frm
        self.to = to
        self.label = label
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
        return '\n' + graphvizstate(self.frm) + " -> " + graphvizstate(self.to) + '[ label = "' + self.label + "//" + str(self.weight) +  '" ];'
            
    def reverse(self):
        self.frm, self.to = self.to, self.frm
        
    def replaceState(self,old,new):
        self.frm = new if self.frm == old else self.frm
        self.to = new if self.to == old else self.to
    
    def tuple(self):
        return FSAEdge(self.frm,(self.to,),self.label,self.weight)
    
    def __repr__(self):
        return "(" + str(self.frm) + "->" + str(self.to) + "//" + str(self.label) + "," + str(self.weight) + ")"
        
    def __hash__(self):
        return hash((self.frm, self.to,self.label,str(self.weight)))

    def __eq__(self, other):
        return (self.frm, self.to,self.label,self.weight) == (other.frm, other.to,other.label,other.weight)
