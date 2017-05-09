from collections import Counter

class Weight(tuple):
    #This is the default weight
    order = ["harm",'pen',"bs",'del','ins','chg']
    
    def __new__ (cls, arg, already = False):
        if already:
            return super(Weight, cls).__new__(cls,arg)
        counter = Counter(arg)
        return super(Weight, cls).__new__(cls,tuple(counter[item] for item in cls.order))
        
    def __add__(self,other):
        return Weight(tuple(s+o for (s,o) in zip(self,other)),True)
        
    def __repr__(self):
        return str({weight:value for (weight,value) in zip(self.order,self) if value != 0})
    
infiniteWeight = Weight(tuple(float("inf") for item in Weight.order),True)
zeroWeight = Weight([])