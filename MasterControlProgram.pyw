import sys
import tkinter as tk
from tkinter.filedialog import askdirectory
import threading
from CollectEpisodes import *
from GenerateNewPage import *
from ImpGenerator import *
from CompileCentral import *

'''
------------TODO:---------------
[x] Create exe/launch w/o console if not in debuggging.
[]  Add stdout/stderr to console.
'''

VERSION = "v0.2.6"
settings = tools.Settings()
imp_factory = ImpFactory(settings)

# Load Styles
PROGRAM_NAME = settings.get_program_name()
PRIMARY_TEXT_COLOR = settings.get_style_primarytextcolor()
PRIMARY_COLOR = settings.get_style_primarycolor()
SECONDARY_TEXT_COLOR = settings.get_style_secondarytextcolor()
SECONDARY_COLOR = settings.get_style_secondarycolor()
INPUT_COLOR = settings.get_style_inputcolor()
ACCENT_COLOR = settings.get_style_accentcolor()
WARNING_COLOR = settings.get_style_warningcolor()
WARNING_TEXT_COLOR = settings.get_style_warningtextcolor()
CLEAR_COLOR = settings.get_style_clearcolor()
HEADER_FONT = settings.get_style_headerfont()
TEXT_FONT = settings.get_style_textfont()
PADDING = settings.get_style_padding()


def get_zone_header(frame, title):
    return settings.label(
        frame,
        text=title,
        font=HEADER_FONT,
        foreground=SECONDARY_TEXT_COLOR,
        background=SECONDARY_COLOR,
    )


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

    zone_label = get_zone_header(frame, title="Generate New Page")
    zone_label.grid(
        row=0, column=0, columnspan=3, sticky="we", padx=PADDING, pady=PADDING
    )

    pagetitle_label = settings.label(
        frame,
        text="Page Title:",
    )
    pagetitle_label.grid(row=1, column=0, sticky="w", padx=PADDING, pady=PADDING)

    pagetitle_entry = settings.entry(
        frame,
        textvariable=pagetitle_var,
    )
    pagetitle_entry.grid(row=1, column=1, sticky="we", padx=PADDING, pady=PADDING)

    generatepage_button = settings.button(
        frame,
        text="Generate New Page",
        command=gen,
        state="disable",
        background=ACCENT_COLOR,
    )
    generatepage_button.grid(column=2, row=1, sticky="e", padx=PADDING, pady=PADDING)


def imp_management_zone(frame):
    frame.grid_columnconfigure(0, weight=1)

    zone_label = get_zone_header(frame, title="Imps")
    zone_label.grid(
        column=0,
        row=0,
        columnspan=2,
        sticky="we",
        padx=PADDING,
        pady=PADDING,
    )

    imp_factory.imp_management_zone(frame)


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

    zone_label = get_zone_header(frame, title="Episode Collectors")
    zone_label.grid(row=0, columnspan=2, padx=PADDING, pady=PADDING, sticky="we")

    collect_button = settings.button(
        frame,
        text="Collect Episodes",
        command=collect_episodes,
    )
    collect_button.grid(row=1, column=0, padx=PADDING, pady=PADDING, sticky="we")

    transforms_button = settings.button(
        frame,
        text="Collect Transform",
        command=collect_transforms,
    )
    transforms_button.grid(row=1, column=1, padx=PADDING, pady=PADDING, sticky="we")

    slice_button = settings.button(
        frame,
        text="Slice Episodes",
        command=slice_episodes,
    )
    slice_button.grid(row=2, column=0, padx=PADDING, pady=PADDING, sticky="we")

    square_button = settings.button(
        frame,
        text="Square Episodes",
        command=square_episodes,
    )
    square_button.grid(row=2, column=1, padx=PADDING, pady=PADDING, sticky="we")

    warning_label = settings.label(
        frame,
        text="Executing Collection",
        foreground=WARNING_TEXT_COLOR,
        background=WARNING_COLOR,
        font=HEADER_FONT,
    )
    warning_label.grid(row=1, column=0, rowspan=2, columnspan=2, sticky="ew")
    warning_label.grid_remove()


