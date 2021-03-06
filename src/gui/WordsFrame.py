from tkinter import *
import sys
sys.path.append('../')
import src.controller as controller
from collections import deque
from threading import Thread
import time

class WordsFrame(Frame):
    def __init__(self,master):
        Frame.__init__(self,master)
        
        self.language = False
        
        self.leftFrame().grid(row = 0, column = 0)

        self.output = Text(self)
        self.output.grid(row = 0, column = 1)
        
        self.rightFrame().grid(row = 0, column = 2)
        
        self.downLevel = 0
        
    def surfaceForms(self,event):
        self.done = False

        self.leverDown()
        self.loading_animation()
        
        conjugation = self.selectedConjugation.get()
        orthography = self.selectedOrthography.get()
        words = self.entry.get().strip().replace(' ', ',').split(',')
        newThread = ComputeThread(self,conjugation,orthography,words)

    def buttonRelease(self,event=None):
        if self.downLevel > 3:
            self.master.after(100,self.leverUp)
        else:
            self.master.after(10,self.buttonRelease)
        
    def loading_animation(self):
        if self.done:
            display = [controller.toForm[self.outputSelection.get()](entry) for entry in self.done]
            if self.autoClear.get():
                self.output.delete('1.0', END)
            self.output.insert('1.0', "\n\n".join(display) + "\n\n")
        else:
            image = self.gearsFrames.popleft()
            self.gearsLabel["image"] = image
            self.gearsFrames.append(image)
            self.update_idletasks()
            self.master.after(100, self.loading_animation)
            
    def leverDown(self):
        if self.downLevel < 4:
            self.downLevel += 1
            self.leverLabel["image"] = self.leverFrames[self.downLevel]
            self.update_idletasks()
            self.master.after(100, self.leverDown)
            
    def leverUp(self):
        if self.downLevel > 0:
            self.downLevel -= 1
            self.leverLabel["image"] = self.leverFrames[self.downLevel]
            self.master.after(10,self.leverUp)

    def update(self,language):
        self.language = language
        self.updateOptionMenu(self.conjugationMenu, self.selectedConjugation, language.conjugations)
        self.updateOptionMenu(self.orthographyMenu, self.selectedOrthography, language.orthographies)
           
    def updateOptionMenu(self, menu, selected, new_values):
        menu['menu'].delete(0,'end')
        selected.set(" ")
        menu['menu'].add_command(label=" ", command=lambda: selected.set(" "))
        for value in new_values:
            menu['menu'].add_command(label=value, command=lambda: selected.set(value))
            
    def leftFrame(self):
        frame = Frame(self)
        
        self.selectedConjugation = StringVar()
        self.selectedConjugation.set(" ")
        Label(frame, text="Category: ").pack()
        self.conjugationMenu = OptionMenu(frame,self.selectedConjugation," ")
        self.conjugationMenu['menu'].add_command(label=" ", command=lambda: self.selectedConjugation.set(" "))
        self.conjugationMenu.pack()
        
        Label(frame, text="Word: ").pack()
        self.entry = Entry(frame)
        self.entry.pack()

        self.borrow = IntVar()
        Checkbutton(frame, text="Borrow", variable=self.borrow).pack()
        
        self.selectedOrthography = StringVar()
        self.selectedOrthography.set(" ")
        Label(frame, text="Orthography: ").pack()
        self.orthographyMenu = OptionMenu(frame,self.selectedOrthography," ")
        self.orthographyMenu['menu'].add_command(label=" ", command=lambda: self.selectedOrthography.set(" "))
        self.orthographyMenu.pack()

        Label(frame, text="Compute").pack()
        self.leverLabel = Label(frame)
        self.leverLabel.pack()
        self.leverLabel.bind("<Button-1>", self.surfaceForms)
        self.leverLabel.bind("<ButtonRelease-1>", self.buttonRelease)
        self.leverFrames = [PhotoImage(file = "static/lever%d.gif" % i).subsample(9) for i in range(5)]
        self.leverLabel["image"] = self.leverFrames[0]
        
        return frame
        
    def rightFrame(self):
        frame = Frame(self)

        self.gearsLabel = Label(frame)
        self.gearsLabel.pack()
        self.gearsFrames = deque([PhotoImage(file = "static/gear%d.gif" % i).subsample(7) for i in range(6)])
        self.gearsLabel["image"] = self.gearsFrames[-1]
        
        self.outputSelection = StringVar()
        self.outputSelection.set("String")
        self.outputMenu = OptionMenu(frame,self.outputSelection,
                                     "String","Verbose String", "XML")
        self.outputMenu.pack()
        
        self.clear = Button(frame, text="Clear")
        self.clear.bind("<Button-1>",lambda event: self.output.delete('1.0','end'))
        self.clear.pack()
        
        self.autoClear = IntVar()
        Checkbutton(frame, text="Automatically clear", variable=self.autoClear).pack()
        
        self.prosody = IntVar()
        self.prosody.set(1)
        Checkbutton(frame, text="Show Prosody", variable=self.prosody).pack()
        
        return frame
    
class ComputeThread(Thread):
    def __init__(self,frame,conjugation,orthography,words):
        Thread.__init__(self)
        self.frame = frame
        self.conjugation = conjugation
        if orthography == " ":
            self.orthography = False
        else:
            self.orthography = orthography
        self.words = words
        self.daemon = True
        self.start()
        
    def run(self):
        removeProsody = not(self.frame.prosody.get())
        borrow = self.frame.borrow.get()
        
        if self.conjugation == " ":
            entries = [self.frame.language.entry(word,self.orthography,removeProsody,borrow) for word in self.words]
        elif borrow:
            entries = [entry for word in self.words for entry in self.frame.language.bestConjugation(self.conjugation,word,self.orthography,removeProsody)]
        else:
            entries = [self.frame.language.conjugate(self.conjugation, word, self.orthography, removeProsody) for word in self.words]
        self.frame.done = entries