from collections import deque

#this isn't aho corasick anymore, since I set failure nodes to the root if there is a greedy match

class AhoCorasickNode:
    def __init__(self):
        self.output = False
        self.failureNode = False
        self.failureOutput = False
        self.children = {}
        
    def addChild(self,symbol):
        self.children[symbol] = AhoCorasickNode()
        
    def addSequence(self,word,output):
        currentNode = self
        for letter in word:
            if letter not in currentNode.children:
                currentNode.addChild(letter)
            currentNode = currentNode.children[letter]
        currentNode.output = output
            
    def setFailureNodes(self):
        queue = deque()
        
        self.failureNode = False;
        for (letter,child) in self.children.items():
            child.failureNode = self
            if not child.output:
                child.output = letter
            child.failureOutput = child.output
            queue.append(child)
        while queue:
            current = queue.pop()
            for (letter,child) in current.children.items():
                if not child.output and letter in current.failureNode.children:
                    child.output = current.output + letter
                    child.failureOutput = current.failureOutput
                    child.failureNode = current.failureNode.children[letter]    
                else:
                    if not child.output:
                        child.output = current.output + letter
                    child.failureOutput = child.output
                    child.failureNode = self
                queue.append(child)
        self.output = ""
        self.failureOutput = ""
                
    def graphviz(self):                                                                   
        string = "digraph finite_state_machine {\nrankdir=LR;\n"
        queue = deque([self])
        while queue:
            current = queue.pop()
            for (letter,child) in current.children.items():
                string += '"' + str(id(current)) + " " + current.output + " " + current.failureOutput + '" -> "' + str(id(child)) + " " + child.output + " " + child.failureOutput + '" [ label = ' + letter + " color=black ];\n"
                queue.append(child)
            if current.failureNode:
                string +=  '"' + str(id(current)) + " " + current.output + " " + current.failureOutput + '" -> "' + str(id(current.failureNode)) + " " + current.failureNode.output + " " + current.failureNode.failureOutput + '" [ color=red ];\n'
        
        return string + '}'
                
    def transform(self,text):
        transformed = ""
        
        current = self
        for letter in text:
            potential = ""
            output = current.output
            while letter not in current.children:
                if current.failureNode:
                    potential += current.failureOutput
                    current = current.failureNode
                else:
                    break
            transformed += potential if current.failureNode else output
            if letter in current.children:
                current = current.children[letter]
            else:
                transformed += letter
        if current.failureNode:
            transformed += current.output
        return transformed
            
    def __repr__(self):
        return "(output: " + self.output + ", children: " + str(self.children.keys()) + ")"
                    
        return transformed