from random import *
import random
import string
import tkinter as tk
from tkinter import colorchooser
import utilities.tools as tools


class Imp:
    def __init__(self, name, adjective, flavor, noun, pronouns, color):
        self.name = name

        self.adjective = adjective
        self.flavor = flavor
        self.noun = noun
        self.transform = lambda: f"{self.adjective}! {self.flavor}! {self.noun}!"

        self.pronouns = pronouns
        self.color = color

    def __str__(self):
        return f"   Name: {self.name}\n   Transform: {self.transform()}\n   Pronouns: {self.pronouns}\n   Color: {self.color}"


class ImpGenerator:
    def __init__(self, settings=None):
        if settings is None:
            settings = tools.Settings()
        self.settings = settings
        self.flavors = tools.load_resource("data/flavors.csv")
        self.adjectives = tools.load_resource("data/adjectives.csv")
        self.nouns = tools.load_resource("data/nouns.csv")
        self.alphabet = string.ascii_lowercase

        self.padding = self.settings.get_style_padding()

    def get_dumi(self):
        return Imp("Dumi", "Public", "Plain", "Placeholder", "Ask", "#8008E1")

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
        r = lambda: random.randint(0, 255)
        return "#%02X%02X%02X" % (r(), r(), r())

    def generate_an_imp(self):
        name = (
            self.get_upper_letter()
            + self.get_letter()
            + self.get_letter()
            + self.get_io()
        )
        letter = self.get_letter()
        adjective = self.get_adj(letter)
        flavor = self.get_flav(letter)
        noun = self.get_noun(letter)
        pronouns = self.get_pronouns()
        color = self.get_color()

        imp = Imp(name, adjective, flavor, noun, pronouns, color)

        self.settings.print_debug(f"Generating Random Imp:\n{imp}")
        return imp

    def save_imp(self, export_imp: Imp):
        exportPath = self.settings.get_imps_save()
        with open(exportPath, "a+") as f:
            f.write(
                f"{export_imp.name},{export_imp.transform},{export_imp.pronouns},{export_imp.color}\n"
            )

    def load_vars_from_imp(self, imp):
        self.name_var.set(imp.name)
        self.adj_var.set(imp.adjective)
        self.flavor_var.set(imp.flavor)
        self.noun_var.set(imp.noun)
        self.pronouns_var.set(imp.pronouns)
        self.color_var.set(imp.color)

    def edit_imp_zone(self, frame, imp):
        self.name_var = tk.StringVar(frame, imp.name)
        self.adj_var = tk.StringVar(frame, imp.adjective)
        self.flavor_var = tk.StringVar(frame, imp.flavor)
        self.noun_var = tk.StringVar(frame, imp.noun)
        self.pronouns_var = tk.StringVar(frame, imp.pronouns)
        self.color_var = tk.StringVar(frame, imp.color)

        def save_button_press():
            # TODO implement new version
            print("NONE fuctioning")
            self.save_imp(imp)

        def pick_color():
            color = colorchooser.askcolor(
                title="Choose color", color=self.color_var.get()
            )[1]
            if color is not None:
                self.color_var.set(color)
                update_imp()

        def update_imp(*args):
            imp.name = self.name_var.get()
            imp.adjective = self.adj_var.get()
            imp.flavor = self.flavor_var.get()
            imp.noun = self.noun_var.get()
            imp.pronouns = self.pronouns_var.get()
            imp.color = self.color_var.get()
            button_color.configure({"background": imp.color})
            button_color.configure({"text": imp.color})

        self.name_var.trace_add("write", update_imp)
        self.adj_var.trace_add("write", update_imp)
        self.flavor_var.trace_add("write", update_imp)
        self.noun_var.trace_add("write", update_imp)
        self.pronouns_var.trace_add("write", update_imp)
        self.color_var.trace_add("write", update_imp)

        frame.grid_columnconfigure(0, weight=3)
        frame.grid_columnconfigure(1, weight=2)
        frame.grid_columnconfigure(2, weight=2)
        frame.grid_columnconfigure(3, weight=2)

        label_name = self.settings.label(
            frame, text="Name", font=self.settings.get_style_headerfont()
        )
        label_name.grid(
            row=0, column=0, sticky="w", padx=self.padding, pady=self.padding
        )
        text_name = self.settings.entry(frame, self.name_var)
        text_name.grid(
            row=0,
            column=1,
            columnspan=3,
            sticky="we",
            padx=self.padding,
            pady=self.padding,
        )

        label_transform = self.settings.label(
            frame, text="Transform", font=self.settings.get_style_headerfont()
        )
        label_transform.grid(
            row=1, column=0, sticky="w", padx=self.padding, pady=self.padding
        )
        text_adj = self.settings.entry(frame, self.adj_var)
        text_adj.grid(
            row=1, column=1, sticky="we", padx=self.padding, pady=self.padding
        )
        text_flavor = self.settings.entry(frame, self.flavor_var)
        text_flavor.grid(
            row=1, column=2, sticky="we", padx=self.padding, pady=self.padding
        )
        text_noun = self.settings.entry(frame, self.noun_var)
        text_noun.grid(
            row=1, column=3, sticky="we", padx=self.padding, pady=self.padding
        )

        label_pronouns = self.settings.label(
            frame, text="Pronouns", font=self.settings.get_style_headerfont()
        )
        label_pronouns.grid(
            row=2, column=0, sticky="w", padx=self.padding, pady=self.padding
        )
        text_pronouns = self.settings.entry(frame, self.pronouns_var)
        text_pronouns.grid(
            row=2,
            column=1,
            columnspan=3,
            sticky="we",
            padx=self.padding,
            pady=self.padding,
        )

        label_color = self.settings.label(
            frame, text="Color", font=self.settings.get_style_headerfont()
        )
        label_color.grid(
            row=3, column=0, sticky="w", padx=self.padding, pady=self.padding
        )
        button_color = self.settings.button(
            frame,
            text=self.color_var.get(),
            command=pick_color,
            background=self.color_var.get(),
        )
        button_color.grid(
            row=3,
            column=1,
            columnspan=3,
            sticky="we",
            padx=self.padding,
            pady=self.padding,
        )

        button_save = self.settings.button(
            frame,
            text="Save",
            command=save_button_press,
            background=self.settings.get_style_accentcolor(),
        )
        button_save.grid(
            row=4, column=3, sticky="we", padx=self.padding, pady=self.padding
        )
        button_save["state"] = "disabled"

    def create_random_zone(self, frame):
        def gen_ran_imp():
            self.load_vars_from_imp(self.generate_an_imp())
            
        self.edit_imp_zone(frame, self.generate_an_imp())

        button_random = self.settings.button(
            frame,
            text="Randomize",
            command=gen_ran_imp,
            background=self.settings.get_style_accentcolor(),
        )
        button_random.grid(
            row=frame.grid_size()[1]-1, column=1, sticky="we", padx=self.padding, pady=self.padding
        )

    def run_imp_gen_IU(self):
        global imp
        app = tools.ImparianApp("Imp Generator", self.settings)
        app.title("Imp Generator")

        frame = app.add_frame(row=1)
        self.create_random_zone(frame)

        frame.mainloop()


if __name__ == "__main__":
    gen = ImpGenerator()
    gen.run_imp_gen_IU()
