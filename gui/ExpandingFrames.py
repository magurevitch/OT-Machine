from tkinter import *

class ExpandingListFrame(Frame):
    def __init__(self,master,name,columnNames, secondColumnWidth = 10,notList = False):
        Frame.__init__(self,master)
        
        Label(self,text=name).grid(row=0,columnspan =2)
        
        self.expand = ExpansionFrame(self,addFunction = self.addDefault,deleteFunction = self.deleteDefault)
        self.expand.grid(row=2,column=0)
        
        self.firstColumn = []
        self.secondColumn = []
        self.thirdColumn = []
        
        self.columns = columnNames
        self.buttons = []
        
        for i in range(len(self.columns)):
            Label(self,text=self.columns[i]).grid(row=1,column = i)
            
        self.secondColumnWidth = secondColumnWidth
        self.notList = notList
        
    def addDefault(self,event = None):
        self.expand.grid_forget()
        self.firstColumn += [Entry(self, width = 7)]
        if len(self.columns) > 1:
            self.secondColumn += [Entry(self, width = self.secondColumnWidth)]
        if len(self.columns) > 2:
            self.thirdColumn += [StringVar()]
            self.thirdColumn[-1].set("b")
            self.buttons += [Radiobutton(self,text = "before",variable=self.thirdColumn[-1],value="b")]
            self.buttons += [Radiobutton(self,text = "after",variable=self.thirdColumn[-1],value="a")]
        for number in range(len(self.firstColumn)):
            self.firstColumn[number].grid(row=number+2,column=0)
            if len(self.columns) > 1:
                self.secondColumn[number].grid(row=number+2,column=1)
            if len(self.columns) > 2:
                self.buttons[2*number].grid(row=number+2,column=2)
                self.buttons[2*number+1].grid(row=number+2,column=3)
        self.expand.grid(row=len(self.firstColumn)+2)
    
    def deleteDefault(self,event = None):
        self.expand.grid_forget()
        self.firstColumn.pop().grid_forget()
        
        if len(self.columns) > 1:
            self.secondColumn.pop().grid_forget()
        if len(self.columns) > 2:
            self.thirdColumn.pop()
            self.buttons.pop().grid_forget()
            self.buttons.pop().grid_forget()
        self.expand.grid(row=len(self.firstColumn)+2)
            
    def get(self):
        if len(self.columns) == 1:
            return [entry.get() for entry in self.firstColumn]
        if len(self.columns) == 2:
            return {self.firstColumn[i].get():self.getSecondColumn(i)
                    for i in range(len(self.firstColumn))}
        if len(self.columns) > 2:
            return {self.firstColumn[i].get():
                    (self.getSecondColumn(i),self.thirdColumn[i].get())
                    for i in range(len(self.firstColumn))}
            
    def getSecondColumn(self,i):
        if self.notList:
            return self.secondColumn[i].get()
        else:
            return self.secondColumn[i].get().replace(' ', ',').split(',')
            
    def clear(self):
        while self.firstColumn:
            self.expand.deleteEntry()
        
    def insert(self, dictionary):
        self.clear()
        
        for (name,entries) in dictionary.items():
            self.expand.addEntry()
            insertToEntry(self.firstColumn[-1],name)
            if len(self.columns) == 2:
                insertToEntry(self.secondColumn[-1], " ".join(entries))
            if len(self.columns) == 3:
                insertToEntry(self.secondColumn[-1], entries[0])
                self.thirdColumn[-1].set(entries[1])
            
