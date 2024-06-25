from operator import truediv
from random import *
import random
import string
import tkinter
import tools
from tkinter import *
from os.path import exists


class Imp:
    def __init__(self, name, transform, pronouns, color):
        self.name = name
        self.transform = transform
        self.pronouns = pronouns
        self.color = color

    def __str__(self):
        return f"   Name: {self.name}\n   Transform: {self.transform}\n   Pronouns: {self.pronouns}\n   Color: {self.color}"


class ImpGenerator:
    def __init__(self):
        self.settings = tools.Settings()
        self.flavors = tools.openfile("data/flavors.csv")
        self.adjectives = tools.openfile("data/adjectives.csv")
        self.nouns = tools.openfile("data/nouns.csv")
        self.colors = tools.openfile("data/colors.csv")
        self.alphabet = string.ascii_lowercase

    def Get_Pronouns(self):
        return choice(["She/Her", "He/Him", "They/Them", "Ask"])

    def Get_255(self):
        return random.randint(0, 255)

    def Get_Letter(self):
        return choice(self.alphabet)

    def Get_Upper_Letter(self):
        return self.Get_Letter().upper()

    def Get_IO(self):
        return choice(["i", "o"])

    def Get_Word_With(self, letter, listofwords):
        return choice([x for x in listofwords if x.lower().startswith(letter)])

    def Get_Flav(self, letter):
        return self.Get_Word_With(letter, self.flavors).split(",")[0].capitalize()

    def Get_Adj(self, letter):
        return self.Get_Word_With(letter, self.adjectives).capitalize()

    def Get_Noun(self, letter):
        return self.Get_Word_With(letter, self.nouns).capitalize()

    def Get_Color(self):
        return choice(self.colors)

    def Generate_An_Imp(self):
        name = (
            self.Get_Upper_Letter()
            + self.Get_Letter()
            + self.Get_Letter()
            + self.Get_IO()
        )
        letter = self.Get_Letter()
        transform = (
            f"{self.Get_Adj(letter)}! {self.Get_Flav(letter)}! {self.Get_Noun(letter)}!"
        )
        pronouns = self.Get_Pronouns()
        color = self.Get_Color()
        return Imp(name, transform, pronouns, color)
    
    def Export_An_Imp(self, export_imp:Imp):
        exportPath = self.settings.getImpsSave()
        with open(exportPath, "a+") as f:
            f.write(f"{export_imp.name},{export_imp.transform},{export_imp.pronouns},{export_imp.color}\n")


def Run_StandAlone():
    generator = ImpGenerator()
    global imp
    imp = generator.Generate_An_Imp()
    root = tkinter.Tk()
    root.title("Imp Generator")
    textWidth = 45
    labelPaddingY = (10, 0)
    padding = 10

    def regenImp():
        global imp
        imp = generator.Generate_An_Imp()
        textName.delete(1.0, END)
        textName.insert(tkinter.END, imp.name)
        textTransform.delete(1.0, END)
        textTransform.insert(tkinter.END, imp.transform)
        textPronouns.delete(1.0, END)
        textPronouns.insert(tkinter.END, imp.pronouns)
        textColor.delete(1.0, END)
        textColor.insert(tkinter.END, imp.color)
        buttonExport["state"] = "normal"

    def exportImp():
        generator.Export_An_Imp(imp)
        buttonExport["state"] = "disabled"

    labelName = Label(root, text="Name")
    labelName.pack(pady=labelPaddingY)
    textName = Text(root, height=1, width=textWidth)
    textName.pack(padx=padding)

    labelTransform = Label(root, text="Transform")
    labelTransform.pack(pady=labelPaddingY)
    textTransform = Text(root, height=1, width=textWidth)
    textTransform.pack(padx=padding)

    labelPronouns = Label(root, text="Pronouns")
    labelPronouns.pack(pady=labelPaddingY)
    textPronouns = Text(root, height=1, width=textWidth)
    textPronouns.pack(padx=padding)

    labelColor = Label(root, text="Color")
    labelColor.pack(pady=labelPaddingY)
    textColor = Text(root, height=1, width=textWidth)
    textColor.pack(padx=padding)

    buttonRegen = tkinter.Button(root, text="Regenerate", command=regenImp)
    buttonRegen.pack(pady=padding, padx=padding, in_=root, side=LEFT)
    buttonExport = tkinter.Button(root, text="Export", command=exportImp)
    buttonExport.pack(pady=padding, padx=padding, in_=root, side=LEFT)
    buttonExit = Button(root, text="Exit", command=root.destroy)
    buttonExit.pack(pady=padding, padx=padding, in_=root, side=LEFT)

    textName.insert(tkinter.END, imp.name)
    textTransform.insert(tkinter.END, imp.transform)
    textPronouns.insert(tkinter.END, imp.pronouns)
    textColor.insert(tkinter.END, imp.color)

    root.mainloop()


if __name__ == "__main__":
    Run_StandAlone()
