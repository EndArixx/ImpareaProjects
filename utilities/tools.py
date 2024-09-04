from abc import ABC, abstractmethod
import random
import sys
import tkinter as tk
from tkinter import ttk
from tkinter.filedialog import askdirectory, askopenfilename
from tkinter import messagebox
from pathlib import Path

# region File Ops


def open_file(str):
    return open(str, "r").read().split("\n")


def append_file(text, path):
    with open(path, "a") as file:
        file.write(text)


def overwrite_file(text, path):
    with open(path, "w") as file:
        file.write(text)


def load_resource(path):
    if getattr(sys, "frozen", False):
        path = Path(sys._MEIPASS).joinpath(path)
    return open_file(path)


def if_not_exist_make_folder(path):
    full_path = Path(path)
    if not full_path.exists():
        full_path.mkdir()


# endregion


class Color:
    def __init__(self, color_str: str):
        if self.is_valid_hex_code(color_str):
            self.color = color_str
        else:
            self.color = "#000000"
            print(f"Invalid color: {color_str}")

    def is_valid_hex_code(self, color_str):
        if color_str[0] != "#":
            return False

        if not (len(color_str) == 4 or len(color_str) == 7):
            return False

        for i in range(1, len(color_str)):
            if not (
                (color_str[i] >= "0" and color_str[i] <= "9")
                or (color_str[i] >= "a" and color_str[i] <= "f")
                or (color_str[i] >= "A" or color_str[i] <= "F")
            ):
                return False

        return True

    def __str__(self):
        return self.color

    @classmethod
    def get_random_color(self):
        r = lambda: random.randint(0, 255)
        return Color("#%02X%02X%02X" % (r(), r(), r()))


class close_warning(ABC):
    @abstractmethod
    def fire_warning(self) -> bool:
        """Runs the nessisary checks then return continue check."""
        pass


class Keys:
    COMIC_FOLDER = "COMIC_FOLDER"
    DEBUG_MODE = "DEBUG_MODE"
    IMAGE_EXTENSION = "IMAGE_EXTENSION"
    IMPS_SAVE = "IMPS_SAVE"
    TRANSFORM_SAVE = "TRANSFORM_SAVE"
    PROGRAM_NAME = "PROGRAM_NAME"
    PRIMARY_TEXT_COLOR = "PRIMARY_TEXT_COLOR"
    PRIMARY_COLOR = "PRIMARY_COLOR"
    SECONDARY_TEXT_COLOR = "SECONDARY_TEXT_COLOR"
    SECONDARY_COLOR = "SECONDARY_COLOR"
    ACCENT_COLOR = "ACCENT_COLOR"
    INPUT_COLOR = "INPUT_COLOR"
    WARNING_COLOR = "WARNING_COLOR"
    WARNING_TEXT_COLOR = "WARNING_TEXT_COLOR"
    CLEAR_COLOR = "CLEAR_COLOR"
    HEADER_FONT = "HEADER_FONT"
    TEXT_FONT = "TEXT_FONT"
    PADDING = "PADDING"


