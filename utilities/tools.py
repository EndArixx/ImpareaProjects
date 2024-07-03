import tkinter as tk
from tkinter import font
from tkinter.filedialog import askdirectory, askopenfilename
from tkinter import messagebox
from pathlib import Path


def open_file(str):
    return open(str, "r").read().split("\n")


def if_not_exist_make_folder(path):
    full_path = Path(path)
    if not full_path.exists():
        full_path.mkdir()


class Keys:
    COMIC_FOLDER = "COMIC_FOLDER"
    DEBUG_MODE = "DEBUG_MODE"
    IMAGE_EXTENSION = "IMAGE_EXTENSION"
    IMPS_SAVE = "IMPS_SAVE"
    TRANSFORM_SAVE = "TRANSFORM_SAVE"
    PROGRAM_NAME = "PROGRAM_NAME"
    PRIMARY_TEXT_COLOR = "PRIMARY_TEXT_COLOR"
    PRIMARY_COLOR = "PRIMARY_COLOR"
    INPUT_COLOR = "INPUT_COLOR"
    ACCENT_COLOR = "ACCENT_COLOR"
    WARNING_COLOR = "WARNING_COLOR"
    WARNING_TEXT_COLOR = "WARNING_TEXT_COLOR"
    CLEAR_COLOR = "CLEAR_COLOR"
    HEADER_FONT = "HEADER_FONT"
    TEXT_FONT = "TEXT_FONT"
    PADDING = "PADDING"


class Settings:
    def __init__(self):
        self.settingLocation = Path.home() / "AppData/Roaming/ImpProjects"
        self.settingsFile = self.settingLocation / "settings"
        self.data = {}
        self.load_settings()
        self.in_debug_Mode = self.get_setting_is_on(Keys.DEBUG_MODE)

    def print_debug(self, str):
        if self.get_setting_is_on(Keys.DEBUG_MODE):
            print(f"{str}")

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

        if Keys.COMIC_FOLDER not in self.data or not Path(self.get_comic_dir()).is_dir():
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

        if Keys.INPUT_COLOR not in self.data:
            self.set_setting(Keys.INPUT_COLOR, "white")

        if Keys.ACCENT_COLOR not in self.data:
            self.set_setting(Keys.ACCENT_COLOR, "plum")

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

    def save_settings(self):
        with open(self.settingsFile, "w") as f:
            for k, v in self.data.items():
                if k and v:
                    self.print_debug(f"Writing: {k},{v}\n")
                    f.write(f"{k},{v}\n")

    def edit_settings(self):
        root = ImparianApp("Settings", self)
        root.mainloop()

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

    def get_style_primaytextcolor(self):
        return self.get_setting(Keys.PRIMARY_TEXT_COLOR)

    def get_style_primarycolor(self):
        return self.get_setting(Keys.PRIMARY_COLOR)

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
    def __init__(self, title: str, settings=None):
        super().__init__()
        self.next_row = 0
        if settings == None:
            settings = Settings()
        self.settings = settings
        self.wm_attributes("-transparentcolor", settings.get_style_clearcolor())
        self.title("Imparea Comic Utilities")
        self.configure(background=settings.get_style_clearcolor())
        self.minsize(600, 0)
        self.overrideredirect(1)
        self.attributes("-topmost", True)
        self.grid_columnconfigure(0, weight=1)

        #TODO: Add logic to ovveride the default fonts with the settings fonts.
        # self.defaultFont = font.nametofont("TkDefaultFont") 
        # self.defaultFont.configure(family="Segoe Script", 
        #                            size=19, 
        #                            weight=font.BOLD)

        #TODO: overide buttons, labels, inputs... etc so you can apply colors.

        m_frame = self.add_frame(color=settings.get_style_primaytextcolor())
        self.top_menu(m_frame, title)

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
        self.destroy()

    def top_menu(self, frame, title):
        frame.bind("<Button-1>", self.startMove)
        frame.bind("<ButtonRelease-1>", self.stopMove)
        frame.bind("<B1-Motion>", self.moving)

        frame.grid_columnconfigure(0, weight=1)
        frame.grid_columnconfigure(1, weight=0)

        label = tk.Label(
            frame,
            text=title,
            foreground=self.settings.get_style_primarycolor(),
            background=self.settings.get_style_primaytextcolor(),
            font=self.settings.get_style_headerfont(),
        )
        label.bind("<Button-1>", self.startMove)
        label.bind("<ButtonRelease-1>", self.stopMove)
        label.bind("<B1-Motion>", self.moving)
        label.grid(column=0, row=0, columnspan=2, sticky="ew")

        exit_button = tk.Button(
            frame,
            text="✕",
            command=self.destroy,
            background=self.settings.get_style_primaytextcolor(),
            foreground=self.settings.get_style_primarycolor(),
            font=self.settings.get_style_headerfont(),
        )
        exit_button.grid(row=0, column=1, sticky="e")

    def add_frame(self, row=-1, column=0, sticky="new", color="White"):
        if row < 0:
            row = self.next_row
            self.next_row += 1
        frame = tk.Frame(self, background=color)
        frame.grid(column=column, row=row, sticky=sticky)
        return frame


# endregion

if __name__ == "__main__":
    settings = Settings()
    settings.edit_settings()
