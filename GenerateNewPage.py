from glob import glob
from pathlib import Path
from tkinter import simpledialog
import shutil
import utilities.tools as tools
import re

class PageGenerator():
    def __init__(self, settings= None):
        if settings == None:
            settings = tools.Settings()
        self.settings = settings
        self.comic_dir = Path(self.settings.get_comic_dir())
        self.pages_dir = self.comic_dir / "Pages"


    def get_next_pagenumber(self):
        return (
            int(
                max(
                    list(
                        filter(
                            lambda x: x.isdecimal(),
                            list(
                                map(
                                    lambda x: x.split("\\")[-2].split(" ")[0],
                                    glob(f"{self.pages_dir}/*/"),
                                )
                            ),
                        )
                    )
                )
            )
            + 1
        )


    def is_title_valid(self, page_title):
        if page_title is None:
            return False
        if page_title.strip() == "":
            return False
        ILLEGAL_NTFS_CHARS = r"[<>:/\\|?*\"]|[\0-\31]"
        if re.search(ILLEGAL_NTFS_CHARS, page_title):
            return False
        if re.match(r"^[. ]|.*[. ]$", page_title):
            return False
        return True


    def generate_new_page(self,page_title):
        if self.is_title_valid(page_title):
            page_number = self.get_next_pagenumber()
            page_name = f"{page_number} {page_title.strip()}"
            page_path = self.pages_dir / page_name
            page_file_name = page_path / f"{page_name}.oci"
            page_template_path = self.comic_dir / "Resources/Templates/webstyle.oci"

            # Create and copy
            page_path.mkdir(exist_ok=True)
            shutil.copy(page_template_path, page_file_name)
            self.settings.print_debug(f"Created: {page_path}")
        else:
            self.settings.print_debug(f"{page_title} is not a valid Title.")


if __name__ == "__main__":
    page_title = simpledialog.askstring(title="Page Name?", prompt="Page Name?")
    PageGenerator().generate_new_page(page_title)
