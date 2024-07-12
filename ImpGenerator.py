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


class Tags:
    edit_tag = "EDIT_IMP"
    grid_tag = "SHOW_GRID"


class ImpFactory:
    def __init__(self, settings=None):
        if settings is None:
            settings = tools.Settings()
        self.settings = settings
        self.flavors = tools.load_resource("data/flavors.csv")
        self.adjectives = tools.load_resource("data/adjectives.csv")
        self.nouns = tools.load_resource("data/nouns.csv")
        self.alphabet = string.ascii_lowercase

        self.padding = self.settings.get_style_padding()

    # region Gets
    def get_dumi(self):
        return Imp("Dumi", "Public", "Plain", "Placeholder", "Ask", "#8008E1")

    def get_empi(self):
        return Imp("", "", "", "", "", "#FFFFFF")

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

    # endregion

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

    # region UI zones

    def load_vars_from_imp(self, imp):
        self.name_var.set(imp.name)
        self.adj_var.set(imp.adjective)
        self.flavor_var.set(imp.flavor)
        self.noun_var.set(imp.noun)
        self.pronouns_var.set(imp.pronouns)
        self.color_var.set(imp.color)

    def add_frame(self, root, row):
        frame = self.settings.frame(root)
        frame.grid(
            row=row,
            column=0,
            columnspan=2,
            sticky="news",
            padx=self.padding,
            pady=self.padding,
        )
        return frame

    def imp_management_zone(self, frame, tag=""):
        self.tab_var = tk.StringVar(frame, "")
        selectedimp = self.get_empi()

        for i in range(2):
            frame.grid_columnconfigure(i, weight=1)

        def turn_off(button, frame):
            button.configure({"background": self.settings.get_style_secondarycolor()})
            button.configure({"font": self.settings.get_style_textfont()})
            frame.grid_remove()

        def turn_on(button, frame):
            frame.grid()
            button.configure({"background": self.settings.get_style_primarycolor()})
            button.configure({"font": self.settings.get_style_headerfont()})

        def open(tag):
            turn_off(button_edit_imp, edit_frame)
            turn_off(button_show_imps, grid_frame)

            if tag == self.tab_var.get():
                self.tab_var.set("")
            else:
                match tag:
                    case Tags.edit_tag:
                        turn_on(button_edit_imp, edit_frame)

                    case Tags.grid_tag:
                        turn_on(button_show_imps, grid_frame)

                self.tab_var.set(tag)

        def show_edit():
            open(Tags.edit_tag)

        def show_grid():
            open(Tags.grid_tag)

        button_show_imps = self.settings.button(
            frame,
            "Imps",
            show_grid,
            highlightthickness=0,
            bd=0,
            width=15,
        )
        button_show_imps.grid(
            row=1, column=0, sticky="ew", padx=self.padding, pady=self.padding
        )
        button_edit_imp = self.settings.button(
            frame,
            "Create/Edit Imp",
            show_edit,
            highlightthickness=0,
            bd=0,
            width=15,
        )
        button_edit_imp.grid(
            row=1, column=1, sticky="ew", padx=self.padding, pady=self.padding
        )

        grid_frame = self.add_frame(frame, 2)
        self.imp_grid_zone(grid_frame)
        grid_frame.grid_remove()

        edit_frame = self.add_frame(frame, 3)
        self.imp_edit_zone(edit_frame, selectedimp)
        edit_frame.grid_remove()

        open(tag)

    def imp_grid_zone(self, frame):
        # TODO implemement
        frame.grid_columnconfigure(0, weight=1)

        DUMMY = self.settings.label(
            frame,
            "THIS IS AN IMP PLACEHOLDER!",
            background=self.settings.get_style_warningcolor(),
            foreground=self.settings.get_style_warningtextcolor(),
        )
        DUMMY.grid(row=0, column=0, sticky="news", padx=self.padding, pady=self.padding)

    def imp_edit_zone(self, frame, imp: Imp):
        self.name_var = tk.StringVar(frame, imp.name)
        self.adj_var = tk.StringVar(frame, imp.adjective)
        self.flavor_var = tk.StringVar(frame, imp.flavor)
        self.noun_var = tk.StringVar(frame, imp.noun)
        self.pronouns_var = tk.StringVar(frame, imp.pronouns)
        self.color_var = tk.StringVar(frame, imp.color)

        def randomize_button_press():
            self.load_vars_from_imp(self.generate_an_imp())

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

        for j in range(6):
            frame.grid_columnconfigure(j, weight=1)

        i = 0

        label_name = self.settings.label(
            frame, text="Name", font=self.settings.get_style_headerfont()
        )
        label_name.grid(
            row=i,
            column=0,
            columnspan=6,
            sticky="ew",
            padx=self.padding,
            pady=self.padding,
        )
        i += 1
        text_name = self.settings.entry(frame, self.name_var, justify="center")
        text_name.grid(
            row=i,
            column=1,
            columnspan=4,
            sticky="we",
            padx=self.padding,
            pady=self.padding,
        )
        i += 1

        label_pronouns = self.settings.label(
            frame, text="Pronouns", font=self.settings.get_style_headerfont()
        )
        label_pronouns.grid(
            row=i,
            column=0,
            columnspan=6,
            sticky="ew",
            padx=self.padding,
            pady=self.padding,
        )
        i += 1

        text_pronouns = self.settings.entry(frame, self.pronouns_var, justify="center")
        text_pronouns.grid(
            row=i,
            column=1,
            columnspan=4,
            sticky="we",
            padx=self.padding,
            pady=self.padding,
        )
        i += 1

        label_transform = self.settings.label(
            frame, text="Transform", font=self.settings.get_style_headerfont()
        )
        label_transform.grid(
            row=i,
            column=0,
            columnspan=6,
            sticky="ew",
            padx=self.padding,
            pady=self.padding,
        )
        i += 1

        label_adj = self.settings.label(
            frame, text="Adjective"
        )
        label_adj.grid(
            row=i,
            column=0,
            columnspan=2,
            sticky="ew",
            padx=self.padding,
            pady=self.padding,
        )
        label_flavor = self.settings.label(
            frame, text="Flavor"
        )
        label_flavor.grid(
            row=i,
            column=2,
            columnspan=2,
            sticky="ew",
            padx=self.padding,
            pady=self.padding,
        )
        label_noun = self.settings.label(
            frame, text="Noun"
        )
        label_noun.grid(
            row=i,
            column=4,
            columnspan=2,
            sticky="ew",
            padx=self.padding,
            pady=self.padding,
        )
        i += 1

        text_adj = self.settings.entry(frame, self.adj_var, justify="center")
        text_adj.grid(
            row=i,
            column=0,
            columnspan=2,
            sticky="we",
            padx=self.padding,
            pady=self.padding,
        )
        text_flavor = self.settings.entry(frame, self.flavor_var, justify="center")
        text_flavor.grid(
            row=i,
            column=2,
            columnspan=2,
            sticky="we",
            padx=self.padding,
            pady=self.padding,
        )
        text_noun = self.settings.entry(frame, self.noun_var, justify="center")
        text_noun.grid(
            row=i,
            column=4,
            columnspan=2,
            sticky="we",
            padx=self.padding,
            pady=self.padding,
        )
        i += 1

        label_color = self.settings.label(
            frame, text="Color", font=self.settings.get_style_headerfont()
        )
        label_color.grid(
            row=i,
            column=0,
            columnspan=6,
            sticky="ew",
            padx=self.padding,
            pady=self.padding,
        )
        i += 1

        button_color = self.settings.button(
            frame,
            text=self.color_var.get(),
            command=pick_color,
            background=self.color_var.get(),
        )
        button_color.grid(
            row=i,
            column=1,
            columnspan=4,
            sticky="we",
            padx=self.padding,
            pady=self.padding,
        )
        i += 1

        button_random = self.settings.button(
            frame,
            text="Randomize",
            command=randomize_button_press,
            background=self.settings.get_style_accentcolor(),
        )
        button_random.grid(
            row=i,
            column=0,
            columnspan=2,
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
            row=i,
            column=4,
            columnspan=2,
            sticky="we",
            padx=self.padding,
            pady=self.padding,
        )
        button_save["state"] = "disabled"
        i += 1

    def run_imp_gen_IU(self):
        global imp
        app = tools.ImparianApp("Imp Generator", self.settings, minwidth=700)
        app.title("Imp Generator")

        frame = app.add_frame(row=1)
        self.imp_management_zone(frame, tag=Tags.edit_tag)

        frame.mainloop()

    # endregion


if __name__ == "__main__":
    gen = ImpFactory()
    gen.run_imp_gen_IU()
