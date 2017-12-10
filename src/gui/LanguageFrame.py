from tkinter import *
import sys
import json
sys.path.append('../')
import src.controller as controller
from .PhonotacticsFrame import PhonotacticsFrame
from .ExpandingFrames import ExpandingListFrame, ListFrame, ConjugationFrame, AssimilationFrame, OrthographyFrame

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
        
        self.clearButton = Button(self.buttonFrame,text = "Clear")
        self.clearButton.bind("<Button-1>",self.clear)
        self.clearButton.grid(row = 0, column = 3)
        
        self.helpButton = Button(self.buttonFrame,text = "Help")
        self.helpButton.bind("<Button-1>",self.help)
        self.helpButton.grid(row = 0, column = 4)
        
        self.leftFrame = Frame(self)        
        self.categories = ExpandingListFrame(self.leftFrame,"Categories",["Label","Phonemes"],25)
        self.categories.pack()
        self.orderFrame = OrderFrame(self.leftFrame)
        self.orderFrame.pack()
        self.leftFrame.grid(row=1,column=0)
        
        self.centerFrame = Frame(self)
        
        self.zero = self.makeStringFrames(self.centerFrame)
        self.zero.pack(fill=X)
        
        self.one = Section(self.centerFrame,"Modifications","Changes, insertions, assimilations\nchanges in coda, traces","modifications_help")
        self.changes = ExpandingListFrame(self.one.hidingFrame,"Changes",["Original","Changed"])
        self.changes.grid(row=0,column=0)
        self.insertions = ExpandingListFrame(self.one.hidingFrame,"Insertions",["Near:","Insert a:","Where:"],3,True)
        self.insertions.grid(row=0,column=1)
        self.assimilations = ListFrame(self.one.hidingFrame,"Assimilations",AssimilationFrame)
        self.assimilations.grid(row=0,column=2)
        self.codas = ExpandingListFrame(self.one.hidingFrame,"Changes in Codas",["Original","Changed"])
        self.codas.grid(row=1,column=0)
        self.traces = ExpandingListFrame(self.one.hidingFrame,"Traces",["Sound:","Trace:"],3,True)
        self.traces.grid(row=1,column=1)
        self.tambajnaFinish = IntVar()
        self.tambajnaFinish.set(0)
        Checkbutton(self.one.hidingFrame,text = "Tambajna-like tone", variable = self.tambajnaFinish).grid(row=1,column=2)
        
        self.one.pack(fill=X)
        
        self.two = Section(self.centerFrame,"Phonotactics","","phonotactic_help")
        self.phonotacticsFrame = PhonotacticsFrame(self.two.hidingFrame)
        self.phonotacticsFrame.pack()
        self.two.pack(fill=X)
        
        self.three = Section(self.centerFrame,"Language properties","Conjugations, orthographies","language_help")
        self.conjugations = ListFrame(self.three.hidingFrame,"Conjugations",ConjugationFrame)
        self.conjugations.pack(side=LEFT)
        self.orthographies = ListFrame(self.three.hidingFrame,"Orthographies",OrthographyFrame)
        self.orthographies.pack(side=LEFT)
        self.three.pack(fill=X)
        
        self.four = Section(self.centerFrame,"Underlying phonology","Underlying phonemes, borrowing","underlying_help")
        Label(self.four.hidingFrame, text="Underlying Phonemes:").grid(row=0,column=0)
        self.underlyingPhonemes = Text(self.four.hidingFrame,width=18,height=10)
        self.underlyingPhonemes.grid(row=1,column=0)
        self.fillBullon = Button(self.four.hidingFrame,text="Guess phonemes")
        self.fillBullon.bind("<Button-1>", self.guessUnderlying)
        self.fillBullon.grid(row=2,column=0)
        self.borrow = ExpandingListFrame(self.four.hidingFrame,"Borrowing",["grapheme","phoneme"])
        self.borrow.grid(row=0,column=1,rowspan=3)
        self.four.pack(fill=X)
        
        self.centerFrame.grid(row=1,column=1)
    
        self.openText = Button(self, text = ">>\ntext input")
        self.openText.bind("<Button-1>",self.openLanguage)
        self.openText.grid(row=0, column = 2,rowspan=2)
        
        self.languageText = TextInput(self)
    
    def makeStringFrames(self,master):
        frame = Section(master,"Simple things","Vowels, Undeletable, Geminates, Bad strings","string_help")
        
        Label(frame.hidingFrame,text = "Vowels:").grid(row = 0, column = 0)
        self.vowels = Entry(frame.hidingFrame,width=36)
        self.vowels.grid(row = 0, column = 1)
        
        Label(frame.hidingFrame,text = "Undeletables:").grid(row = 1, column = 0)
        self.undeletables = Entry(frame.hidingFrame,width=36)
        self.undeletables.grid(row = 1, column = 1)
        
        Label(frame.hidingFrame,text = "Geminates:").grid(row = 2, column = 0)
        self.geminates = Entry(frame.hidingFrame,width=36)
        self.geminates.grid(row = 2, column = 1)
        
        Label(frame.hidingFrame,text = "Bad strings:").grid(row = 3, column = 0)
        self.badstrings = Entry(frame.hidingFrame,width=36)
        self.badstrings.grid(row = 3, column = 1)
        
        return frame
        
    
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
            "undeletables": self.undeletables.get().replace(' ', ',').split(',') if self.undeletables.get() else False,
            "geminates": self.geminates.get().replace(' ', ',').split(','),
            "vowels": self.vowels.get().replace(' ', ',').split(','),
            "bad strings": self.badstrings.get().replace(' ', ',').split(','),
            "order": self.orderFrame.get(),
            "traces": self.traces.get(),
            "tambajna finish": self.tambajnaFinish.get(),
            "orthographies": self.orthographies.get(),
            "underlying inventory":{
                "underlying":self.underlyingPhonemes.get('1.0',END).replace(' ', ',').split(',') if self.badstrings.get() else False,
                "borrowings":self.borrow.get()
                }
            }
        
    def getLangauge(self,event):
        self.openLanguage(event)
        language = json.dumps(self.get())
        insertToEntry(self.languageText.textbox, '1.0', language)

    def insertLanguage(self, dictionary):
        insertToEntry(self.vowels, 0, " ".join(dictionary["vowels"]))
        insertToEntry(self.geminates, 0, " ".join(dictionary["geminates"]))
        insertToEntry(self.undeletables, 0, " ".join(dictionary["undeletables"]) if dictionary["undeletables"] else "")
        insertToEntry(self.badstrings, 0, " ".join(dictionary["bad strings"]) if dictionary["bad strings"] else "")
        insertToEntry(self.underlyingPhonemes, '1.0', " ".join(dictionary["underlying inventory"]["underlying"]) if dictionary["underlying inventory"] else "")
        self.tambajnaFinish.set(dictionary["tambajna finish"])
        self.orderFrame.order.delete(0, 6)
        for num, item in enumerate(dictionary["order"]):
            self.orderFrame.order.insert(num, item)
        
        self.phonotacticsFrame.insert(dictionary["phonotactics"])
        self.categories.insert(dictionary["categories"])
        self.traces.insert(dictionary["traces"])
        self.insertions.insert(dictionary["insertions"])
        self.changes.insert(dictionary["changes"])
        self.codas.insert(dictionary["codas"])
        self.assimilations.insert(dictionary["harmonies"])
        self.conjugations.insert(dictionary["conjugations"])
        self.orthographies.insert(dictionary["orthographies"])
        self.borrow.insert(dictionary["underlying inventory"]["borrowings"])

    def insertTambajna(self,event):
        file = open("./static/tambajna_phonology.txt","r")
        dictionary = json.loads(file.read())
        file.close()
        
        self.insertLanguage(dictionary)
        
    def unfilledNecessaries(self):
        necessaries = {self.vowels:self.zero, self.phonotacticsFrame.unstressed:self.two}
        return {n:p for (n,p) in necessaries.items() if n.get() == ""}
        
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
            "traces": {},
            "tambajna finish":False,
            "conjugations": {},
            "orthographies": {},
            "underlying inventory":{"underlying":[],"borrowings":{}}
            }
        self.insertLanguage(blankLanguage)
        
    def help(self,event):
        top = Toplevel()
        top.title("OT machine GUI help")
        
        scrollbar = Scrollbar(top)
        scrollbar.pack(side=RIGHT, fill=Y)

        text = Text(top, yscrollcommand=scrollbar.set)

        for file in ["gui_overview","string_help","modifications_help","phonotactic_help","language_help","underlying_help"]:
            file = open("./static/" + file + ".txt","r")
            text.insert(END,file.read())
            file.close()
        text.pack()
        
        scrollbar.config(command=text.yview)
        
    def openLanguage(self,event = None):
        self.openText.grid_forget()
        self.languageText.grid(row=0, column = 4, rowspan = 2)
        
        
    def guessUnderlying(self,event):
        phonemes = " ".join(set(phoneme for list in self.categories.get().values() for phoneme in list))
        insertToEntry(self.underlyingPhonemes,'1.0', phonemes)

