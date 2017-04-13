from Tkinter import *
from gui.WordsFrame import WordsFrame
from gui.LanguageFrame import LanguageFrame

root = Tk()

class Application:
    def __init__(self,master):
        self.frame = self.makeToggleFrame(master)
        self.languageFrame = LanguageFrame(master)
        self.wordsFrame = WordsFrame(master)
        
        self.frame.grid(row = 0)
        self.languageFrame.grid(row = 1)

    def toLanguage(self,event):
        self.wordsFrame.grid_forget()
        self.languageFrame.grid(row = 1)
        self.toLanguageButton.grid_forget()
        self.toWordsButton.grid(row = 0)
    
    def toWords(self,event):
        self.languageFrame.grid_forget()
        self.wordsFrame.grid(row = 1)
        self.toWordsButton.grid_forget()
        self.toLanguageButton.grid(row = 0)
        self.wordsFrame.language = self.languageFrame.makeLanguage()
        self.wordsFrame.updateConjugations()

    def makeToggleFrame(self,master):
        frame = Frame(master)
        
        self.toWordsButton = Button(frame, text="run the machine")
        self.toWordsButton.bind("<Button-1>",self.toWords)
        self.toLanguageButton = Button(frame, text="tinker with your language")
        self.toLanguageButton.bind("<Button-1>",self.toLanguage)
        self.toWordsButton.grid(row = 0, column = 0)
        self.aboutButton = Button(frame, text="About OT")
        self.aboutButton.bind("<Button-1>",self.about)
        self.aboutButton.grid(row = 0, column = 1)
        
        return frame
    
    def about(self,event):
        top = Toplevel()
        top.title("About OT")
        
        scrollbar = Scrollbar(top)
        scrollbar.pack(side=RIGHT, fill=Y)

        file = open("about_OT.txt","r")
        text = Text(top, yscrollcommand=scrollbar.set)
        text.insert('1.0',file.read())
        text.pack()
        file.close()
        
        scrollbar.config(command=text.yview)
    
root.title("OT machine")
app = Application(root)
root.mainloop()