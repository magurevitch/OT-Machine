from Weight import Weight

class FSTEdge:
    def __init__(self,frm,to,original,changed,weight=[]):
        self.frm = frm
        self.to = to
        self.original = original
        self.changed = changed
        if isinstance(weight,list):
            self.weight = Weight(weight)
        else:
            self.weight = weight
        
    def prettyprint(self):
        if self.weight == Weight([]):
            print "(" + str(self.frm) + "," + str(self.to) + "::" + str(self.original) + " > " + str(self.changed) + ")"
        else:
            print "(" + str(self.frm) + "," + str(self.to) + "::" + str(self.original) + " > " + str(self.changed) + "//" + str(self.weight) + ")"
            
    def graphviz(self):
        def graphvizstate(state):
            try:
                return '"' + str(state) + '"'
            except TypeError:
                strstate = map(str,state)
                return '"' + "".join(strstate) + '"'
        return '\n' + graphvizstate(self.frm) + " -> " + graphvizstate(self.to) + '[ label = "' + str(self.original) + " > " + str(self.changed) + "//" + str(self.weight) +  '" ];'
            
    def Reverse(self):
        self.frm, self.to = self.to, self.frm
        
    def replaceState(self,old,new):
        self.frm = new if self.frm == old else self.frm
        self.to = new if self.to == old else self.to
        
    def __hash__(self):
        return hash((self.frm, self.to,self.original,self.changed,str(self.weight)))

    def __eq__(self, other):
        return (self.frm, self.to,self.original,self.changed,self.weight) == (other.frm, other.to,other.original,other.changed,other.weight)