class OrderFrame(Frame):
    def __init__(self,master):
        Frame.__init__(self,master)
        Label(self,text="order").grid(row = 0, column = 0)
        self.order = Listbox(self, selectmode = SINGLE, height = 6, width = 6)
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

class TextInput(Frame):
    def __init__(self,master):
        Frame.__init__(self,master)
        
        self.closeButton = Button(self,text = "<<")
        self.closeButton.bind("<Button-1>",self.close)
        self.closeButton.grid(row = 0, column = 0)
        
        self.setButton = Button(self,text="Set the language from the text box")
        self.setButton.bind("<Button-1>",self.setLanguage)
        self.setButton.grid(row = 0, column = 1)
        
        self.clearButton = Button(self, text="clear")
        self.clearButton.grid(row=0,column=2)
        
        self.textbox = Text(self)
        self.textbox.grid(row = 1, column = 0, columnspan = 3)
        
        self.clearButton.bind('<Button-1>',lambda e: self.textbox.delete('1.0', END))
        
    def setLanguage(self,event):
        language = json.loads(self.textbox.get("1.0",END))
        self.master.insertLanguage(language)
        
    def close(self,event = None):
        self.grid_forget()
        self.master.openText.grid(row=0, column = 4, rowspan = 2)
        
class Section(Frame):
    def __init__(self,master,name,display,helpFile):
        Frame.__init__(self, master, highlightbackground="black", highlightthickness=1)
        
        self.name = name
        self.label = Label(self,text=name)
        self.label.grid(row=0,column=0)
        
        self.display = Label(self,text=display)
        self.hidingFrame = Frame(self)
        self.display.grid(row=1,column=0,columnspan=2)
        
        self.helpButton = Button(self,text="Help")
        self.helpFile = helpFile
        
        self.bind('<Enter>',self.show)
        self.bind('<Leave>',self.hide)
        self.bind('<Button-1>',self.click)
        self.hidingFrame.bind('<Button-1>',self.click)
        self.label.bind('<Button-1>',self.click)
        self.helpButton.bind('<Button-1>',self.help)
        
        self.isClicked = False
    
    def show(self,event):
        self.display.grid_forget()
        self.helpButton.grid(row=0,column=1)
        self.hidingFrame.grid(row=1,column=0,columnspan=2)
    
    def hide(self,event):
        self.helpButton.grid_forget()
        self.hidingFrame.grid_forget()
        self.display.grid(row=1,column=0,columnspan=2)
        
    def click(self,event):
        if self.isClicked:
            self.config(highlightbackground="black")
            self.isClicked = False
            self.bind('<Leave>',self.hide)
        else:
            self.config(highlightbackground="red")
            self.isClicked = True
            self.unbind('<Leave>')
        
    def help(self,event):
        top = Toplevel()
        top.title(self.name + " help")
        
        scrollbar = Scrollbar(top)
        scrollbar.pack(side=RIGHT, fill=Y)

        text = Text(top, yscrollcommand=scrollbar.set)

        
        file = open("./static/" + self.helpFile + ".txt","r")
        text.insert(END,file.read())
        file.close()
        text.pack()
        
        scrollbar.config(command=text.yview)

def insertToEntry(entry,index,string):
    entry.delete(index,END)
    entry.insert(index,string)