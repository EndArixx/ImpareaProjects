from tkinter.filedialog import askdirectory, askopenfile, askopenfilename
from tkinter import messagebox
from pathlib import Path




def openfile(str):
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
        self.loadSettings()

    def printDebug(self, str):
        if self.getSettingIsOn(Keys.DebugMode):
            print(f"{str}")

    def getSetting(self, key):
        if key in self.data:
            return self.data[key]
        else:
            return ""

    def getSettingIsOn(self, key):
        setting = self.getSetting(key)
        if setting.lower() == "yes":
            return True
        else:
            return False

    def setSetting(self, key: str, value: str):
        self.data[key] = value
        self.printDebug(f"Adding: {key} : {value}")
        self.saveSettings()

    def loadSettings(self):

        # Ensure file exists if not create a new one.
        if_not_exist_make_folder(self.settingLocation)
        if Path(self.settingsFile).is_file():
            i = 0
            for s in openfile(self.settingsFile):
                setting = s.strip().split(",")
                if len(setting) == 2:
                    self.data[setting[0]] = setting[1]
                i += 1

        # Prompt for missing or failing Settings

        if Keys.DebugMode not in self.data:
            response = messagebox.askquestion("DebugMode", "Would you like to turn on 'Debug Mode'?")
            self.setSetting(Keys.DebugMode, response)

        if Keys.ComicFolder not in self.data or not Path(self.getComicDir()).is_dir():
            url = askdirectory(title="Select Comic Root")
            if len(url) > 0:
                self.setSetting(Keys.ComicFolder, url)

        if Keys.ImpsSave not in self.data or not Path(self.getImpsSave()).is_file():
            url = askopenfilename(title='Select Imps File',filetypes=[("CSV files", "*.csv")])
            if url:
                self.setSetting(Keys.ImpsSave, url)

        if Keys.TransformsSave not in self.data or not Path(self.getTransformSave()).is_file():
            url = askopenfilename(title='Select Transforms File',filetypes=[("CSV files", "*.csv")])
            if url:
                self.setSetting(Keys.TransformsSave, url)

        if Keys.ImageExtention not in self.data:
            self.setSetting(Keys.ImageExtention, ".png")

        self.printDebug(f"Loaded: {self.settingsFile}\nSettings: {str(self.data)}")

    def saveSettings(self):
        with open(self.settingsFile, "w") as f:
            for k, v in self.data.items():
                if k and v:
                    self.printDebug(f"Writing: {k},{v}\n")
                    f.write(f"{k},{v}\n")

    def getComicDir(self):
        return self.getSetting(Keys.ComicFolder)

    def getImageFormat(self):
        return self.getSetting(Keys.ImageExtention)

    def getImpsSave(self):
        return self.getSetting(Keys.ImpsSave)
    
    def getTransformSave(self):
        return self.getSetting(Keys.TransformsSave)