from Weight import Weight

class FSAEdge:
    #weights are state the edge comes from, state it goes to, label, and weight
    def __init__(self,frm,to,label,weight=[]):
        self.frm = frm
        self.to = to
        self.label = label
        if isinstance(weight,list):
            self.weight = Weight(weight)
        else:
            self.weight = weight
        
    def prettyprint(self):
        if self.weight == Weight([]):
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
            
    def Reverse(self):
        self.frm, self.to = self.to, self.frm
        
    def replaceState(self,old,new):
        self.frm = new if self.frm == old else self.frm
        self.to = new if self.to == old else self.to
        
    def __hash__(self):
        return hash((self.frm, self.to,self.label,str(self.weight)))

    def __eq__(self, other):
        return (self.frm, self.to,self.label,self.weight) == (other.frm, other.to,other.label,other.weight)