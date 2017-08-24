from tkinter import *

class PhonotacticsFrame(Frame):
    def __init__(self,master):
        Frame.__init__(self,master)
        
        Label(self,text = "Phonotactics").grid(row=0, column=0)
        
        self.sideVar = StringVar()
        self.sideVar.set("None")
        self.sideVar.trace("w",self.showPrimary) 
        self.footVar = StringVar()
        self.footVar.set("0")
        self.footVar.trace("w",self.showSecondary)
        self.placementVar = StringVar()
        self.placementVar.set("1")
        self.deleteVar = BooleanVar()
        self.deleteVar.set(False)
        self.insertVar = BooleanVar()
        self.insertVar.set(False)
        
        self.alwaysFrame = Frame(self)
        self.primaryFrame = Frame(self)
        
        self.alwaysFrame.grid(row=1,column=0)
        
        Label(self.alwaysFrame,text = "Side:").pack()
        self.side = OptionMenu(self.alwaysFrame,self.sideVar,"None","Left","Right")
        self.side.pack()
        Label(self.alwaysFrame,text = "Default Syllable:").pack()
        self.unstressed = Entry(self.alwaysFrame)
        self.unstressed.pack()
        
        Label(self.primaryFrame,text = "Primary stress placement:").grid(row=0,column=0)
        self.placement = Spinbox(self.primaryFrame,from_=1,to=10, textvar = self.placementVar, width = 3)
        self.placement.grid(row=1,column=0)
        Label(self.primaryFrame,text = "Syllables between stresses").grid(row=0,column=1)
        Label(self.primaryFrame,text = "Primary Stressed syllable:").grid(row=2,column=0)
        self.primaryStress = Entry(self.primaryFrame)
        self.primaryStress.grid(row=3,column=0)
        Label(self.primaryFrame,text = "Bad Edge syllable:").grid(row=2,column=1)
        self.badEdge = Entry(self.primaryFrame)
        self.badEdge.grid(row=3,column=1)
        
        self.secondaryText = Label(self.primaryFrame,text = "Secondary Stressed syllable:")
        self.secondaryStress = Entry(self.primaryFrame)
        
        self.foot = Spinbox(self.primaryFrame,from_=0,to=10,textvariable=self.footVar,width = 3)
        self.foot.grid(row=1,column=1)
        
        Checkbutton(self.primaryFrame,text = "can insert",variable=self.insertVar).grid(row=0,column = 2)
        Checkbutton(self.primaryFrame,text = "can delete",variable=self.deleteVar).grid(row=1,column = 2)
        
    def showPrimary(self,*args):
        if self.sideVar.get() == "None":
            self.primaryFrame.grid_forget()
        else:
            self.primaryFrame.grid(row=1,column=1)
            
    def showSecondary(self,*args):
        if self.footVar.get() == "0":
            self.secondaryText.grid_forget()
            self.secondaryStress.grid_forget()
        else:
            self.secondaryText.grid(row=2,column=2)
            self.secondaryStress.grid(row=3,column=2)
        
    def get(self):
        return {
            "side": self.sideVar.get(),
            "foot": int(self.footVar.get()),
            "placement": int(self.placementVar.get()),
            "unstressed": self.unstressed.get(),
            "primary stress": self.primaryStress.get(),
            "secondary stress": self.secondaryStress.get(),
            "bad edge": self.badEdge.get(),
            "can insert": self.insertVar.get(),
            "can delete": self.deleteVar.get()
            }
        
    def insert(self,dictionary):
        self.sideVar.set(dictionary["side"])
        self.footVar.set(dictionary["foot"])
        self.placementVar.set(dictionary["placement"])
        insertToEntry(self.unstressed,dictionary["unstressed"])
        insertToEntry(self.primaryStress,dictionary["primary stress"])
        insertToEntry(self.badEdge,dictionary["bad edge"])
        insertToEntry(self.secondaryStress,dictionary["secondary stress"])
        self.deleteVar.set(dictionary["can delete"])
        self.insertVar.set(dictionary["can insert"])
        
def insertToEntry(entry,string):
    entry.delete(0,"end")
    entry.insert(0,string)