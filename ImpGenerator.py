from random import *
import random
import string
import tkinter as tk
from tkinter import colorchooser
from tkinter.filedialog import askopenfilename, asksaveasfilename
from typing import Dict, List
import utilities.tools as tools


class Imp:
    def __init__(
        self,
        name: str,
        adjective: str,
        flavor: str,
        noun: str,
        pronouns: str,
        glowcolor: tools.Color,
        skincolor: tools.Color,
        dullcolor: tools.Color,
    ):
        self.name = name
        self.adjective = adjective
        self.flavor = flavor
        self.noun = noun
        self.transform = lambda: f"{self.adjective}! {self.flavor}! {self.noun}!"
        self.pronouns = pronouns
        self.glowcolor = glowcolor
        self.skincolor = skincolor
        self.dullcolor = dullcolor
        # name,adjective,flavor,noun,pronoun,glowcolor,skincolor,dullcolor
        self.filestring = (
            lambda: f"{self.name},{self.adjective},{self.flavor},{self.noun},{self.pronouns},{self.glowcolor},{self.skincolor},{self.dullcolor}"
        )

    @classmethod
    def create_imp_from_filestring(self, filestring):
        if len(filestring) == 0:
            return None
        if filestring[0] == "#":
            return None
        data = filestring.split(",")
        if len(data) != 8:
            print(f"Error, filestring could not be parsed:\n {filestring}")
            return None

        imp = Imp(
            data[0],
            data[1],
            data[2],
            data[3],
            data[4],
            tools.Color(data[5]),
            tools.Color(data[6]),
            tools.Color(data[7]),
        )

        return imp

    def __str__(self):
        return f"   Name: {self.name}\n   Transform: {self.transform()}\n   Pronouns: {self.pronouns}\n   Glow Color: {self.glowcolor}, Skin Color: {self.skincolor}, Dull Color: {self.dullcolor}"

    def set_glowcolor(self, color_str):
        self.glowcolor = tools.Color(color_str)

    def set_skincolor(self, color_str):
        self.skincolor = tools.Color(color_str)

    def set_dullcolor(self, color_str):
        self.dullcolor = tools.Color(color_str)

    @classmethod
    def get_empi(self):
        return Imp("", "", "", "", "", "#FFFFFF", "#A6A6A6", "#3B3B3B")


class Tags:
    edit_tag = "EDIT_IMP"
    grid_tag = "SHOW_GRID"


IMP_FILE_FORMAT = ".csv"


