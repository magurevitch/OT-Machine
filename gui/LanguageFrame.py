from Tkinter import *
import sys
sys.path.append('../')
import ast
import src.controller as controller
from PhonotacticsFrame import PhonotacticsFrame
from ExpandingFrames import ExpandingListFrame, ListFrame, ConjugationFrame, AssimilationFrame

class LanguageFrame(Frame):
    def __init__(self,master):
        Frame.__init__(self,master)
        self.buttonFrame = Frame(self)
        self.buttonFrame.grid(row=0,columnspan = 4)
        
        self.tambajna = Button(self.buttonFrame,text = "insert Tambajna")
        self.tambajna.bind("<Button-1>",self.insertTambajna)
        self.tambajna.grid(row = 0,column=0)
        
        self.getLanguage = Button(self.buttonFrame,text = "Get the language from the entries")
        self.getLanguage.bind("<Button-1>",self.getLangauge)
        self.getLanguage.grid(row = 0, column = 1)
        
        self.setLanguage = Button(self.buttonFrame,text = "Set the language from the text box")
        self.setLanguage.bind("<Button-1>",lambda event: self.insertLanguage(ast.literal_eval(self.languageText.get("1.0",END))))
        self.setLanguage.grid(row = 0, column = 2)
        
        self.clearButton = Button(self.buttonFrame,text = "Clear")
        self.clearButton.bind("<Button-1>",self.clear)
        self.clearButton.grid(row = 0, column = 3)
        
        self.helpButton = Button(self.buttonFrame,text = "Help")
        self.helpButton.bind("<Button-1>",self.help)
        self.helpButton.grid(row = 0, column = 4)
        
        self.orderFrame = OrderFrame(self)
        self.orderFrame.grid(row = 1, column = 2, rowspan = 4)
        
        self.phonotacticsFrame = PhonotacticsFrame(self)
        self.phonotacticsFrame.grid(row = 1, column = 3, rowspan = 4)
        
        self.categories = ExpandingListFrame(self,"Categories",["Label","types"])
        self.categories.grid(row = 6, column = 0, columnspan = 2)
        self.insertions = ExpandingListFrame(self,"Insertions",["Near:","Insert a:","Where:"])
        self.insertions.grid(row = 5, column = 0, columnspan = 2)
        self.changes = ExpandingListFrame(self,"Changes",["Original","Changed"])
        self.changes.grid(row = 5, column = 2)
        self.codas = ExpandingListFrame(self,"Changes in Codas",["Original","Changed"])
        self.codas.grid(row = 5, column = 3)
        self.conjugations = ListFrame(self,"conjugations",ConjugationFrame)
        self.conjugations.grid(row = 6, column = 3)
        self.assimilations = ListFrame(self,"assimilations",AssimilationFrame)
        self.assimilations.grid(row = 6, column = 2)
        
        Label(self,text = "Undeletables:").grid(row = 1, column = 0)
        self.undeletables = Entry(self)
        self.undeletables.grid(row = 1, column = 1)
        
        Label(self,text = "Geminates:").grid(row = 2, column = 0)
        self.geminates = Entry(self)
        self.geminates.grid(row = 2, column = 1)
        
        Label(self,text = "Vowels:").grid(row = 3, column = 0)
        self.vowels = Entry(self)
        self.vowels.grid(row = 3, column = 1)
        
        Label(self,text = "Bad strings:").grid(row = 4, column = 0)
        self.badstrings = Entry(self)
        self.badstrings.grid(row = 4, column = 1)
        
        self.languageText = Text(self)
        self.languageText.grid(row = 1, column = 4, rowspan = 6)
    
    def makeLanguage(self):
        dictionary = self.get()
        return controller.makeLanguage(dictionary)
    
    
    def get(self):
        return {
            "categories": self.categories.get(),
            "insertions": self.insertions.get(),
            "changes": self.changes.get(),
            "phonotactics": self.phonotacticsFrame.get(),
            "codas": self.codas.get(),
            "harmonies": self.assimilations.get(),
            "conjugations": self.conjugations.get(),
            "undeletables": self.undeletables.get().replace(' ', ',').split(','),
            "geminates": self.geminates.get().replace(' ', ',').split(','),
            "vowels": self.vowels.get().replace(' ', ',').split(','),
            "bad strings": self.badstrings.get().replace(' ', ',').split(','),
            "order": self.orderFrame.get()
            }
        
    def getLangauge(self,event):
        self.languageText.delete('1.0', END)
        self.languageText.insert('1.0', self.get())
        
        

    def insertLanguage(self, dictionary):
        insertToEntry(self.vowels, " ".join(dictionary["vowels"]))
        insertToEntry(self.geminates, " ".join(dictionary["geminates"]))
        insertToEntry(self.undeletables, " ".join(dictionary["undeletables"]))
        insertToEntry(self.badstrings, " ".join(dictionary["bad strings"]))
        self.orderFrame.order.delete(0, 6)
        for num, item in enumerate(dictionary["order"]):
            self.orderFrame.order.insert(num, item)
        
        self.phonotacticsFrame.insert(dictionary["phonotactics"])
        self.categories.insert(dictionary["categories"])
        self.insertions.insert(dictionary["insertions"])
        self.changes.insert(dictionary["changes"])
        self.codas.insert(dictionary["codas"])
        self.assimilations.insert(dictionary["harmonies"])
        self.conjugations.insert(dictionary["conjugations"])

    def insertTambajna(self,event):
        file = open("./src/tambajna_phonology.txt","r")
        dictionary = ast.literal_eval(file.read())
        file.close()
        
        self.insertLanguage(dictionary)
        
    def clear(self,event):
        blankLanguage = {
            "categories": {},
            "insertions": {},
            "changes": {},
            "undeletables": [],
            "order": ["bs","chg","del","harm","ins","pen"],
            "geminates": [],
            "phonotactics": {"side":"None","foot":0,"placement":1,"unstressed":"","primary stress":"","secondary stress": "","bad edge": "","can delete":False,"can insert":False},
            "codas": {},
            "vowels": [],
            "harmonies": [],
            "bad strings": [],
            "conjugations": {}
            }
        self.insertLanguage(blankLanguage)
        
    def help(self,event):
        top = Toplevel()
        top.title("OT machine GUI help")
        
        scrollbar = Scrollbar(top)
        scrollbar.pack(side=RIGHT, fill=Y)

        file = open("gui_help.txt","r")
        text = Text(top, yscrollcommand=scrollbar.set)
        text.insert('1.0',file.read())
        text.pack()
        file.close()
        
        scrollbar.config(command=text.yview)

