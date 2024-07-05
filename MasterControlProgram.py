import sys
import tkinter as tk
import PyInstaller.__main__
from CollectEpisodes import *
from GenerateNewPage import *
import threading


VERSION = "v0.2.3"
settings = tools.Settings()
# Load Styles
PROGRAM_NAME = settings.get_program_name()
PRIMARY_TEXT_COLOR = settings.get_style_primarytextcolor()
PRIMARY_COLOR = settings.get_style_primarycolor()
INPUT_COLOR = settings.get_style_inputcolor()
ACCENT_COLOR = settings.get_style_accentcolor()
WARNING_COLOR = settings.get_style_warningcolor()
WARNING_TEXT_COLOR = settings.get_style_warningtextcolor()
CLEAR_COLOR = settings.get_style_clearcolor()
HEADER_FONT = settings.get_style_headerfont()
TEXT_FONT = settings.get_style_textfont()
PADDING = settings.get_style_padding()


def generate_page_zone(frame):
    pagetitle_var = tk.StringVar(frame, "")
    gnp = PageGenerator(settings)

    def gen():
        title = pagetitle_var.get()

        if gnp.is_title_valid(title):
            result = tk.messagebox.askyesno(
                title="Create New Page",
                message=f"Are you sure you wish to generate\n'{gnp.get_next_pagenumber()} {pagetitle_var.get()}'",
            )
            if result:
                gnp.generate_new_page(title)
                pagetitle_var.set("")

        else:
            tk.messagebox.showerror(
                title="Error", message=f"'{title}' is not a valid title."
            )

    def enable_gen(*args):
        if pagetitle_var.get():
            generatepage_button["state"] = "normal"
        else:
            generatepage_button["state"] = "disable"

    pagetitle_var.trace_add("write", enable_gen)

    frame.grid_columnconfigure(0, weight=0)
    frame.grid_columnconfigure(1, weight=1)

    zone_label = settings.label(
        frame,
        text="Generate New Page",
    )
    zone_label.grid(
        column=0, row=0, columnspan=3, sticky="we", padx=PADDING, pady=PADDING
    )

    pagetitle_label = settings.label(
        frame,
        text="Page Title:",
    )
    pagetitle_label.grid(column=0, row=1, sticky="w", padx=PADDING, pady=PADDING)

    pagetitle_entry = settings.entry(
        frame,
        textvariable=pagetitle_var,
    )
    pagetitle_entry.grid(column=1, row=1, sticky="we", padx=PADDING, pady=PADDING)

    generatepage_button = settings.button(
        frame,
        text="Generate new Page",
        command=gen,
        state="disable",
        background=ACCENT_COLOR,
    )
    generatepage_button.grid(column=2, row=1, sticky="e", padx=PADDING, pady=PADDING)


def collect_episodes_zone(frame):
    episode_collector = EpisodeCollector(settings)
    for i in range(2):
        frame.grid_columnconfigure(i, weight=1)
        frame.grid_rowconfigure(i, weight=1)

    def collect(mode, message):
        def execute_collection(mode):
            episode_collector.execute(mode)
            tk.messagebox.showinfo(title="Complete", message=message)
            enable_all()

        disable_all()
        thread = threading.Thread(target=execute_collection, args=(mode,))
        thread.start()

    def collect_episodes():
        collect("", "Episodes Collected")

    def slice_episodes():
        collect(MODE_SLICE, "Episodes Sliced")

    def square_episodes():
        collect(MODE_SQUARE, "Episodes Squared")

    def collect_transforms():
        collect(MODE_TRANSFORM, "Transforms Collected")

    def disable_all():
        warning_label.grid()
        collect_button["state"] = "disable"
        slice_button["state"] = "disable"
        square_button["state"] = "disable"
        transforms_button["state"] = "disable"

    def enable_all():
        warning_label.grid_remove()
        collect_button["state"] = "normal"
        slice_button["state"] = "normal"
        square_button["state"] = "normal"
        transforms_button["state"] = "normal"

    collect_button = settings.button(
        frame,
        text="Collect Episodes",
        command=collect_episodes,
    )
    collect_button.grid(row=0, column=0, padx=PADDING, pady=PADDING, sticky="we")

    transforms_button = settings.button(
        frame,
        text="Collect Transform",
        command=collect_transforms,
    )
    transforms_button.grid(row=0, column=1, padx=PADDING, pady=PADDING, sticky="we")

    slice_button = settings.button(
        frame,
        text="Slice Episodes",
        command=slice_episodes,
    )
    slice_button.grid(row=1, column=0, padx=PADDING, pady=PADDING, sticky="we")

    square_button = settings.button(
        frame,
        text="Square Episodes",
        command=square_episodes,
    )
    square_button.grid(row=1, column=1, padx=PADDING, pady=PADDING, sticky="we")

    warning_label = settings.label(
        frame,
        text="Executing Collection",
        foreground=WARNING_TEXT_COLOR,
        background=WARNING_COLOR,
        font=HEADER_FONT,
    )
    warning_label.grid(row=0, column=0, rowspan=2, columnspan=2, sticky="ew")
    warning_label.grid_remove()


def file_zone(frame):
    frame.grid_rowconfigure(0, weight=0)
    frame.grid_columnconfigure(0, weight=0)
    frame.grid_columnconfigure(1, weight=0)
    frame.grid_columnconfigure(2, weight=1)

    def disable_all():
        warning_label.grid()
        open_comic_button["state"] = "disable"
        create_exe_button["state"] = "disable"

    def enable_all():
        warning_label.grid_remove()
        open_comic_button["state"] = "normal"
        create_exe_button["state"] = "normal"

    def open_comic_folder():
        print(settings.get_comic_dir())
        os.startfile(settings.get_comic_dir())

    def create_exe():
        def run_thread():
            PyInstaller.__main__.run(
                [
                    "MasterControlProgram.py",
                    "--onefile",
                    "--icon=data/mcp.ico",
                    f"--name={PROGRAM_NAME}",
                ]
            )
            tk.messagebox.showinfo(title="Complete", message="Executable Created")
            enable_all()

        disable_all()
        thread = threading.Thread(target=run_thread, args=())
        thread.start()

    open_comic_button = settings.button(
        frame,
        text="Open Comic Folder",
        command=open_comic_folder,
    )
    open_comic_button.grid(row=0, column=0, sticky="w", padx=PADDING, pady=PADDING)

    create_exe_button = settings.button(
        frame,
        text="Create Executable",
        command=create_exe,
    )
    create_exe_button.grid(row=0, column=1, sticky="w", padx=PADDING, pady=PADDING)
    if not settings.in_debug_Mode or "\\python.exe" not in sys.executable:
        create_exe_button.grid_remove()

    warning_label = settings.label(
        frame,
        text="Creating Executable",
        foreground=WARNING_TEXT_COLOR,
        background=WARNING_COLOR,
        font=HEADER_FONT,
    )
    warning_label.grid(row=0, column=0, columnspan=3, sticky="ew")
    warning_label.grid_remove()


def execute_primary_function():
    # Create the main window
    root = tools.ImparianApp(f"{settings.get_program_name()} - {VERSION}", settings, True)

    # Generate New Page
    gnp_frame = root.add_frame(color=CLEAR_COLOR)
    generate_page_zone(gnp_frame)

    # Collect Episodes
    ce_frame = root.add_frame(color=CLEAR_COLOR)
    collect_episodes_zone(ce_frame)

    # File zone
    fz_frame = root.add_frame(color=CLEAR_COLOR)
    file_zone(fz_frame)

    # execute the GUI
    root.mainloop()


if __name__ == "__main__":
    execute_primary_function()