class Settings(close_warning):
    def __init__(self):
        self.settingLocation = Path.home() / "AppData/Roaming/ImpProjects"
        self.settingsFile = self.settingLocation / "settings"
        self.data = {}
        self.load_settings()
        self.in_debug_Mode = self.get_setting_is_on(Keys.DEBUG_MODE)
        self.has_changes = False
        self.padding = self.get_style_padding()

    def print_debug(self, str):
        if self.get_setting_is_on(Keys.DEBUG_MODE):
            print(f"{str}")

    # region Settings controls

    def get_setting(self, key):
        if key in self.data:
            return self.data[key]
        else:
            return ""

    def get_setting_is_on(self, key):
        setting = self.get_setting(key)
        if setting.lower() == "yes":
            return True
        else:
            return False

    def set_setting(self, key: str, value: str):
        self.data[key] = value
        self.print_debug(f"Adding: {key} : {value}")
        self.save_settings()

    def save_settings(self):
        with open(self.settingsFile, "w") as f:
            for k, v in self.data.items():
                if k and v:
                    self.print_debug(f"Writing: {k},{v}\n")
                    f.write(f"{k},{v}\n")

    # endregion

    # region Load settings

    def load_settings(self):

        # Ensure file exists if not create a new one.
        if_not_exist_make_folder(self.settingLocation)
        if Path(self.settingsFile).is_file():
            i = 0
            for s in open_file(self.settingsFile):
                setting = s.strip().split(",")
                if len(setting) == 2:
                    self.data[setting[0]] = setting[1]
                i += 1

        # Prompt for missing or failing Settings

        if Keys.DEBUG_MODE not in self.data:
            response = messagebox.askquestion(
                "DebugMode", "Would you like to turn on 'Debug Mode'?"
            )
            self.set_setting(Keys.DEBUG_MODE, response)

        if (
            Keys.COMIC_FOLDER not in self.data
            or not Path(self.get_comic_dir()).is_dir()
        ):
            url = askdirectory(title="Select Comic Root")
            if len(url) > 0:
                self.set_setting(Keys.COMIC_FOLDER, url)

        if Keys.IMPS_SAVE not in self.data or not Path(self.get_imps_save()).is_file():
            url = askopenfilename(
                title="Select Imps File", filetypes=[("CSV files", "*.csv")]
            )
            if url:
                self.set_setting(Keys.IMPS_SAVE, url)

        if (
            Keys.TRANSFORM_SAVE not in self.data
            or not Path(self.get_transforms_save()).is_file()
        ):
            url = askopenfilename(
                title="Select Transforms File", filetypes=[("CSV files", "*.csv")]
            )
            if url:
                self.set_setting(Keys.TRANSFORM_SAVE, url)

        if Keys.IMAGE_EXTENSION not in self.data:
            self.set_setting(Keys.IMAGE_EXTENSION, ".png")

        if Keys.PROGRAM_NAME not in self.data:
            self.set_setting(Keys.PROGRAM_NAME, "Imparean Solutions")

        if Keys.PRIMARY_TEXT_COLOR not in self.data:
            self.set_setting(Keys.PRIMARY_TEXT_COLOR, "black")

        if Keys.PRIMARY_COLOR not in self.data:
            self.set_setting(Keys.PRIMARY_COLOR, "MediumSpringGreen")

        if Keys.SECONDARY_TEXT_COLOR not in self.data:
            self.set_setting(Keys.SECONDARY_TEXT_COLOR, "white")

        if Keys.SECONDARY_COLOR not in self.data:
            self.set_setting(Keys.SECONDARY_COLOR, "darkgreen")

        if Keys.ACCENT_COLOR not in self.data:
            self.set_setting(Keys.ACCENT_COLOR, "plum")

        if Keys.INPUT_COLOR not in self.data:
            self.set_setting(Keys.INPUT_COLOR, "aquamarine")

        if Keys.WARNING_COLOR not in self.data:
            self.set_setting(Keys.WARNING_COLOR, "crimson")

        if Keys.WARNING_TEXT_COLOR not in self.data:
            self.set_setting(Keys.WARNING_TEXT_COLOR, "white")

        if Keys.CLEAR_COLOR not in self.data:
            self.set_setting(Keys.CLEAR_COLOR, "snow")

        if Keys.HEADER_FONT not in self.data:
            self.set_setting(Keys.HEADER_FONT, "Helvetica 14 bold")

        if Keys.TEXT_FONT not in self.data:
            self.set_setting(Keys.TEXT_FONT, "Courier 12")

        if Keys.PADDING not in self.data:
            self.set_setting(Keys.PADDING, "5")

        self.print_debug(f"Loaded: {self.settingsFile}\nSettings: {str(self.data)}")

    # endregion

    # region Grid UI
    def fire_warning(self) -> bool:
        if self.has_changes:
            result = tk.messagebox.askyesno(
                title=f"Unsaved settings.",
                message=f"Are you sure you wish to close with unsaved changes?",
                icon="warning",
            )
            if not result:
                return False
        return True

    def open_settings(self):
        root = ImparianApp(
            "Settings",
            self,
            minwidth=600,
            close_warnings=[self],
        )

        grid = root.add_frame()

        self.setting_grid(grid)

        root.mainloop()

    def setting_grid(self, frame):
        labels = []
        textvariables = []
        entries = []

        def validate_data():
            # TODO add validation!
            altered = False
            for j in range(len(textvariables)):
                k = labels[j].cget("text")
                v = textvariables[j].get()
                if v != self.data[k]:
                    entries[j].configure({"background": self.get_style_accentcolor()})
                    altered = True
                else:
                    entries[j].configure({"background": self.get_style_inputcolor()})

            return altered

        def enable_save(*args):
            if validate_data():
                save_button["state"] = "normal"
                self.has_changes = True
            else:
                save_button["state"] = "disable"
                self.has_changes = False

        def save():
            result = tk.messagebox.askyesno(
                title="Save Settings",
                message=f"Are you sure you wish to Save Settings?",
            )
            if result:
                for j in range(len(textvariables)):
                    k = labels[j].cget("text")
                    v = textvariables[j].get()
                    if v != self.data[k]:
                        self.data[k] = v
                self.save_settings()
                validate_data()

        frame.grid_columnconfigure(0, weight=1)
        frame.grid_columnconfigure(1, weight=1)

        scrolling_frame = self.scrolling_frame(frame)

        i = 0
        for k, v in self.data.items():
            # TODO: Add support for different kinds of inputs:
            #   [] Yes/no
            #   [] File/folder location/name
            labels.append(
                self.label(
                    scrolling_frame.inner_frame,
                    k,
                    foreground=self.get_style_secondarytextcolor(),
                )
            )
            labels[i].grid(
                row=i, column=0, sticky="w", padx=self.padding, pady=self.padding
            )
            textvariables.append(tk.StringVar(scrolling_frame.inner_frame, v))
            textvariables[i].trace_add("write", enable_save)
            entries.append(
                self.entry(scrolling_frame.inner_frame, textvariables[i], width=32)
            )
            entries[i].grid(
                row=i, column=1, sticky="ew", padx=self.padding, pady=self.padding
            )
            i += 1

        scrolling_frame.outer_frame.grid(
            column=0,
            columnspan=2,
            row=1,
            sticky="news",
            padx=self.padding,
            pady=self.padding,
        )

        def reset():
            for j in range(len(textvariables)):
                textvariables[j].set(self.data[labels[j].cget("text")])

        reset_button = self.button(
            frame,
            text="Reset",
            command=reset,
            state="normal",
            background=self.get_style_accentcolor(),
        )
        reset_button.grid(
            column=0, row=2, sticky="e", padx=self.padding, pady=self.padding
        )

        save_button = self.button(
            frame,
            text="Save Settings",
            command=save,
            state="disable",
            background=self.get_style_accentcolor(),
        )
        save_button.grid(
            column=1, row=2, sticky="w", padx=self.padding, pady=self.padding
        )

    # endregion

    # region Widget Overrides

    def scrolling_frame(
        self,
        root,
        outer_background=None,
        inner_background=None,
        *args,
        **kwargs,
    ):

        class ScrollingFrame:
            def __init__(
                self, outer_frame: self.frame, inner_frame: self.frame
            ) -> None:
                self.outer_frame = outer_frame
                self.inner_frame = inner_frame

        outer_frame = self.frame(
            root,
            background=outer_background,
        )
        outer_frame.rowconfigure(0, weight=0)
        outer_frame.rowconfigure(1, weight=1)
        outer_frame.columnconfigure(0, weight=1)
        outer_frame.columnconfigure(1, weight=0)

        # Create a canvas inside the frame
        canvas = self.canvas(outer_frame)
        canvas.grid(row=1, column=0, sticky="news")

        # add a horizantal scrollbar to the frame
        scrollbar = ttk.Scrollbar(outer_frame, orient="horizontal", command=canvas.xview)
        scrollbar.grid(row=0, column=0, columnspan=2, sticky="ew")

        # Add a vertical scrollbar to the frame
        scrollbar = ttk.Scrollbar(outer_frame, orient="vertical", command=canvas.yview)
        scrollbar.grid(row=1, column=1, sticky="ns")

        # Configure canvas to work with scrollbar
        canvas.configure(yscrollcommand=scrollbar.set)

        # Add another frame inside the canvas for the actual content
        inner_frame = self.frame(canvas, background=inner_background)
        canvas.create_window((0, 0), window=inner_frame, anchor="nw")

        # Ensure scrolling works
        inner_frame.bind(
            "<Configure>",
            lambda event: canvas.configure(scrollregion=canvas.bbox("all")),
        )

        return ScrollingFrame(outer_frame, inner_frame)

    def frame(
        self,
        root,
        background=None,
        *args,
        **kwargs,
    ):
        if background is None:
            background = root["background"]
        return tk.Frame(root, background=background, *args, **kwargs)

    def canvas(
        self,
        root,
        background=None,
        *args,
        **kwargs,
    ):
        if background is None:
            background = root["background"]
        return tk.Canvas(
            root,
            background=background,
            highlightthickness=0,
            *args,
            **kwargs,
        )

    def button(
        self,
        root,
        text,
        command,
        foreground=None,
        background=None,
        font=None,
        *args,
        **kwargs,
    ):
        if foreground is None:
            foreground = self.get_style_primarytextcolor()
        if background is None:
            background = self.get_style_primarycolor()
        if font is None:
            font = self.get_style_textfont()
        return tk.Button(
            root,
            text=text,
            command=command,
            foreground=foreground,
            background=background,
            font=font,
            *args,
            **kwargs,
        )

    def label(
        self,
        root,
        text,
        foreground=None,
        background=None,
        font=None,
        *args,
        **kwargs,
    ):
        if foreground is None:
            foreground = self.get_style_primarytextcolor()
        if background is None:
            background = root["background"]
        if font is None:
            font = self.get_style_textfont()
        return tk.Label(
            root,
            text=text,
            foreground=foreground,
            background=background,
            font=font,
            *args,
            **kwargs,
        )

    def entry(
        self,
        root,
        textvariable,
        foreground=None,
        background=None,
        font=None,
        text="",
        *args,
        **kwargs,
    ):
        if foreground is None:
            foreground = self.get_style_primarytextcolor()
        if background is None:
            background = self.get_style_inputcolor()
        if font is None:
            font = self.get_style_textfont()
        return tk.Entry(
            root,
            text=text,
            textvariable=textvariable,
            foreground=foreground,
            background=background,
            font=font,
            *args,
            **kwargs,
        )

    def text(
        self,
        root,
        width,
        height,
        textvariable,
        foreground=None,
        background=None,
        font=None,
        *args,
        **kwargs,
    ):
        if foreground is None:
            foreground = self.get_style_primarytextcolor()
        if background is None:
            background = self.get_style_inputcolor()
        if font is None:
            font = self.get_style_textfont()
        return tk.Text(
            root,
            height=height,
            width=width,
            textvariable=textvariable,
            foreground=foreground,
            background=background,
            font=font,
            *args,
            **kwargs,
        )

    # endregion

    # region Specific gets

    def get_comic_dir(self):
        return self.get_setting(Keys.COMIC_FOLDER)

    def get_image_format(self):
        return self.get_setting(Keys.IMAGE_EXTENSION)

    def get_imps_save(self):
        return self.get_setting(Keys.IMPS_SAVE)

    def get_transforms_save(self):
        return self.get_setting(Keys.TRANSFORM_SAVE)

    def get_program_name(self):
        return self.get_setting(Keys.PROGRAM_NAME)

    def get_style_primarytextcolor(self):
        return self.get_setting(Keys.PRIMARY_TEXT_COLOR)

    def get_style_primarycolor(self):
        return self.get_setting(Keys.PRIMARY_COLOR)

    def get_style_secondarytextcolor(self):
        return self.get_setting(Keys.SECONDARY_TEXT_COLOR)

    def get_style_secondarycolor(self):
        return self.get_setting(Keys.SECONDARY_COLOR)

    def get_style_inputcolor(self):
        return self.get_setting(Keys.INPUT_COLOR)

    def get_style_accentcolor(self):
        return self.get_setting(Keys.ACCENT_COLOR)

    def get_style_warningcolor(self):
        return self.get_setting(Keys.WARNING_COLOR)

    def get_style_warningtextcolor(self):
        return self.get_setting(Keys.WARNING_TEXT_COLOR)

    def get_style_clearcolor(self):
        return self.get_setting(Keys.CLEAR_COLOR)

    def get_style_headerfont(self):
        return self.get_setting(Keys.HEADER_FONT)

    def get_style_textfont(self):
        return self.get_setting(Keys.TEXT_FONT)

    def get_style_padding(self):
        return self.get_setting(Keys.PADDING)

    # endregion


