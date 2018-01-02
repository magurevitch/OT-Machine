from src.aho_corasick_node import AhoCorasickNode

class Orthography:
    def __init__(self,map):
        self.map = map
        self.decodeRoot = AhoCorasickNode()
        self.encodeRoot = AhoCorasickNode()
        for (input,output) in map.items():
            self.decodeRoot.addSequence(input,output)
            self.encodeRoot.addSequence(output,input)
        self.decodeRoot.setFailureNodes()
        self.encodeRoot.setFailureNodes()
            
    def decode(self,text):
        return self.decodeRoot.transform(text)
    
    def encode(self,text):
        return self.encodeRoot.transform(text)