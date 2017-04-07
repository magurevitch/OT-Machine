from Weight import Weight

class PQElement(object):
    __slots__ = ['label', 'weight', 'paths']

    def __init__(self,label,weight=Weight.infiniteWeight(),paths=[]):
        self.label = label
        self.weight = weight
        self.paths = paths