# region Imparian Base App
class ImparianApp(tk.Tk):
    def __init__(
        self,
        title: str,
        settings: Settings = None,
        has_settings_edit=False,
        close_warnings: list[close_warning] = [],
        minwidth=0,
        minheight=0,
    ):
        super().__init__()
        self.next_row = 0
        if settings == None:
            settings = Settings()
        self.settings = settings
        self.wm_attributes("-transparentcolor", settings.get_style_clearcolor())
        self.title("Imparea Comic Utilities")
        self.configure(background=settings.get_style_clearcolor())
        self.minsize(minwidth, minheight)
        self.overrideredirect(1)
        self.attributes("-topmost", True)
        self.grid_columnconfigure(0, weight=1)
        self.close_warnings = close_warnings

        # TODO: Add logic to ovveride the default fonts with the settings fonts.
        # self.defaultFont = font.nametofont("TkDefaultFont")
        # self.defaultFont.configure(family="Segoe Script",
        #                            size=19,
        #                            weight=font.BOLD)

        m_frame = self.add_frame(background=settings.get_style_primarytextcolor())
        self.top_menu(m_frame, title, has_settings_edit)

    def startMove(self, event):
        self.x = event.x
        self.y = event.y

    def stopMove(self, event):
        self.x = None
        self.y = None

    def moving(self, event):
        x = event.x_root - self.x
        y = event.y_root - self.y
        self.geometry("+%s+%s" % (x, y))

    def exit(self):
        for x in self.close_warnings:
            if not x.fire_warning():
                return
        self.destroy()

    def top_menu(self, frame, title, has_settings_edit):
        frame.bind("<Button-1>", self.startMove)
        frame.bind("<ButtonRelease-1>", self.stopMove)
        frame.bind("<B1-Motion>", self.moving)

        frame.grid_columnconfigure(0, weight=1)
        frame.grid_columnconfigure(1, weight=0)
        frame.grid_columnconfigure(2, weight=0)

        label = tk.Label(
            frame,
            text=title,
            foreground=self.settings.get_style_primarycolor(),
            background=self.settings.get_style_primarytextcolor(),
            font=self.settings.get_style_headerfont(),
        )
        label.bind("<Button-1>", self.startMove)
        label.bind("<ButtonRelease-1>", self.stopMove)
        label.bind("<B1-Motion>", self.moving)
        label.grid(column=0, row=0, columnspan=2, sticky="ew")
        if has_settings_edit:
            # TODO: Fix bug that is causing scrollbar to not be formatted when this is use.
            setting_button = tk.Button(
                frame,
                text="⚙",
                command=self.settings.open_settings,
                background=self.settings.get_style_primarytextcolor(),
                foreground=self.settings.get_style_primarycolor(),
                font=self.settings.get_style_headerfont(),
            )
            setting_button.grid(row=0, column=1, sticky="e")

        exit_button = tk.Button(
            frame,
            text="✕",
            command=self.exit,
            background=self.settings.get_style_primarytextcolor(),
            foreground=self.settings.get_style_primarycolor(),
            font=self.settings.get_style_headerfont(),
        )
        exit_button.grid(row=0, column=2, sticky="e")

    def add_frame(
        self, row=-1, column=0, sticky="news", background=None, *args, **kwargs
    ):
        if background is None:
            background = self.settings.get_style_primarycolor()
        if row < 0:
            row = self.next_row
            self.next_row += 1
        frame = self.settings.frame(
            self,
            background=background,
            *args,
            **kwargs,
        )
        frame.grid(row=row, column=column, sticky=sticky)
        return frame


# endregion

if __name__ == "__main__":
    settings = Settings()
    settings.open_settings()
