from glob import glob
from pathlib import Path
import tkinter as tk
from tkinter import simpledialog
import shutil
import tools


def GenerateNewPage():
    settings = tools.Settings()

    page_title = simpledialog.askstring(title="Page Name?", prompt="Page Name?")
    if page_title is not None and len(page_title.strip()) > 0:
        comic_dir = Path(settings.getComicDir())
        pages_dir = comic_dir / "Pages"
        # sorry
        page_number = (
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
        page_name = f"{page_number} {page_title.strip()}"
        page_path = pages_dir / page_name
        page_file_name = page_path / f"{page_name}.oci"
        page_template_path = comic_dir / "Resources/Templates/webstyle.oci"

        # Create and copy
        page_path.mkdir(exist_ok=True)
        shutil.copy(page_template_path, page_file_name)
        settings.printDebug(f"Created: {page_path}")


if __name__ == "__main__":
    GenerateNewPage()
