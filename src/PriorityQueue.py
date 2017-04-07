import Weight
from PQElement import PQElement

class PriorityQueue:
    def __init__(self,list):
        self.list = [False] + [PQElement(item) for item in list]
        for i in range(len(list) - 1, 0, -1):
            self.percolateDown(i)
            
    def parent(self,index):
        index = index/2
        if index < 1:
            return False
        return index
        
    def leftChild(self,index):
        index *=2
        if index >= len(self.list):
            return False
        return index
        
    def rightChild(self,index):
        index = (2*index) + 1
        if index >= len(self.list):
            return False
        return index
        
    def percolateUp(self,i):
        p = self.parent(i)
        if p:
            if self.list[i].weight < self.list[p].weight:
                self.list[i], self.list[p] = self.list[p], self.list[i]
                self.percolateUp(p)
                    
    def percolateDown(self,i):
        l = self.leftChild(i)
        r = self.rightChild(i)
        if l and r:
            w = r if self.list[r].weight < self.list[l].weight else l
            if self.list[i].weight > self.list[w].weight:
                self.list[i], self.list[w] = self.list[w], self.list[i]
                self.percolateDown(w)
        elif l:
            if self.list[i].weight > self.list[l].weight:
                self.list[i], self.list[l] = self.list[l], self.list[i]
                self.percolateDown(l)
                
    def pop(self):
        returner = self.list[1]
        self.list = [False] + [self.list[-1]] + self.list[2:-1]
        self.percolateDown(1)
        return returner
        
    def update(self,label,weight,paths):
        element = [element for element in self.list[1:] if element.label == label][0]
        element.weight = weight
        element.paths = paths
        i = self.list.index(element)
        if self.parent(i):
            self.percolateUp(i)
        if self.leftChild(i):
            self.percolateDown(i)
            
    def getWeight(self,label):
        potentials = [item.weight for item in self.list[1:] if item.label == label]
        if len(potentials) < 1:
            return False
        return potentials[0]
        
    def getPaths(self,label):
        potentials = [item.paths for item in self.list[1:] if item.label == label]
        if len(potentials) < 1:
            return False
        return potentials[0]
            
    def prettyprint(self):
        print [(item.label,item.weight,item.paths) for item in self.list[1:]]
