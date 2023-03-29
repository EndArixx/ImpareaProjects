from operator import truediv
from random import *
import random
import tkinter
from tkinter import *
from os.path import exists

def openfile(str): return open(str, 'r').read().split('\n')
flavors = openfile("data/flavors.csv")
adjectives = openfile("data/adjectives.csv")
nouns = openfile("data/nouns.csv")
colors = openfile("data/colors.csv")
alphabet = list("abcdefghijklmnopqrstuvwxyz")

def Get_Pronouns(): 
    return choice(["She/Her","He/Him","They/Them","Ask"])
def Get_255(): 
    return random.randint(0,255)
def Get_Letter(): 
    return choice(alphabet)
def Get_Upper_Letter(): 
    return Get_Letter().upper()
def Get_IO(): 
    return choice(['i','o']) 
def Get_Word_With(letter, listofwords):
    return choice([x for x in listofwords if x.lower().startswith(letter)])
def Get_Flav(letter): 
    return  Get_Word_With(letter,flavors).split(',')[0].capitalize()
def Get_Adj(letter): 
    return  Get_Word_With(letter, adjectives).capitalize()
def Get_Noun(letter): 
    return  Get_Word_With(letter, nouns).capitalize()
def Get_Color(): 
    return  choice(colors)

class Imp:
    def __init__(self, name, transform, pronouns, color):
        self.name = name
        self.transform = transform
        self.pronouns = pronouns
        self.color = color
    def __str__(self):
        return f"   Name: {self.name}\n   Transform: {self.transform}\n   Pronouns: {self.pronouns}\n   Color: {self.color}"


def Generate_An_Imp():
    name = Get_Upper_Letter() + Get_Letter() +Get_Letter() +  Get_IO()
    letter = Get_Letter()
    transform = f"{Get_Adj(letter)}! {Get_Flav(letter)}! {Get_Noun(letter)}!"
    pronouns = Get_Pronouns()
    color = Get_Color()
    return Imp(name, transform, pronouns, color)



def UI():
    global imp
    imp = Generate_An_Imp()
    root = tkinter.Tk()
    root.title('Imp Generator')
    textWidth = 45
    labelPaddingY = (10,0) 
    padding = 10

    def regenImp():
        global imp 
        imp = Generate_An_Imp()
        textName.delete(1.0,END)
        textName.insert(tkinter.END, imp.name)
        textTransform.delete(1.0,END)
        textTransform.insert(tkinter.END, imp.transform)
        textPronouns.delete(1.0,END)
        textPronouns.insert(tkinter.END, imp.pronouns)
        textColor.delete(1.0,END)
        textColor.insert(tkinter.END, imp.color)
        buttonExport["state"] = "normal"

    def exportImp():
        exportPath = 'Imps.csv'
        if not exists(exportPath):
            export = open(exportPath, 'w+')
            export.write("Name,Transform,Pronouns,Color\n")
        else:
            export = open(exportPath, 'a+')    
        export.write(f"{imp.name},{imp.transform},{imp.pronouns},{imp.color}\n")
        export.close()
        buttonExport["state"] = "disabled"
        


    labelName = Label(root, text="Name")
    labelName.pack(pady=labelPaddingY)
    textName = Text(root, height = 1, width = textWidth)
    textName.pack(padx=padding)

    labelTransform = Label(root, text="Transform")
    labelTransform.pack(pady=labelPaddingY)
    textTransform = Text(root, height = 1, width = textWidth)
    textTransform.pack(padx=padding)

    labelPronouns = Label(root, text="Pronouns")
    labelPronouns.pack(pady=labelPaddingY)
    textPronouns = Text(root, height = 1, width = textWidth)
    textPronouns.pack(padx=padding)

    labelColor = Label(root, text="Color")
    labelColor.pack(pady=labelPaddingY)
    textColor = Text(root, height = 1, width = textWidth)
    textColor.pack(padx=padding)

    buttonRegen = tkinter.Button(root, text ="Regenerate", command = regenImp)
    buttonRegen.pack(pady=padding,padx=padding,in_=root, side=LEFT)
    buttonExport = tkinter.Button(root, text ="Export", command = exportImp)
    buttonExport.pack(pady=padding,padx=padding,in_=root, side=LEFT)
    buttonExit = Button(root, text="Exit", command=root.destroy)
    buttonExit.pack(pady=padding,padx=padding,in_=root, side=LEFT)

    textName.insert(tkinter.END, imp.name)
    textTransform.insert(tkinter.END, imp.transform)
    textPronouns.insert(tkinter.END, imp.pronouns)
    textColor.insert(tkinter.END, imp.color)

    root.mainloop()
UI()
