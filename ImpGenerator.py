from random import *
import random
import string
import utilities.tools as tools


class Imp:
    def __init__(self, name, transform, pronouns, color):
        self.name = name
        self.transform = transform
        self.pronouns = pronouns
        self.color = color

    def __str__(self):
        return f"   Name: {self.name}\n   Transform: {self.transform}\n   Pronouns: {self.pronouns}\n   Color: {self.color}"


class ImpGenerator:
    def __init__(self, settings=None):
        if settings is None:
            settings = tools.Settings()
        self.settings = settings
        self.flavors = tools.load_resource("data/flavors.csv")
        self.adjectives = tools.load_resource("data/adjectives.csv")
        self.nouns = tools.load_resource("data/nouns.csv")
        self.colors = tools.load_resource("data/colors.csv")
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


def run_imp_gen_IU():
    settings = tools.Settings()
    generator = ImpGenerator(settings)
    global imp
    imp = generator.generate_an_imp()
    app = tools.ImparianApp("Imp Generator", settings)
    app.title("Imp Generator")
    root = app.add_frame(row=1, background=settings.get_style_primarycolor())
    textWidth = 35
    labelPaddingY = (10, 0)
    padding = 10

    def regen_imp():
        global imp
        imp = generator.generate_an_imp()
        textName.delete(1.0, "end")
        textName.insert("end", imp.name)
        textTransform.delete(1.0, "end")
        textTransform.insert("end", imp.transform)
        textPronouns.delete(1.0, "end")
        textPronouns.insert("end", imp.pronouns)
        textColor.delete(1.0, "end")
        textColor.insert("end", imp.color)
        buttonExport["state"] = "normal"

    def export_imp():
        generator.export_an_imp(imp)
        buttonExport["state"] = "disabled"

    labelName = settings.label(root, text="Name", font=settings.get_style_headerfont())
    labelName.pack(pady=labelPaddingY)
    textName = settings.text(root, height=1, width=textWidth)
    textName.pack(padx=padding)

    labelTransform = settings.label(root, text="Transform", font=settings.get_style_headerfont())
    labelTransform.pack(pady=labelPaddingY)
    textTransform = settings.text(root, height=1, width=textWidth)
    textTransform.pack(padx=padding)

    labelPronouns = settings.label(root, text="Pronouns", font=settings.get_style_headerfont())
    labelPronouns.pack(pady=labelPaddingY)
    textPronouns = settings.text(root, height=1, width=textWidth)
    textPronouns.pack(padx=padding)

    labelColor = settings.label(root, text="Color", font= settings.get_style_headerfont())
    labelColor.pack(pady=labelPaddingY)
    textColor = settings.text(root, height=1, width=textWidth)
    textColor.pack(padx=padding)

    buttonRegen = settings.button(root, text="Regenerate", command=regen_imp, background=settings.get_style_accentcolor())
    buttonRegen.pack(pady=padding, padx=padding, in_=root)
    buttonExport = settings.button(root, text="Export", command=export_imp, background=settings.get_style_accentcolor())
    buttonExport.pack(pady=padding, padx=padding, in_=root)

    textName.insert("end", imp.name)
    textTransform.insert("end", imp.transform)
    textPronouns.insert("end", imp.pronouns)
    textColor.insert("end", imp.color)

    root.mainloop()


if __name__ == "__main__":
    run_imp_gen_IU()