class OrderFrame(Frame):
    def __init__(self,master):
        Frame.__init__(self,master)
        Label(self,text="order").grid(row = 0, column = 0)
        self.order = Listbox(self, selectmode = SINGLE, heigh = 6)
        for (num,item) in enumerate(["bs","chg","del","harm","ins","pen"]):
            self.order.insert(num,item)
        self.order.grid(row = 1, column = 0,rowspan = 6)
        self.up = Button(self,text="/\\")
        self.up.bind("<Button-1>",self.moveUp)
        self.up.grid(row=2,column=1)
        self.down = Button(self,text="\\/")
        self.down.bind("<Button-1>",self.moveDown)
        self.down.grid(row=3,column=1)

    def moveUp(self,event):
        num = self.order.curselection()
        if num != () and num[0] > 0:
            text = self.order.get(num[0])
            self.order.delete(num[0])
            self.order.insert(num[0] - 1, text)
            self.order.selection_set(num[0]-1)
        
    def moveDown(self,event):
        num = self.order.curselection()
        if num != () and num[0] < 5:
            text = self.order.get(num[0])
            self.order.delete(num[0])
            self.order.insert(num[0] + 1, text)
            self.order.selection_set(num[0] + 1)

    def get(self):
        return list(self.order.get(0,6))


def insertToEntry(entry,string):
    entry.delete(0,"end")
    entry.insert(0,string)