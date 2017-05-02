class FSM:
    #fields: starting state, ending states, list of all states, and list of edges 
    def __init__(self,start,ends,states,edges):                                   
        self.start = start                                                        
        self.ends = ends                                                          
        self.states = states                                                      
        self.edges = edges                          
        
    #This is a print function for a graph if you want to use graphviz to visualize it     
    def graphviz(self):                                                                   
        string = "digraph finite_state_machine {\nrankdir=LR;\n"                          
        string += "\nnode [shape = doublecircle];"                                        
        def graphvizstate(state):                                                         
            try:                                                                          
                return '"' + str(state) + '"'                                             
            except TypeError:                                                             
                strstate = map(str,state)                                                 
                return '"' + "".join(strstate) + '"'                                      
        for state in self.ends:                                                           
            string += " " + graphvizstate(state)                                          
        string += ";\nnode [shape = circle];"                                             
        for edge in self.edges:                                                           
            string += edge.graphviz()                                                     
        return string + '}'                                                               
                                                                                          
    def prettyprint(self):                                                                
        print "states: ", self.states                                                     
        print "start: ", self.start                                                       
        print "ends: ", self.ends                                                         
        print "edges: "                                                                   
        for edge in self.edges:                                                           
            edge.prettyprint()
            
    def replaceState(self,old,new):                                                           
        if self.start == old:                                                                 
            self.start = new                                                                  
        self.ends = [new if end == old else end for end in self.ends]                         
        self.states = [new if state == old else state for state in self.states]               
        for edge in self.edges:                                                               
            edge.replaceState(old,new)                                                        
                                                                                              
    def quotient(self,states):                                                                
        choice = states[0]                                                                    
        for state in states[1:]:                                                              
            self.replaceState(state,choice)                                                   
        self.ends = list(set(self.ends))                                                      
        self.states = list(set(self.states))                                                  
                                                                                              
    #This shouldn't really be useful unless you want to visualize everything better           
    def relabelStates(self):                                                                  
        newStates = enumerate(self.states)                                                    
        for (new,old) in newStates:                                                               
            self.replaceState(old,new)                                              
                                                                                              
    def reverse(self):                                                                        
        self.capEnd()                                                                         
        self.start, self.ends = self.ends[0], [self.start]                                    
        for edge in self.edges:                                                               
            edge.reverse()

    def stateFrom(self,tup=False):
        if tup:
            return {fromState : [e.tuple() for e in self.edges if e.frm == fromState] for fromState in self.states}
        return {fromState : [e for e in self.edges if e.frm == fromState] for fromState in self.states}
    
    def __hash__(self):                                                                                                                             
        return hash((self.start, set(self.ends),set(self.states),set(self.edges)))                                                                  
                                                                                                                                                    
    def __eq__(self, other):                                                                                                                        
        return (self.start, set(self.ends),set(self.states),set(self.edges)) == (other.start, set(other.ends),set(other.states),set(other.edges))   