def file_zone(frame):
    frame.grid_rowconfigure(0, weight=0)
    for i in range(4):
        frame.grid_columnconfigure(index=i, weight=1)
    hasExeButt = not getattr(sys, "frozen", False) and settings.in_debug_Mode

    def disable_all():
        warning_label.grid()
        open_comic_button["state"] = "disable"
        compile_pdf_button["state"] = "disable"
        if hasExeButt: create_exe_button["state"] = "disable"

    def enable_all():
        warning_label.grid_remove()
        open_comic_button["state"] = "normal"
        compile_pdf_button["state"] = "normal"
        if hasExeButt: create_exe_button["state"] = "normal"

    compile_central = CompileCentral(disable_all, enable_all, settings)

    def open_comic_folder():
        print(settings.get_comic_dir())
        os.startfile(settings.get_comic_dir())

    png_folder = f"{settings.get_comic_dir()}\\PNGs\\"
    pdf_folder = f"{settings.get_comic_dir()}\\PDFs\\"

    def compile_comic_to_pdf():
        source = png_folder
        dest = f"{pdf_folder}{settings.get_comic_name()}.pdf"
        compile_central.compile_to_pdf(source, dest)

    def compile_folder_to_pdf():
        source = askdirectory(title="Select Source Folder",initialdir=png_folder)
        if not source:
            return
        destination = asksaveasfilename(title="PDF Name",initialdir=pdf_folder, filetypes=[("PDF files", f"*.pdf")])
        compile_central.compile_to_pdf(source, destination)     

    def compile_folder_to_avi():
        source = askdirectory(title="Select Image Folder")
        if not source:
            return
        destination = asksaveasfilename(title="Video File Name", filetypes=[("Video Files", f"*.avi")])
        compile_central.compile_to_video(source, destination)

    def compile_folder_to_gif():
        source = askdirectory(title="Select Image Folder")
        if not source:
            return
        destination = asksaveasfilename(title="Jiff File Name", filetypes=[("Gif", f"*.gif")])
        compile_central.compile_to_gif(source, destination)

    zone_label = get_zone_header(frame, title="File Operations")
    zone_label.grid(row=0, column=0, columnspan=4, padx=PADDING, pady=PADDING, sticky="we")

    open_comic_button = settings.button(
        frame,
        text="Open Comic Folder",
        command=open_comic_folder,
        width=1,
    )
    open_comic_button.grid(row=1, column=0, sticky="ew", padx=PADDING, pady=PADDING)

    if hasExeButt:
        create_exe_button = settings.button(
            frame,
            text="Create Executable",
            command=compile_central.create_exe,
            width=1,
        )
        create_exe_button.grid(row=1, column=1, sticky="ew", padx=PADDING, pady=PADDING)
    
    compile_comic_button = settings.button(
        frame,
        text=f"Create: {settings.get_comic_name()}.pdf",
        command=compile_comic_to_pdf,
        width=1
    )
    compile_comic_button.grid(row=1, column=2, sticky="ew", padx=PADDING, pady=PADDING) 
    
    compile_pdf_button = settings.button(
        frame,
        text="Create .pdf from Folder",
        command=compile_folder_to_pdf,
        width=1,
    )
    compile_pdf_button.grid(row=1, column=3, sticky="ew", padx=PADDING, pady=PADDING) 

    compile_video_button = settings.button(
        frame,
        text="Create .avi from Folder",
        command=compile_folder_to_avi,
        width=1,
    )
    compile_video_button.grid(row=2, column=0, sticky="ew", padx=PADDING, pady=PADDING) 

    compile_gif_button = settings.button(
        frame,
        text="Create .gif from Folder",
        command=compile_folder_to_gif,
        width=1,
    )
    compile_gif_button.grid(row=2, column=1, sticky="ew", padx=PADDING, pady=PADDING) 


    warning_label = settings.label(
        frame,
        text="⌛ In Progress ⏳",
        foreground=WARNING_TEXT_COLOR,
        background=WARNING_COLOR,
        font=HEADER_FONT,
    )
    warning_label.grid(row=1, column=0, columnspan=4, rowspan=2, sticky="ew")
    warning_label.grid_remove()


def execute_primary_function():

    # Create the main window
    root = tools.ImparianApp(
        f"{settings.get_program_name()} - {VERSION}",
        settings,
        has_settings_edit=True,
        has_debug_log=True,
        close_warnings=[imp_factory],
        minwidth=975,
    )

    # Generate New Page
    gnp_frame = root.add_frame(background=PRIMARY_COLOR)
    generate_page_zone(gnp_frame)

    # Imp Management
    imp_management_frame = root.add_frame(background=PRIMARY_COLOR)
    imp_management_zone(imp_management_frame)

    # Collect Episodes
    ce_frame = root.add_frame(background=CLEAR_COLOR)
    collect_episodes_zone(ce_frame)

    # File zone
    fz_frame = root.add_frame(background=CLEAR_COLOR)
    file_zone(fz_frame)

    # execute the GUI
    root.mainloop()


if __name__ == "__main__":
    execute_primary_function()
