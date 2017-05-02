from Tkinter import *
import sys
sys.path.append('../')
from src.language import Language
import src.controller as controller

class WordsFrame(Frame):
    def __init__(self,master):
        Frame.__init__(self,master)
        Label(self, text="Category: ").grid(row = 0, column = 0)
        Label(self, text="Word: ").grid(row = 0, column = 2)

        self.language = Language(False,False)

        self.selectedConjugation = StringVar()
        self.selectedConjugation.set(" ")

        self.conjugationMenu = OptionMenu(self,self.selectedConjugation," ")
        self.conjugationMenu['menu'].add_command(label=" ", command=lambda: self.selectedConjugation.set(" "))
        self.conjugationMenu.grid(row = 0, column = 1)

        self.entry = Entry(self)
        self.entry.grid(row = 0, column = 3)
        
        self.outputSelection = StringVar()
        self.outputSelection.set("String")

        self.outputMenu = OptionMenu(self,self.outputSelection,
                                     "String","Verbose String", "XML")
        self.outputMenu.grid(row = 0, column = 4)
        
        self.submit = Button(self, text = "find surface forms")
        self.submit.bind("<Button-1>",self.surfaceForms)
        self.submit.grid(row = 0, column = 5)
        
        self.autoClear = IntVar()
        self.autoClearChoice = Checkbutton(self, text="Automatically clear", variable=self.autoClear)
        self.autoClearChoice.grid(row = 0, column = 6)
        
        self.clear = Button(self, text="Clear")
        self.clear.bind("<Button-1>",lambda entry: self.output.delete('1.0','end'))
        self.clear.grid(row=0, column = 7)

        self.output = Text(self)
        self.output.grid(row = 1, columnspan = 8)
        
    def surfaceForms(self,event):
        conjugation = self.selectedConjugation.get()
        words = self.entry.get().strip().replace(' ', ',').split(',')
        if conjugation == " ":
            entries = [self.language.entry(word) for word in words]
        else:
            entries = [self.language.conjugate(conjugation,word) for word in words]
        display = [controller.toForm[self.outputSelection.get()](entry) for entry in entries]
        if self.autoClear.get():
            self.output.delete('1.0', END)
        self.output.insert('1.0',"\n\n".join(display) + "\n\n")
            
    def updateConjugations(self):
        self.conjugationMenu['menu'].delete(1,'end')
        for conjugation in self.language.conjugations:
            self.conjugationMenu['menu'].add_command(label=conjugation, command=lambda: self.selectedConjugation.set(conjugation))
        
    