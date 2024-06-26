import sys
import tkinter as tk
import PyInstaller.__main__
from CollectEpisodes import *
import GenerateNewPage as gnp
import threading


VERSION = "v0.1.2"
PROGRAM_NAME = "Imparean Solutions"
PRIMARY_TEXT_COLOR = "black"
PRIMARY_COLOR = "MediumSpringGreen"
INPUT_COLOR = "white"
ACCENT_COLOR = "plum"
WARNING_COLOR = "crimson"
WARNING_TEXT_COLOR = "white"
CLEAR_COLOR = "snow"
HEADER_FONT = "Handlee 14 bold"
TEXT_FONT = "Courier 12"
PADDING = 5
settings = tools.Settings()


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.wm_attributes("-transparentcolor", CLEAR_COLOR)
        self.title("Imparea Comic Utilities")
        self.configure(background=CLEAR_COLOR)
        self.minsize(600, 0)
        self.overrideredirect(1)
        self.attributes("-topmost", True)
        self.grid_columnconfigure(0, weight=1)

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


def menu_zone(frame, root):
    frame.bind("<Button-1>", root.startMove)
    frame.bind("<ButtonRelease-1>", root.stopMove)
    frame.bind("<B1-Motion>", root.moving)

    frame.grid_columnconfigure(0, weight=1)
    frame.grid_columnconfigure(1, weight=0)

    label = tk.Label(
        frame,
        text=f"{PROGRAM_NAME} - {VERSION}",
        foreground=PRIMARY_COLOR,
        background=PRIMARY_TEXT_COLOR,
        font=HEADER_FONT,
    )
    label.bind("<Button-1>", root.startMove)
    label.bind("<ButtonRelease-1>", root.stopMove)
    label.bind("<B1-Motion>", root.moving)
    label.grid(column=0, row=0, columnspan=2, sticky="ew")

    exit_button = tk.Button(
        frame,
        text="✕",
        command=root.destroy,
        background=PRIMARY_TEXT_COLOR,
        foreground=PRIMARY_COLOR,
        font=HEADER_FONT,
    )
    exit_button.grid(row=0, column=1, sticky="e")


def generate_page_zone(frame):
    pagetitle_var = tk.StringVar(frame, "")

    def gen():
        title = pagetitle_var.get()

        if gnp.is_title_valid(title):
            result = tk.messagebox.askyesno(
                title="Create New Page",
                message=f"Are you sure you wish to generate\n'{gnp.get_next_pagenumber()} {pagetitle_var.get()}'",
            )
            if result:
                gnp.generate_new_page(pagetitle_var.get())
                pagetitle_var.set("")

        else:
            tk.messagebox.showerror(
                title="Error", message=f"'{title}' is not a valid title."
            )

    def enable_gen(var, index, mode):
        if pagetitle_var.get():
            generatepage_button["state"] = "normal"
        else:
            generatepage_button["state"] = "disable"

    pagetitle_var.trace_add("write", enable_gen)

    frame.grid_columnconfigure(0, weight=0)
    frame.grid_columnconfigure(1, weight=1)

    zone_label = tk.Label(
        frame,
        text="Generate New Page",
        foreground=PRIMARY_TEXT_COLOR,
        background=PRIMARY_COLOR,
        font=TEXT_FONT,
    )
    zone_label.grid(
        column=0, row=0, columnspan=3, sticky="we", padx=PADDING, pady=PADDING
    )

    pagetitle_label = tk.Label(
        frame,
        text="Page Title:",
        foreground=PRIMARY_TEXT_COLOR,
        background=PRIMARY_COLOR,
        font=TEXT_FONT,
    )
    pagetitle_label.grid(column=0, row=1, sticky="w", padx=PADDING, pady=PADDING)

    pagetitle_entry = tk.Entry(
        frame,
        foreground=PRIMARY_TEXT_COLOR,
        background=INPUT_COLOR,
        font=TEXT_FONT,
        textvariable=pagetitle_var,
    )
    pagetitle_entry.grid(column=1, row=1, sticky="we", padx=PADDING, pady=PADDING)

    generatepage_button = tk.Button(
        frame,
        text="Generate new Page",
        command=gen,
        state="disable",
        background=ACCENT_COLOR,
        foreground=PRIMARY_TEXT_COLOR,
        font=TEXT_FONT,
    )
    generatepage_button.grid(column=2, row=1, sticky="e", padx=PADDING, pady=PADDING)


