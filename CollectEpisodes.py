import os
import shutil
from glob import glob
from PIL import Image
from optparse import OptionParser
import utilities.tools as tools

MODE_SLICE = "s"
MODE_TRANSFORM = "t"
MODE_SQUARE = "q"


class EpisodeCollector:

    def __init__(self):
        self.settings = tools.Settings()
        self.image_file_type = self.settings.getImageFormat()
        self.slice_half_folder_name = "Slice-Half"
        self.slice_Quarter_folder_name = "Slice-Quarter"
        self.transform_folder_name = "Transforms"
        self.uncensored_folder_name = "(U)"
        self.square_half_folder_name = "Square-Half"
        self.square_Quarter_folder_name = "Square-Quarter"
        self.comic_dir = self.settings.getComicDir()
        self.png_dir = f"{self.comic_dir}\\PNGs\\"
        self.pages_dir = f"{self.comic_dir}\\Pages\\"
        self.pages_files = [
            y
            for x in os.walk(self.pages_dir)
            for y in glob(os.path.join(x[0], "*{}".format(self.image_file_type)))
        ]
        self.remove_files = [
            y
            for x in os.walk(self.png_dir)
            for y in glob(os.path.join(x[0], "*{}".format(self.image_file_type)))
        ]
        self.transforms = tools.openfile(self.settings.getTransformSave())

    class coordinate:
        def __init__(self, left, top, right, bottom):
            self.left = left
            self.top = top
            self.right = right
            self.bottom = bottom

    def deleteExisting(self):
        for remove_path in self.remove_files:
            print("deleting:{}".format(remove_path.split("\\")[-1]))
            instahalf = (
                not remove_path.__contains__("\\" + self.square_half_folder_name + "\\")
                or options.insta
            )
            instaquarter = (
                not remove_path.__contains__(
                    "\\" + self.square_Quarter_folder_name + "\\"
                )
                or options.insta
            )
            slicehalf = (
                not remove_path.__contains__("\\" + self.slice_half_folder_name + "\\")
                or options.slice
            )
            slicequarter = (
                not remove_path.__contains__(
                    "\\" + self.slice_Quarter_folder_name + "\\"
                )
                or options.slice
            )
            transform = (
                not remove_path.__contains__("\\" + self.transform_folder_name + "\\")
                or options.transform
            )
            if instahalf and instaquarter and transform and slicehalf and slicequarter:
                os.remove(remove_path)

    def if_not_exist_make_folder(self, path):
        tools.if_not_exist_make_folder(f"{self.png_dir}\\{path}")

    def trim_headers(self, trim_image_Path):
        trim_image = Image.open(trim_image_Path)
        trim_image_width, trim_image_height = trim_image.size
        if trim_image_height > 4800:
            print("trimming:{}".format(trim_image_Path.split("\\")[-1]))
            left = 0
            top = 1200
            right = trim_image_width
            bottom = trim_image_height
            trimmed_image = trim_image.crop((left, top, right, bottom))
            trimmed_image.save(trim_image_Path)

    # copy over files
    def copy_stuff(self, files):
        self.if_not_exist_make_folder(self.uncensored_folder_name)
        for image_path in files:
            image_path_split = image_path.split("\\")
            image_dir = image_path_split[-2]
            image_name = image_path_split[-1]
            image_destination = "ERROR"
            self.trim_headers(image_path)
            if "{}{}".format(image_dir, self.image_file_type) == image_name:
                print("copying:{}".format(image_name))
                image_destination = os.path.join(self.png_dir, image_name)
            elif "{}(U){}".format(image_dir, self.image_file_type) == image_name:
                print("copying:{} (Uncensored)".format(image_name))
                image_destination = os.path.join(
                    self.png_dir, self.uncensored_folder_name, image_name
                )
            if image_destination != "ERROR":
                shutil.copy(image_path, image_destination)

    def Slice_Transform(self, files, folder):
        print("Slicing Transforms")
        self.if_not_exist_make_folder(folder)
        for image_path in files:
            image_path_split = image_path.split("\\")
            image_dir = image_path_split[-2]
            image_name = image_path_split[-1]
            image = Image.open(image_path)
            if "{}{}".format(image_dir, self.image_file_type) == image_name:
                x, height = image.size
                y = 2400
                for i in range(height // y):
                    name = f"{image_name[0:3]}P{i+1}"
                    file = os.path.join(self.png_dir, folder, f"{name}.png")
                    if name in self.transforms:
                        panel = image.crop((0, i * y, x, (i + 2) * y))
                        panel = panel.crop((0, 0, x, y))
                        print(f"Saving:{file}")
                        panel.save(file)

    def Slice(self, files, folder, square=False, quarter=False):
        print("Slicing Files")
        self.if_not_exist_make_folder(folder)
        for image_path in files:
            image_path_split = image_path.split("\\")
            image_dir = image_path_split[-2]
            image_name = image_path_split[-1]
            image = Image.open(image_path)
            if "{}{}".format(image_dir, self.image_file_type) == image_name:
                x, height = image.size
                if quarter:
                    y = 1200
                else:
                    y = 2400
                for i in range(height // y):
                    name = f"{image_name[0:3]}P{i+1}"
                    file = os.path.join(self.png_dir, folder, f"{name}.png")
                    panel = image.crop((0, i * y, x, (i + 2) * y))
                    if square and quarter:
                        panel = panel.crop((0, 0, x, y))
                        panel = panel.crop((0, -200, x, y + 200))
                    elif square:
                        panel = panel.crop((-400, 0, x + 400, 2400))
                    else:
                        panel = panel.crop((0, 0, x, y))
                    print(f"Saving:{file}")
                    panel.save(file)

    def CleanUp(self):
        for folder in glob(f"{self.png_dir}*\\"):
            if len(os.listdir(folder)) == 0:
                print(f"Removing Empty Directory: {folder.split('\\')[-2]}")
                os.rmdir(folder)

    def execute(self, Mode=""):
        self.copy_stuff(self.pages_files)
        if MODE_SLICE in Mode:
            self.Slice(self.pages_files, self.slice_Quarter_folder_name, quarter=True)
            self.Slice(self.pages_files, self.slice_half_folder_name)
        if MODE_TRANSFORM in Mode:
            self.Slice_Transform(self.pages_files, self.transform_folder_name)
        if MODE_SQUARE in Mode:
            self.Slice(self.pages_files, self.square_Quarter_folder_name, True, True)
            self.Slice(self.pages_files, self.square_half_folder_name, True)
        self.CleanUp()


if __name__ == "__main__":
    parser = OptionParser()
    parser.add_option("-s", "--slice", action="store_true", dest="s", default=False)
    parser.add_option("-t", "--transform", action="store_true", dest="t", default=False)
    parser.add_option("-q", "--square", action="store_true", dest="q", default=False)
    (options, args) = parser.parse_args()
    collector = EpisodeCollector()
    mode = ""
    if options.s:
        mode += MODE_SLICE
    if options.t:
        mode += MODE_TRANSFORM
    if options.q:
        mode += MODE_SQUARE
    collector.execute(mode)
