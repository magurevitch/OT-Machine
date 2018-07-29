from .weight import zeroWeight, infiniteWeight

class PriorityQueue:
    def __init__(self,list):
        self.list = [False] + [PQElement(item) for item in list]
        for i in range(len(list) - 1, 0, -1):
            self.percolateDown(i)
        
    def percolateUp(self,i):
        p = parent(i)
        if p > 0 and self.list[i].weight < self.list[p].weight:
            self.list[i], self.list[p] = self.list[p], self.list[i]
            self.percolateUp(p)
                    
    def percolateDown(self,i):
        l = leftChild(i)
        r = rightChild(i)
        if r < len(self.list):
            w = r if self.list[r].weight < self.list[l].weight else l
            if self.list[i].weight > self.list[w].weight:
                self.list[i], self.list[w] = self.list[w], self.list[i]
                self.percolateDown(w)
        elif r == len(self.list):
            if self.list[i].weight > self.list[l].weight:
                self.list[i], self.list[l] = self.list[l], self.list[i]
                self.percolateDown(l)
                
    def pop(self):
        returner = self.list[1]
        if len(self.list) > 2:
            self.list[1] = self.list.pop()
            self.percolateDown(1)
        else:
            self.list = []
        return returner
        
    def update(self,label,weight,paths):
        (i, element) = next(((i+1,item) for (i,item) in enumerate(self.list[1:]) if item.label == label))
        element.weight = weight
        element.paths = paths
        if parent(i):
            self.percolateUp(i)
        if leftChild(i) < len(self.list):
            self.percolateDown(i)
            
    def addToPaths(self,label,paths):
        element = next((item for item in self.list[1:] if item.label == label))
        element.paths += paths
            
    def getWeight(self,label):
        return next((item.weight for item in self.list[1:] if item.label == label),False)
        
    def getPaths(self,label):
        return next((item.paths for item in self.list[1:] if item.label == label),False)
    
    def __contains__(self,key):
        return key in [item.label for item in self.list[1:]]

class PQElement(object):
    __slots__ = ['label', 'weight', 'paths']

    def __init__(self,label,weight=infiniteWeight,paths=[]):
        self.label = label
        self.weight = weight
        self.paths = paths
        
def parent(index):
    index //= 2
    return index if index > 0 else False
        
def leftChild(index):
    return index * 2     

def rightChild(index):
    return index*2 + 1