def collect_episodes_zone(frame):
    episode_collector = EpisodeCollector()
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

    collect_button = tk.Button(
        frame,
        text="Collect Episodes",
        command=collect_episodes,
        foreground=PRIMARY_TEXT_COLOR,
        background=PRIMARY_COLOR,
        font=TEXT_FONT,
    )
    collect_button.grid(row=0, column=0, padx=PADDING, pady=PADDING, sticky="we")

    transforms_button = tk.Button(
        frame,
        text="Collect Transform",
        command=collect_transforms,
        foreground=PRIMARY_TEXT_COLOR,
        background=PRIMARY_COLOR,
        font=TEXT_FONT,
    )
    transforms_button.grid(row=0, column=1, padx=PADDING, pady=PADDING, sticky="we")

    slice_button = tk.Button(
        frame,
        text="Slice Episodes",
        command=slice_episodes,
        foreground=PRIMARY_TEXT_COLOR,
        background=PRIMARY_COLOR,
        font=TEXT_FONT,
    )
    slice_button.grid(row=1, column=0, padx=PADDING, pady=PADDING, sticky="we")

    square_button = tk.Button(
        frame,
        text="Square Episodes",
        command=square_episodes,
        foreground=PRIMARY_TEXT_COLOR,
        background=PRIMARY_COLOR,
        font=TEXT_FONT,
    )
    square_button.grid(row=1, column=1, padx=PADDING, pady=PADDING, sticky="we")

    warning_label = tk.Label(
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
        print(settings.getComicDir())
        os.startfile(settings.getComicDir())

    def create_exe():
        def run_thread():
            PyInstaller.__main__.run(
                [
                    "MasterControlProgram.py",
                    "--onefile",
                    "--icon=data/mcp.ico",
                    f"--name={PROGRAM_NAME} {VERSION}",
                ]
            )
            tk.messagebox.showinfo(title="Complete", message="Executable Created")
            enable_all()

        disable_all()
        thread = threading.Thread(target=run_thread, args=())
        thread.start()

    open_comic_button = tk.Button(
        frame,
        text="Open Comic Folder",
        command=open_comic_folder,
        background=PRIMARY_TEXT_COLOR,
        foreground=PRIMARY_COLOR,
        font=TEXT_FONT,
    )
    open_comic_button.grid(row=0, column=0, sticky="w", padx=PADDING, pady=PADDING)

    create_exe_button = tk.Button(
        frame,
        text="Create Executable",
        command=create_exe,
        background=PRIMARY_TEXT_COLOR,
        foreground=PRIMARY_COLOR,
        font=TEXT_FONT,
    )
    create_exe_button.grid(row=0, column=1, sticky="w", padx=PADDING, pady=PADDING)
    if not settings.in_debug_Mode or "\python.exe" not in sys.executable:
        create_exe_button.grid_remove()

    warning_label = tk.Label(
        frame,
        text="Creating Executable",
        foreground=WARNING_TEXT_COLOR,
        background=WARNING_COLOR,
        font=HEADER_FONT,
    )
    warning_label.grid(row=0, column=0, columnspan=3, sticky="ew")
    warning_label.grid_remove()


def setup_frame(root, row=0, column=0, sticky="new", color=CLEAR_COLOR):
    frame = tk.Frame(root, background=color)
    frame.grid(column=column, row=row, sticky=sticky)
    return frame


def execute_primary_function():
    # Create the main window
    root = App()
    i = 0

    # Menu
    m_frame = setup_frame(root, row=i, column=0, color=PRIMARY_TEXT_COLOR)
    menu_zone(m_frame, root)
    i += 1

    # Generate New Page
    gnp_frame = setup_frame(root, row=i, column=0, color=PRIMARY_COLOR)
    generate_page_zone(gnp_frame)
    i += 1

    # Collect Episodes
    ce_frame = setup_frame(root, row=i, column=0, color=CLEAR_COLOR)
    collect_episodes_zone(ce_frame)
    i += 1

    # File zone
    fz_frame = setup_frame(root, row=i, column=0, color=CLEAR_COLOR)
    file_zone(fz_frame)
    i += 1

    # execute the GUI
    root.mainloop()


if __name__ == "__main__":
    execute_primary_function()
