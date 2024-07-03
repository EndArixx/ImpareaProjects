from random import *
import random
import string
import tkinter
import utilities.tools as tools
from tkinter import *


class Imp:
    def __init__(self, name, transform, pronouns, color):
        self.name = name
        self.transform = transform
        self.pronouns = pronouns
        self.color = color

    def __str__(self):
        return f"   Name: {self.name}\n   Transform: {self.transform}\n   Pronouns: {self.pronouns}\n   Color: {self.color}"


class ImpGenerator:
    def __init__(self, settings= None):
        if settings is None:
            settings = tools.Settings()
        self.settings = settings
        self.flavors = tools.open_file("data/flavors.csv")
        self.adjectives = tools.open_file("data/adjectives.csv")
        self.nouns = tools.open_file("data/nouns.csv")
        self.colors = tools.open_file("data/colors.csv")
        self.alphabet = string.ascii_lowercase

    def get_pronouns(self):
        return choice(["She/Her", "He/Him", "They/Them", "Ask"])

    def get_255(self):
        return random.randint(0, 255)

    def get_letter(self):
        return choice(self.alphabet)

    def get_upper_letter(self):
        return self.get_letter().upper()

    def get_io(self):
        return choice(["i", "o"])

    def get_word_with(self, letter, listofwords):
        return choice([x for x in listofwords if x.lower().startswith(letter)])

    def get_flav(self, letter):
        return self.get_word_with(letter, self.flavors).split(",")[0].capitalize()

    def get_adj(self, letter):
        return self.get_word_with(letter, self.adjectives).capitalize()

    def get_noun(self, letter):
        return self.get_word_with(letter, self.nouns).capitalize()

    def get_color(self):
        return choice(self.colors)

    def generate_an_imp(self):
        name = (
            self.get_upper_letter()
            + self.get_letter()
            + self.get_letter()
            + self.get_io()
        )
        letter = self.get_letter()
        transform = (
            f"{self.get_adj(letter)}! {self.get_flav(letter)}! {self.get_noun(letter)}!"
        )
        pronouns = self.get_pronouns()
        color = self.get_color()
        return Imp(name, transform, pronouns, color)

    def export_an_imp(self, export_imp: Imp):
        exportPath = self.settings.get_imps_save()
        with open(exportPath, "a+") as f:
            f.write(
                f"{export_imp.name},{export_imp.transform},{export_imp.pronouns},{export_imp.color}\n"
            )


def run_standAlone():
    settings = tools.Settings()
    generator = ImpGenerator(settings)
    global imp
    imp = generator.generate_an_imp()
    app = tools.ImparianApp("Imp Generator", settings)
    app.title("Imp Generator")
    root = app.add_frame(row=1, color=settings.get_style_primarycolor())
    textWidth = 45
    labelPaddingY = (10, 0)
    padding = 10

    def regen_imp():
        global imp
        imp = generator.generate_an_imp()
        textName.delete(1.0, END)
        textName.insert(tkinter.END, imp.name)
        textTransform.delete(1.0, END)
        textTransform.insert(tkinter.END, imp.transform)
        textPronouns.delete(1.0, END)
        textPronouns.insert(tkinter.END, imp.pronouns)
        textColor.delete(1.0, END)
        textColor.insert(tkinter.END, imp.color)
        buttonExport["state"] = "normal"

    def export_imp():
        generator.export_an_imp(imp)
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

    buttonRegen = tkinter.Button(root, text="Regenerate", command=regen_imp)
    buttonRegen.pack(pady=padding, padx=padding, in_=root, side=LEFT)
    buttonExport = tkinter.Button(root, text="Export", command=export_imp)
    buttonExport.pack(pady=padding, padx=padding, in_=root, side=LEFT)

    textName.insert(tkinter.END, imp.name)
    textTransform.insert(tkinter.END, imp.transform)
    textPronouns.insert(tkinter.END, imp.pronouns)
    textColor.insert(tkinter.END, imp.color)

    root.mainloop()


if __name__ == "__main__":
    run_standAlone()