class ImpFactory(tools.close_warning):
    def __init__(self, settings=None):
        if settings is None:
            settings = tools.Settings()
        self.settings = settings
        self.flavors = tools.load_resource("data/flavors.csv")
        self.adjectives = tools.load_resource("data/adjectives.csv")
        self.nouns = tools.load_resource("data/nouns.csv")
        self.pronouns = tools.load_resource("data/pronouns.csv")
        self.alphabet = string.ascii_lowercase
        self.imps_primaryfile = self.settings.get_imps_save()
        self.grid_columns = []
        self.edit_imp = Imp.get_empi()
        self.imps = {}
        self.load_imps_from_primaryfile()

        self.has_grid_changes_warning = False

        self.padding = self.settings.get_style_padding()

    # region Gets
    def get_pronouns(self):
        return choice(self.pronouns)

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
        glowcolor = tools.Color.get_random_color()
        skincolor = tools.Color.get_random_color()
        dullcolor = tools.Color.get_random_color()

        imp = Imp(
            name, adjective, flavor, noun, pronouns, glowcolor, skincolor, dullcolor
        )

        self.settings.print_debug(f"Generating Random Imp:\n{imp}")
        return imp

    # region File Stuph

    def save_imps_to_fileprompt(self):
        url = asksaveasfilename(
            title="Save Imps to CSV", filetypes=[("CSV files", f"*{IMP_FILE_FORMAT}")]
        )
        if url:
            if url[-4:] != IMP_FILE_FORMAT:
                url = url + IMP_FILE_FORMAT
            self.save_imps_to_file(url)

    def save_imps_to_primaryfile(self):
        self.save_imps_to_file(self.imps_primaryfile)

    def save_imps_to_file(self, file):
        self.settings.print_debug(f"Saving Imps to '{file}'.")
        text = "#name,adjective,flavor,noun,pronoun,glowcolor,skincolor,dullcolor\n"
        for imp in self.imps.values():
            text += f"{imp.filestring()}\n"
        tools.overwrite_file(text, file)
        self.turn_off_warning()

    def load_imps_from_fileprompt(self):
        url = askopenfilename(
            title="Import Imp CSV", filetypes=[("CSV files", f"*{IMP_FILE_FORMAT}")]
        )
        if url:
            self.load_imps_from_file(url)
            self.refreshgrid()

    def load_imps_from_primaryfile(self):
        self.load_imps_from_file(self.imps_primaryfile)

    def load_imps_from_file(self, file):
        self.settings.print_debug(f"Loading Imps!\n  '{file}'")

        data = tools.open_file(file)
        for i in data:
            imp = Imp.create_imp_from_filestring(i)
            if imp is not None:
                if imp.name in self.imps:
                    #todo, add YesToAll and NoToAll
                    result = tk.messagebox.askyesno(
                        title=f"Override Imp?",
                        message=f"Do you want to override {imp.name}?\n {imp}",
                    )
                    if not result:
                        self.settings.print_debug(f"    {imp.name} Skipped.")
                        continue
                self.imps[imp.name] = imp
                self.settings.print_debug(f"    {imp.name} Loaded.")

    # endregion

    # region Warning methods

    def fire_warning(self) -> bool:
        if self.has_grid_changes_warning:
            result = tk.messagebox.askyesno(
                title=f"Unsaved changes to Imp Grid.",
                message=f"Are you sure you wish to close with unsaved Imp changes?",
                icon="warning",
            )
            if not result:
                return False
        return True

    def change_warning(self, bool: bool):
        self.has_grid_changes_warning = bool

        if bool:
            self.button_save_grid.configure(
                {"background": self.settings.get_style_warningcolor()}
            )
            self.button_save_grid.configure(
                {"foreground": self.settings.get_style_warningtextcolor()}
            )
            self.button_save_grid.configure(
                {"font": self.settings.get_style_headerfont()}
            )
            self.button_save_grid_as.configure(
                {"background": self.settings.get_style_warningcolor()}
            )
            self.button_save_grid_as.configure(
                {"foreground": self.settings.get_style_warningtextcolor()}
            )
            self.button_save_grid_as.configure(
                {"font": self.settings.get_style_headerfont()}
            )
        else:
            self.button_save_grid.configure(
                {"background": self.settings.get_style_secondarycolor()}
            )
            self.button_save_grid.configure(
                {"foreground": self.settings.get_style_secondarytextcolor()}
            )
            self.button_save_grid.configure(
                {"font": self.settings.get_style_textfont()}
            )
            self.button_save_grid_as.configure(
                {"background": self.settings.get_style_secondarycolor()}
            )
            self.button_save_grid_as.configure(
                {"foreground": self.settings.get_style_secondarytextcolor()}
            )
            self.button_save_grid_as.configure(
                {"font": self.settings.get_style_textfont()}
            )

        self.button_save_grid.grid()

    def turn_on_warning(self):
        self.change_warning(True)

    def turn_off_warning(self):
        self.change_warning(False)

    # endregion

    # region UI zones

    def load_vars_from_imp(self, imp: Imp):
        self.name_var.set(imp.name)
        self.adj_var.set(imp.adjective)
        self.flavor_var.set(imp.flavor)
        self.noun_var.set(imp.noun)
        self.pronouns_var.set(imp.pronouns)
        self.glowcolor_var.set(imp.glowcolor)
        self.skincolor_var.set(imp.skincolor)
        self.dullcolor_var.set(imp.dullcolor)

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

    def turn_off_button(self, button, frame):
        button.configure({"background": self.settings.get_style_secondarycolor()})
        button.configure({"foreground": self.settings.get_style_secondarytextcolor()})
        button.configure({"font": self.settings.get_style_textfont()})
        frame.grid_remove()

    def turn_on_button(self, button, frame):
        frame.grid()
        button.configure({"background": self.settings.get_style_primarycolor()})
        button.configure({"foreground": self.settings.get_style_primarytextcolor()})
        button.configure({"font": self.settings.get_style_headerfont()})

    def open_panel(self, tag):
        self.turn_off_button(self.button_edit_imp, self.edit_frame)
        self.turn_off_button(self.button_show_imps, self.grid_frame)

        if tag == self.tab_var.get():
            self.tab_var.set("")
        else:
            match tag:
                case Tags.edit_tag:
                    self.turn_on_button(self.button_edit_imp, self.edit_frame)

                case Tags.grid_tag:
                    self.turn_on_button(self.button_show_imps, self.grid_frame)

            self.tab_var.set(tag)

    def imp_management_zone(self, frame, tag=""):
        self.tab_var = tk.StringVar(frame, "")

        for i in range(2):
            frame.grid_columnconfigure(i, weight=1)

        def show_edit():
            self.open_panel(Tags.edit_tag)

        def show_grid():
            self.open_panel(Tags.grid_tag)

        self.button_show_imps = self.settings.button(
            frame,
            "Imps",
            show_grid,
            highlightthickness=0,
            bd=0,
            width=15,
        )
        self.button_show_imps.grid(
            row=1, column=0, sticky="ew", padx=self.padding, pady=self.padding
        )
        self.button_edit_imp = self.settings.button(
            frame,
            "Create/Edit Imp",
            show_edit,
            highlightthickness=0,
            bd=0,
            width=15,
        )
        self.button_edit_imp.grid(
            row=1, column=1, sticky="ew", padx=self.padding, pady=self.padding
        )

        self.grid_frame = self.add_frame(frame, 2)
        self.imp_grid_zone(self.grid_frame)
        self.grid_frame.grid_remove()

        self.edit_frame = self.add_frame(frame, 3)
        self.imp_edit_zone(self.edit_frame)
        self.edit_frame.grid_remove()

        self.open_panel(tag)

    def refreshgrid(self):
        if len(self.grid_columns) > 0:
            for row in self.grid_columns:
                if len(row) > 0:
                    for cell in row:
                        cell.destroy()
            self.grid_columns = []
        i = 1

        def edit(target):
            self.settings.print_debug(f"Editing {target}")
            imp = self.imps[target]
            self.load_vars_from_imp(imp)
            self.open_panel(Tags.edit_tag)

        def delete(target):
            result = tk.messagebox.askyesno(
                title=f"Delete {target}",
                message=f"Are you sure you wish to delete {target}?",
            )
            if result:
                if self.imps.pop(target):
                    self.settings.print_debug(f"  Removed {target} from grid")
                    self.refreshgrid()
                else:
                    self.settings.print_debug(
                        f"ERROR: Failed to remove {target} from grid"
                    )

        for imp in self.imps.values():
            row = []
            row.append(
                self.settings.label(
                    self.imp_frame, imp.name, borderwidth=1, relief="solid"
                )
            )
            row[0].grid(row=i, column=0, sticky="news")

            row.append(
                self.settings.label(
                    self.imp_frame, imp.transform(), borderwidth=1, relief="solid"
                )
            )
            row[1].grid(row=i, column=1, sticky="news")

            row.append(
                self.settings.label(
                    self.imp_frame, imp.pronouns, borderwidth=1, relief="solid"
                )
            )
            row[2].grid(row=i, column=2, sticky="news")

            row.append(
                self.settings.label(
                    self.imp_frame,
                    imp.glowcolor,
                    background=imp.glowcolor,
                    borderwidth=1,
                    relief="solid",
                )
            )
            row[3].grid(row=i, column=3, sticky="news")

            row.append(
                self.settings.label(
                    self.imp_frame,
                    imp.skincolor,
                    background=imp.skincolor,
                    borderwidth=1,
                    relief="solid",
                )
            )
            row[4].grid(row=i, column=4, sticky="news")

            row.append(
                self.settings.label(
                    self.imp_frame,
                    imp.dullcolor,
                    background=imp.dullcolor,
                    borderwidth=1,
                    relief="solid",
                )
            )
            row[5].grid(row=i, column=5, sticky="news")

            row.append(
                self.settings.button(
                    self.imp_frame,
                    "✎",
                    command=lambda target=imp.name: edit(target),
                    foreground=self.settings.get_style_primarytextcolor(),
                    background=self.settings.get_style_primarycolor(),
                    borderwidth=1,
                    relief="solid",
                    font=self.settings.get_style_headerfont(),
                )
            )
            row[6].grid(row=i, column=6, sticky="news")

            row.append(
                self.settings.button(
                    self.imp_frame,
                    "🗑",
                    command=lambda target=imp.name: delete(target),
                    foreground=self.settings.get_style_primarytextcolor(),
                    background=self.settings.get_style_primarycolor(),
                    borderwidth=1,
                    relief="solid",
                    font=self.settings.get_style_headerfont(),
                )
            )
            row[7].grid(row=i, column=7, sticky="news")

            self.grid_columns.append(row)
            i += 1

    def imp_grid_zone(self, frame):
        secondary_text_color = self.settings.get_style_secondarytextcolor()
        secondary_color = self.settings.get_style_secondarycolor()
        zone_columns = 4
        grid_columns = 8
        headerwidth = 10

        for i in range(zone_columns):
            frame.grid_columnconfigure(zone_columns, weight=1)
        #TODO: make this actually work!
        self.imp_frame = self.settings.scrollable_frame(
            frame,
            data=self.imps,
            height=100,
            row=0,
            column=0,
            columnspan=zone_columns,
            background=self.settings.get_style_inputcolor(),
        )

        for i in range(grid_columns):
            self.imp_frame.grid_columnconfigure(i, weight=1)

        label_header_name = self.settings.label(
            self.imp_frame,
            "Name",
            font=self.settings.get_style_headerfont(),
            background=secondary_color,
            foreground=secondary_text_color,
            borderwidth=1,
            relief="solid",
            width=headerwidth,
        )
        label_header_name.grid(row=0, column=0, sticky="ew")

        label_header_transform = self.settings.label(
            self.imp_frame,
            "Transform",
            font=self.settings.get_style_headerfont(),
            background=secondary_color,
            foreground=secondary_text_color,
            borderwidth=1,
            relief="solid",
            width=headerwidth,
        )
        label_header_transform.grid(row=0, column=1, sticky="ew")

        label_header_pronoun = self.settings.label(
            self.imp_frame,
            "Pronouns",
            font=self.settings.get_style_headerfont(),
            background=secondary_color,
            foreground=secondary_text_color,
            borderwidth=1,
            relief="solid",
            width=headerwidth,
        )
        label_header_pronoun.grid(row=0, column=2, sticky="ew")

        label_header_glowcolor = self.settings.label(
            self.imp_frame,
            "Glow Color",
            font=self.settings.get_style_headerfont(),
            background=secondary_color,
            foreground=secondary_text_color,
            borderwidth=1,
            relief="solid",
            width=headerwidth,
        )
        label_header_glowcolor.grid(row=0, column=3, sticky="ew")

        label_header_skincolor = self.settings.label(
            self.imp_frame,
            "Skin Color",
            font=self.settings.get_style_headerfont(),
            background=secondary_color,
            foreground=secondary_text_color,
            borderwidth=1,
            relief="solid",
            width=headerwidth,
        )
        label_header_skincolor.grid(row=0, column=4, sticky="ew")

        label_header_dullcolor = self.settings.label(
            self.imp_frame,
            "Dull Color",
            font=self.settings.get_style_headerfont(),
            background=secondary_color,
            foreground=secondary_text_color,
            borderwidth=1,
            relief="solid",
            width=headerwidth,
        )
        label_header_dullcolor.grid(row=0, column=5, sticky="ew")

        label_header_functions = self.settings.label(
            self.imp_frame,
            "",
            font=self.settings.get_style_headerfont(),
            background=secondary_color,
            foreground=secondary_text_color,
            borderwidth=1,
            relief="solid",
        )
        label_header_functions.grid(row=0, column=6, columnspan=2, sticky="ew")

        self.refreshgrid()
        self.imp_frame.grid(
            row=0,
            column=0,
            columnspan=zone_columns,
            sticky="ew",
            padx=self.padding,
            pady=self.padding,
        )

        self.button_import = self.settings.button(
            frame,
            "Import Imp from CSV",
            self.load_imps_from_fileprompt,
            background=secondary_color,
            foreground=secondary_text_color,
        )
        self.button_import.grid(
            row=1,
            column=0,
            sticky="ew",
            padx=self.padding,
            pady=self.padding,
        )

        self.button_save_grid_as = self.settings.button(
            frame,
            "Save As",
            self.save_imps_to_fileprompt,
            background=secondary_color,
            foreground=secondary_text_color,
        )
        self.button_save_grid_as.grid(
            row=1,
            column=zone_columns - 2,
            sticky="ew",
            padx=self.padding,
            pady=self.padding,
        )

        self.button_save_grid = self.settings.button(
            frame,
            "Save",
            self.save_imps_to_primaryfile,
            background=secondary_color,
            foreground=secondary_text_color,
        )
        self.button_save_grid.grid(
            row=1,
            column=zone_columns - 1,
            sticky="ew",
            padx=self.padding,
            pady=self.padding,
        )

    def imp_edit_zone(self, frame):
        self.name_var = tk.StringVar(frame, self.edit_imp.name)
        self.adj_var = tk.StringVar(frame, self.edit_imp.adjective)
        self.flavor_var = tk.StringVar(frame, self.edit_imp.flavor)
        self.noun_var = tk.StringVar(frame, self.edit_imp.noun)
        self.pronouns_var = tk.StringVar(frame, self.edit_imp.pronouns)
        self.glowcolor_var = tk.StringVar(frame, self.edit_imp.glowcolor)
        self.skincolor_var = tk.StringVar(frame, self.edit_imp.skincolor)
        self.dullcolor_var = tk.StringVar(frame, self.edit_imp.dullcolor)

        def randomize_button_press():
            self.load_vars_from_imp(self.generate_an_imp())

        def can_add2grid():
            if (
                len(self.name_var.get())
                * len(self.adj_var.get())
                * len(self.flavor_var.get())
                * len(self.noun_var.get())
                * len(self.pronouns_var.get())
                * len(self.glowcolor_var.get())
                * len(self.skincolor_var.get())
                * len(self.dullcolor_var.get())
                == 0
            ):
                return False
            return True

        def add2grid_button_press():
            if can_add2grid():
                self.turn_on_warning()
                self.imps[self.edit_imp.name] = Imp.create_imp_from_filestring(
                    self.edit_imp.filestring()
                )
                self.load_vars_from_imp(Imp.get_empi())
                update_selected_imp()
                self.refreshgrid()
                self.open_panel(Tags.grid_tag)

        def pick_glowcolor():
            color = colorchooser.askcolor(
                title="Choose Glow Color", color=self.glowcolor_var.get()
            )[1]
            if color is not None:
                self.glowcolor_var.set(color)
                update_selected_imp()

        def pick_skincolor():
            color = colorchooser.askcolor(
                title="Choose Skin Color", color=self.skincolor_var.get()
            )[1]
            if color is not None:
                self.skincolor_var.set(color)
                update_selected_imp()

        def pick_dullcolor():
            color = colorchooser.askcolor(
                title="Choose Dull Color", color=self.dullcolor_var.get()
            )[1]
            if color is not None:
                self.dullcolor_var.set(color)
                update_selected_imp()

        def update_selected_imp(*args):
            self.edit_imp.name = self.name_var.get()
            self.edit_imp.adjective = self.adj_var.get()
            self.edit_imp.flavor = self.flavor_var.get()
            self.edit_imp.noun = self.noun_var.get()
            self.edit_imp.pronouns = self.pronouns_var.get()
            self.edit_imp.set_glowcolor(self.glowcolor_var.get())
            self.edit_imp.set_skincolor(self.skincolor_var.get())
            self.edit_imp.set_dullcolor(self.dullcolor_var.get())
            button_glowcolor.configure({"background": self.edit_imp.glowcolor})
            button_glowcolor.configure({"text": self.edit_imp.glowcolor})
            button_skincolor.configure({"background": self.edit_imp.skincolor})
            button_skincolor.configure({"text": self.edit_imp.skincolor})
            button_dullcolor.configure({"background": self.edit_imp.dullcolor})
            button_dullcolor.configure({"text": self.edit_imp.dullcolor})

            if self.name_var.get() in self.imps.keys():
                button_add2grid["text"] = "Update Grid"
            else:
                button_add2grid["text"] = "Add to Grid"
            if can_add2grid():
                button_add2grid["state"] = "normal"
            else:
                button_add2grid["state"] = "disable"

        self.name_var.trace_add("write", update_selected_imp)
        self.adj_var.trace_add("write", update_selected_imp)
        self.flavor_var.trace_add("write", update_selected_imp)
        self.noun_var.trace_add("write", update_selected_imp)
        self.pronouns_var.trace_add("write", update_selected_imp)
        self.glowcolor_var.trace_add("write", update_selected_imp)
        self.skincolor_var.trace_add("write", update_selected_imp)
        self.dullcolor_var.trace_add("write", update_selected_imp)

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

        label_adj = self.settings.label(frame, text="Adjective")
        label_adj.grid(
            row=i,
            column=0,
            columnspan=2,
            sticky="ew",
            padx=self.padding,
            pady=self.padding,
        )
        label_flavor = self.settings.label(frame, text="Flavor")
        label_flavor.grid(
            row=i,
            column=2,
            columnspan=2,
            sticky="ew",
            padx=self.padding,
            pady=self.padding,
        )
        label_noun = self.settings.label(frame, text="Noun")
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

        label_glowcolor = self.settings.label(frame, text="Glow")
        label_skincolor = self.settings.label(frame, text="Skin")
        label_dullcolor = self.settings.label(frame, text="Dull")
        label_glowcolor.grid(
            row=i,
            column=0,
            columnspan=2,
            sticky="ew",
            padx=self.padding,
            pady=self.padding,
        )
        label_skincolor.grid(
            row=i,
            column=2,
            columnspan=2,
            sticky="ew",
            padx=self.padding,
            pady=self.padding,
        )
        label_dullcolor.grid(
            row=i,
            column=4,
            columnspan=2,
            sticky="ew",
            padx=self.padding,
            pady=self.padding,
        )
        i += 1

        button_glowcolor = self.settings.button(
            frame,
            text=self.glowcolor_var.get(),
            command=pick_glowcolor,
            background=self.glowcolor_var.get(),
        )
        button_skincolor = self.settings.button(
            frame,
            text=self.skincolor_var.get(),
            command=pick_skincolor,
            background=self.skincolor_var.get(),
        )
        button_dullcolor = self.settings.button(
            frame,
            text=self.dullcolor_var.get(),
            command=pick_dullcolor,
            background=self.dullcolor_var.get(),
        )
        button_glowcolor.grid(
            row=i,
            column=0,
            columnspan=2,
            sticky="we",
            padx=self.padding,
            pady=self.padding,
        )
        button_skincolor.grid(
            row=i,
            column=2,
            columnspan=2,
            sticky="we",
            padx=self.padding,
            pady=self.padding,
        )
        button_dullcolor.grid(
            row=i,
            column=4,
            columnspan=2,
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

        button_add2grid = self.settings.button(
            frame,
            text="Add to Grid",
            command=add2grid_button_press,
            background=self.settings.get_style_accentcolor(),
            state="disable",
        )
        button_add2grid.grid(
            row=i,
            column=4,
            columnspan=2,
            sticky="we",
            padx=self.padding,
            pady=self.padding,
        )
        i += 1

    def run_imp_gen_IU(self):

        app = tools.ImparianApp(
            "Imp Generator", self.settings, minwidth=700, close_warnings=[self]
        )
        app.title("Imp Generator")

        frame = app.add_frame(row=1)
        self.imp_management_zone(frame, tag=Tags.grid_tag)

        frame.mainloop()

    # endregion


if __name__ == "__main__":
    gen = ImpFactory()
    gen.run_imp_gen_IU()
