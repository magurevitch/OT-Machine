import copy

class Weight:
    
    #This is the default weight
    order = ["harm",'pen',"bs",'del','ins','chg']
    
    @classmethod
    def infiniteWeight(cls):
        returner = cls([])
        for item in cls.order:
            returner.bag[item] = float("inf")
        return returner
            
    def __init__(self,list):
        self.bag = {}
        for item in Weight.order:
            self.bag[item] = 0
        for item in list:
            if item in self.bag:
                self.bag[item] += 1
        
    def __cmp__(self,other):
        for weight in Weight.order:
            if self.bag[weight] != other.bag[weight]:
                return cmp(self.bag[weight], other.bag[weight])
        return 0
    
    def __add__(self,other):
        returner = copy.deepcopy(self)
        for weight in self.bag:
            returner.bag[weight] += other.bag[weight]
        return returner
        
    def __str__(self):
        list = []
        for weight in Weight.order:
            list += self.bag[weight] * [weight]
        return str(list)
    
    def __hash__(self):
        return hash(str(self))