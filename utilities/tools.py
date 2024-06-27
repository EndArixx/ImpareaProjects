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
    ComicFolder = "ComicFolderPath"
    DebugMode = "DebugMode"
    ImageExtention = "ImageExtention"
    ImpsSave = "ImpsSave"
    TransformsSave = "TransformsSave"


class Settings:
    def __init__(self):
        self.settingLocation = Path.home() / "AppData/Roaming/ImpProjects"
        self.settingsFile = self.settingLocation / "settings"
        self.data = {}
        self.load_settings()
        self.in_debug_Mode = self.get_setting_is_on(Keys.DebugMode)

    def print_debug(self, str):
        if self.get_setting_is_on(Keys.DebugMode):
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

        if Keys.DebugMode not in self.data:
            response = messagebox.askquestion(
                "DebugMode", "Would you like to turn on 'Debug Mode'?"
            )
            self.set_setting(Keys.DebugMode, response)

        if Keys.ComicFolder not in self.data or not Path(self.get_comic_dir()).is_dir():
            url = askdirectory(title="Select Comic Root")
            if len(url) > 0:
                self.set_setting(Keys.ComicFolder, url)

        if Keys.ImpsSave not in self.data or not Path(self.get_imps_save()).is_file():
            url = askopenfilename(
                title="Select Imps File", filetypes=[("CSV files", "*.csv")]
            )
            if url:
                self.set_setting(Keys.ImpsSave, url)

        if (
            Keys.TransformsSave not in self.data
            or not Path(self.get_transforms_save()).is_file()
        ):
            url = askopenfilename(
                title="Select Transforms File", filetypes=[("CSV files", "*.csv")]
            )
            if url:
                self.set_setting(Keys.TransformsSave, url)

        if Keys.ImageExtention not in self.data:
            self.set_setting(Keys.ImageExtention, ".png")

        self.print_debug(f"Loaded: {self.settingsFile}\nSettings: {str(self.data)}")

    def save_settings(self):
        with open(self.settingsFile, "w") as f:
            for k, v in self.data.items():
                if k and v:
                    self.print_debug(f"Writing: {k},{v}\n")
                    f.write(f"{k},{v}\n")

    #TODO 
    # def edit_settings(self): 

    def get_comic_dir(self):
        return self.get_setting(Keys.ComicFolder)

    def get_image_format(self):
        return self.get_setting(Keys.ImageExtention)

    def get_imps_save(self):
        return self.get_setting(Keys.ImpsSave)

    def get_transforms_save(self):
        return self.get_setting(Keys.TransformsSave)
