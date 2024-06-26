from glob import glob
from pathlib import Path
import tkinter as tk
from tkinter import simpledialog
import shutil
import utilities.tools as tools
import re

settings = tools.Settings()
comic_dir = Path(settings.getComicDir())
pages_dir = comic_dir / "Pages"


def get_next_pagenumber():
    return (
        int(
            max(
                list(
                    filter(
                        lambda x: x.isdecimal(),
                        list(
                            map(
                                lambda x: x.split("\\")[-2].split(" ")[0],
                                glob(f"{pages_dir}/*/"),
                            )
                        ),
                    )
                )
            )
        )
        + 1
    )


def is_title_valid(page_title):
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


def generate_new_page(page_title):
    if is_title_valid(page_title):
        page_number = get_next_pagenumber()
        page_name = f"{page_number} {page_title.strip()}"
        page_path = pages_dir / page_name
        page_file_name = page_path / f"{page_name}.oci"
        page_template_path = comic_dir / "Resources/Templates/webstyle.oci"

        # Create and copy
        page_path.mkdir(exist_ok=True)
        shutil.copy(page_template_path, page_file_name)
        print(f"Created: {page_path}")
    else:
        print(f"{page_title} is not a valid Title.")


if __name__ == "__main__":
    page_title = simpledialog.askstring(title="Page Name?", prompt="Page Name?")
    generate_new_page(page_title)
