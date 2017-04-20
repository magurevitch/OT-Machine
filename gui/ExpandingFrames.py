from Tkinter import *
from encodings.punycode import insertion_sort

class ExpandingListFrame(Frame):
    def __init__(self,master,name,columnNames):
        Frame.__init__(self,master)
        
        Label(self,text=name).grid(row=0)
        
        self.expand = Button(self,text = "+")
        self.expand.bind("<Button-1>", self.addEntry)
        self.expand.grid(row=2,column=0)
        
        self.firstColumn = []
        self.secondColumn = []
        self.thirdColumn = []
        
        self.columns = columnNames
        self.buttons = []
        
        for i in range(len(self.columns)):
            Label(self,text=self.columns[i]).grid(row=1,column = i)
        
    def addEntry(self,event):
        self.expand.grid_forget()
        self.firstColumn += [Entry(self)]
        if len(self.columns) > 1:
            self.secondColumn += [Entry(self)]
        if len(self.columns) > 2:
            self.thirdColumn += [StringVar()]
            self.thirdColumn[-1].set("b")
        for number in range(len(self.firstColumn)):
            self.firstColumn[number].grid(row=number+2,column=0)
            if len(self.columns) > 1:
                self.secondColumn[number].grid(row=number+2,column=1)
            if len(self.columns) > 2:
                self.buttons += [Radiobutton(self,text = "before",variable=self.thirdColumn[number],value="b")]
                self.buttons[-1].grid(row=number+2,column=2)
                self.buttons += [Radiobutton(self,text = "after",variable=self.thirdColumn[number],value="a")]
                self.buttons[-1].grid(row=number+2,column=3)
        self.expand.grid(row=len(self.firstColumn)+2)
            
    def get(self):
        if len(self.columns) == 1:
            return [entry.get() for entry in self.firstColumn]
        if len(self.columns) == 2:
            return {self.firstColumn[i].get():self.secondColumn[i].get().replace(' ', ',').split(',')
                    for i in range(len(self.firstColumn))}
        if len(self.columns) > 2:
            return {self.firstColumn[i].get():
                    (self.secondColumn[i].get(),self.thirdColumn[i].get())
                    for i in range(len(self.firstColumn))}
            
    def clear(self):
        for i in range(len(self.firstColumn)):
            self.firstColumn[i].destroy()
            if len(self.columns) > 1:
                self.secondColumn[i].destroy()
        for button in self.buttons:
            button.destroy()
        self.firstColumn = []
        self.secondColumn = []
        self.thirdColumn = []
        self.buttons = []
        
    def insert(self, dictionary):
        self.clear()
        
        for (name,entries) in dictionary.items():
            self.addEntry(None)
            insertToEntry(self.firstColumn[-1],name)
            if len(self.columns) == 2:
                insertToEntry(self.secondColumn[-1], " ".join(entries))
            if len(self.columns) == 3:
                insertToEntry(self.secondColumn[-1], entries[0])
                self.thirdColumn[-1].set(entries[1])
            
class ListFrame(Frame):
    def __init__(self,master,name,cls):
        Frame.__init__(self,master)
        
        self.cls = cls
        self.name = name
        
        self.expand = Button(self,text = "add another " + self.name[:-1])
        self.expand.bind("<Button-1>", self.addEntry)
        
        self.column = []
        
        Label(self,text=name).pack()
        
        self.expand.pack()
        
    def addEntry(self,event):
        self.expand.pack_forget()
        self.column += [self.cls(self)]
        self.column[-1].pack()
        self.expand.pack()
            
    def get(self):
        try:
            return {entry.name.get():entry.get() for entry in self.column}
        except:
            return [entry.get() for entry in self.column]
        
    def clear(self):
        for entry in self.column:
            entry.pack_forget()
        self.column = []
        
    def insert(self,dictionary):
        self.clear()
        
        try:
            for (name,entry) in dictionary.items():
                self.addEntry(None)
                insertToEntry(self.column[-1].name, name)
                self.column[-1].insert(entry)
        except:
            for assimilation in dictionary:
                self.addEntry(None)
                self.column[-1].insert(assimilation)
    
class AssimilationFrame(Frame):
    def __init__(self,master):
        Frame.__init__(self,master)
        
        self.expand = Button(self,text = "+")
        self.expand.bind("<Button-1>", self.addEntry)
        
        self.column = []
        
        self.tierFrame = Frame(self)
        self.tierFrame.pack()
        
        self.listLabel = Label(self.tierFrame, text="Entries in the tier: ")
        self.list = Entry(self.tierFrame)
        
        self.hasList = IntVar()
        self.hasList.set(0)
        Checkbutton(self.tierFrame,text = "is it in a tier?", variable = self.hasList).grid(row=0,columnspan=2)
        self.hasList.trace("w",self.turnOnList)
        
        self.dissimilation = BooleanVar()
        self.dissimilation.set(False)
        Radiobutton(self,text = "Assimilation",variable = self.dissimilation, value = False).pack()
        Radiobutton(self,text = "Dissimilation",variable = self.dissimilation, value = True).pack()
        
        self.expand.pack()
        
    def addEntry(self,event):
        self.expand.pack_forget()
        self.column += [Entry(self)]
        self.column[-1].pack()
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
            insertToEntry(self.list,dictionary["tier"])
            
        for group in dictionary["lists"]:
            self.addEntry(None)
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
            self.addEntry(None)
            
            insertToEntry(self.firstColumn[-1],name)
            insertToEntry(self.secondColumn[-1],form)
        
        
        
def insertToEntry(entry,string):
    entry.delete(0,"end")
    entry.insert(0,string)