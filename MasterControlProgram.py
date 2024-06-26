import tkinter as tk
from CollectEpisodes import *
import GenerateNewPage as gnp
import threading

TEXT_COLOR = "black"
PRIMARY_COLOR = "MediumSpringGreen"
ACCENT_COLOR = "plum"
WARNING_COLOR = "crimson"
WARNING_TEXT_COLOR = "white"
CLEAR_COLOR = "snow"


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.wm_attributes("-transparentcolor", CLEAR_COLOR)
        self.title("Imparea Comic Utilities")
        self.configure(background=CLEAR_COLOR)
        self.minsize(500, 0)
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
        text="Imparia Solutions!",
        foreground=PRIMARY_COLOR,
        background=TEXT_COLOR,
    )
    label.bind("<Button-1>", root.startMove)
    label.bind("<ButtonRelease-1>", root.stopMove)
    label.bind("<B1-Motion>", root.moving)
    label.grid(column=0, row=0, columnspan=2, sticky="ew", padx=5, pady=5)

    exit_button = tk.Button(
        frame,
        text="✕",
        command=root.destroy,
        background=TEXT_COLOR,
        foreground=PRIMARY_COLOR,
    )
    exit_button.grid(row=0, column=1, sticky="e", padx=5, pady=5)


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

    zone_label = tk.Label(frame, text="Generate New Page", background=PRIMARY_COLOR)
    zone_label.grid(column=0, row=0, columnspan=3, sticky="we", padx=5, pady=5)

    pagetitle_label = tk.Label(frame, text="Page Title:", background=PRIMARY_COLOR)
    pagetitle_label.grid(column=0, row=1, sticky="w", padx=5, pady=5)

    pagetitle_entry = tk.Entry(frame, textvariable=pagetitle_var)
    pagetitle_entry.grid(column=1, row=1, sticky="we", padx=5, pady=5)

    generatepage_button = tk.Button(
        frame,
        text="Generate new Page",
        command=gen,
        state="disable",
        background=ACCENT_COLOR,
    )
    generatepage_button.grid(column=2, row=1, sticky="e", padx=5, pady=5)


def collect_episodes_zone(frame):
    episode_collector = EpisodeCollector()
    for i in range(4):
        frame.grid_columnconfigure(i, weight=1)

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
        collect_button.grid_remove()
        slice_button["state"] = "disable"
        slice_button.grid_remove()
        square_button["state"] = "disable"
        square_button.grid_remove()
        transforms_button["state"] = "disable"
        transforms_button.grid_remove()

    def enable_all():
        warning_label.grid_remove()
        collect_button["state"] = "normal"
        collect_button.grid()
        slice_button["state"] = "normal"
        slice_button.grid()
        square_button["state"] = "normal"
        square_button.grid()
        transforms_button["state"] = "normal"
        transforms_button.grid()

    collect_button = tk.Button(
        frame,
        text="Collect Episodes",
        command=collect_episodes,
        background=ACCENT_COLOR,
    )
    collect_button.grid(row=0, column=0, padx=5, pady=5, sticky="we")

    slice_button = tk.Button(
        frame, text="Slice Episodes", command=slice_episodes, background=ACCENT_COLOR
    )
    slice_button.grid(row=0, column=1, padx=5, pady=5, sticky="we")

    square_button = tk.Button(
        frame, text="Square Episodes", command=square_episodes, background=ACCENT_COLOR
    )
    square_button.grid(row=0, column=2, padx=5, pady=5, sticky="we")

    transforms_button = tk.Button(
        frame,
        text="Collect Transform",
        command=collect_transforms,
        background=ACCENT_COLOR,
    )
    transforms_button.grid(row=0, column=3, padx=5, pady=5, sticky="we")

    warning_label = tk.Label(
        frame,
        text="Warning: Collection currently running.",
        foreground=WARNING_TEXT_COLOR,
        background=WARNING_COLOR,
        font="Helvetica 16 bold",
    )
    warning_label.grid(row=1, column=0, columnspan=4, sticky="ew")
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
    m_frame = setup_frame(root, row=i, column=0, color=TEXT_COLOR)
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

    root.mainloop()


if __name__ == "__main__":
    execute_primary_function()