class ListFrame(Frame):
    def __init__(self,master,name,cls):
        Frame.__init__(self,master)
        
        self.name = name
        
        self.expand = ExpansionFrame(self,cls = cls)
        
        self.column = []
        
        Label(self,text=name).pack()
        
        self.expand.pack()
            
    def get(self):
        try:
            return {entry.name.get():entry.get() for entry in self.column}
        except:
            return [entry.get() for entry in self.column]
        
    def clear(self):
        while self.column:
            self.expand.deleteEntry()
        
    def insert(self,dictionary):
        self.clear()
        
        try:
            for (name,entry) in dictionary.items():
                self.expand.addEntry()
                insertToEntry(self.column[-1].name, name)
                self.column[-1].insert(entry)
        except:
            for assimilation in dictionary:
                self.expand.addEntry()
                self.column[-1].insert(assimilation)
    
class AssimilationFrame(Frame):
    def __init__(self,master):
        Frame.__init__(self,master)
        
        self.expand = ExpansionFrame(self)
        
        self.column = []
        
        self.tierFrame = Frame(self)
        self.tierFrame.pack()
        
        self.listLabel = Label(self.tierFrame, text="Opaque phonemes: ")
        self.list = Entry(self.tierFrame)
        
        self.hasList = IntVar()
        self.hasList.set(0)
        Checkbutton(self.tierFrame,text = "is it long distance?", variable = self.hasList).grid(row=0,columnspan=2)
        self.hasList.trace("w",self.turnOnList)
        
        self.dissimilation = BooleanVar()
        self.dissimilation.set(False)
        Radiobutton(self,text = "Assimilation",variable = self.dissimilation, value = False).pack()
        Radiobutton(self,text = "Dissimilation",variable = self.dissimilation, value = True).pack()
        
        self.expand.pack()
            
    def get(self):
        return {
            "tier": self.list.get().replace(' ', ',').split() if self.hasList.get() else False,
            "lists": [entry.get() for entry in self.column],
            "dissimilation": self.dissimilation.get()
            }
        
    def turnOnList(self, *args):
        if self.hasList.get():
            self.listLabel.grid(row=1,column=0)
            self.list.grid(row=1,column=1)
        else:
            self.listLabel.grid_forget()
            self.list.grid_forget()
            
    def insert(self,dictionary):
        if dictionary["tier"] == False:
            self.hasList.set(0)
        else:
            self.hasList.set(1)
            insertToEntry(self.list," ".join(dictionary["tier"]))
            
        for group in dictionary["lists"]:
            self.expand.addEntry()
            insertToEntry(self.column[-1]," ".join(group))
                    
class ConjugationFrame(ExpandingListFrame):
    def __init__(self,master):
        ExpandingListFrame.__init__(self,master,"Conjugation name:",["Form name","form"])
        
        self.name = Entry(self)
        self.name.grid(row=0,column=1)
        
    def get(self):
        return [(self.firstColumn[i].get(),self.secondColumn[i].get())
                    for i in range(len(self.firstColumn))]
        
    def insert(self, dictionary):
        self.clear()
        
        for (name,form) in dictionary:
            self.expand.addEntry()
            
            insertToEntry(self.firstColumn[-1],name)
            insertToEntry(self.secondColumn[-1],form)
        
class ExpansionFrame(Frame):
    def __init__(self,master,cls = Entry, addFunction = False, deleteFunction = False):
        Frame.__init__(self,master)
        
        self.cls = cls
        self.addEntry = addFunction if addFunction else self.addDefault
        self.deleteEntry = deleteFunction if deleteFunction else self.deleteDefault
        
        self.expand = Button(self,text = "+")
        self.expand.bind("<Button-1>", self.addEntry)
        self.expand.grid(row=0,column=0)
        
        self.collapse = Button(self,text = "-")
        self.collapse.bind("<Button-1>", self.deleteEntry)
        self.collapse.grid(row=0,column=1)
        
    def addDefault(self,event = None):
        self.pack_forget()
        self.master.column += [self.cls(self.master)]
        self.master.column[-1].pack()
        self.pack()
        
    def deleteDefault(self,event = None):
        if self.master.column:
            self.pack_forget()
            self.master.column.pop().pack_forget()
            self.pack()

def insertToEntry(entry,string):
    entry.delete(0,"end")
    entry.insert(0,string)