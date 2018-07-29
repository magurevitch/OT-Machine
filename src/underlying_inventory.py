from .fst import FST
from .fsa import FSA

class UnderlyingInventory:
    def __init__(self,underlying,borrowings):
        self.underlying = underlying
        self.borrowings = borrowings
        
    def borrowingFST(self):
        fst = FST.selfLooping(self.underlying)
        for (foreign,options) in self.borrowings.items():
            for option in options:
                fst.addString(0,0,foreign,option)
        return fst
    
    def borrow(self,word):
        fsa = FSA.fromString(word)
        if not self.underlying:
            return fsa
        fst = self.borrowingFST()
        
        borrowingFSA = fst.product(fsa)
        
        if not(borrowingFSA.ends):
            return False
        return borrowingFSA
    
    def goodUnderlying(self,word):
        return all([x in self.underlying for x in word])