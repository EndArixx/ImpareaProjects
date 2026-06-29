# Importing libraries
from io import BytesIO
import os
import threading
from tkinter.filedialog import askdirectory, asksaveasfilename
import cv2
from PIL import Image
import utilities.tools as tools
import tkinter as tk
import PyInstaller.__main__


vid_formats = {
    ".avi": "DIVX",
    ".mp4": "MP4V",
}


class CompileCentral():
    def __init__(self, lock_start, lock_end, settings= None):
        if settings == None:
            settings = tools.Settings()
        self.settings = settings
        self.lock_start = lock_start
        self.lock_end = lock_end
    def compile_to_video(self, source, destination, type =".avi"):
    
        if not source or not destination or type not in vid_formats:
            self.lock_end()
            self.settings.print_debug("compile_to_video cancelled")
            return

        def run_thread(src, dest):
            images = [img for img in os.listdir(src) if img.endswith((".jpg", ".jpeg", ".png"))]
            if os.path.splitext(dest)[1] != type:
                    dest = dest + type
            self.settings.print_debug(f"Images:{images}")

            first = os.path.join(src, images[0])
            # Set frame from the first image
            frame = cv2.imread(first)
            height, width, layers = frame.shape

            # Video writer to create .avi file
            video = cv2.VideoWriter(dest, cv2.VideoWriter_fourcc(*vid_formats[type]), 30, (width, height))

            # Appending images to video
            for img in images:
                video.write(cv2.imread(os.path.join(src, img)))

            # Release the video file
            video.release()
            cv2.destroyAllWindows()
            self.settings.print_debug(f"{dest} created Successfully.")
            self.lock_end()
            os.startfile(dest)
        
        self.lock_start()
        thread = threading.Thread(target=lambda: run_thread(source, destination))
        thread.start()

        
    def compile_to_gif(self, source, destination):
        if(not source or not destination):
            self.lock_end()
            self.settings.print_debug("compile_to_gif cancelled")
            return
        self.settings.print_debug(f"Compiling {source} into {destination}")

        def run_thread(src, dest):
            # Create the frames
            frames = []
            images = [img for img in os.listdir(src) if img.endswith((".jpg", ".jpeg", ".png"))]
            if os.path.splitext(dest)[1] != ".gif":
                    dest = dest + ".gif"
            self.settings.print_debug(f"Images:{images}")

            for i in images:
                new_frame = Image.open(os.path.join(src, i))
                frames.append(new_frame)

            # Save into a GIF file that loops forever
            frames[0].save(dest, format='GIF',
                append_images=frames[1:],
                save_all=True,
                duration=30, loop=0)
            
            self.lock_end()
            self.settings.print_debug(f"{dest} created Successfully.")
            os.startfile(dest)

        self.lock_start()
        thread = threading.Thread(target=lambda: run_thread(source, destination))
        thread.start()

    def compile_to_pdf(self, source, destination):
        if(not source or not destination):
            self.lock_end()
            self.settings.print_debug("compile_to_pdf cancelled")
            return
        self.settings.print_debug(f"Compiling {source} into {destination}")
        
        def run_thread(src, dest):
            imgs = []
            if os.path.splitext(dest)[1] != ".pdf":
                    dest = dest + ".pdf"

            valid_images = [".jpg",".gif",".png",".tga", ".jpeg", ".bmp"]
            for f in os.listdir(src):
                ext = os.path.splitext(f)[1]
                if ext.lower() not in valid_images:
                    continue
                img = Image.open(os.path.join(src, f)).convert("RGB")
                with BytesIO() as f:
                    img.save(f, format='JPEG')
                    f.seek(0)
                    ima_jpg = Image.open(f)
                    ima_jpg.load()

                imgs.append(ima_jpg)

            imgs[0].save(dest, "PDF" ,resolution=100.0, save_all=True, append_images=imgs[1:])
            self.lock_end()
            self.settings.print_debug(f"{dest} created Successfully.")
            os.startfile(dest)

        self.lock_start()
        thread = threading.Thread(target=lambda: run_thread(source, destination))
        thread.start()

    def create_exe(self):
        def run_thread():
            PyInstaller.__main__.run(
                [
                    "MasterControlProgram.pyw",
                    "--onefile",
                    "--icon=data/mcp.ico",
                    f"--name={self.settings.get_program_name()}",
                    "--add-data=data/:data",
                ]
            )
            tk.messagebox.showinfo(title="Complete", message="Executable Created")
            self.lock_end()

        self.lock_start()
        thread = threading.Thread(target=run_thread, args=())
        thread.start()


if __name__ == "__main__":
    settings = tools.Settings()
    
    def start():
        settings.print_debug("Start")
    def end():
        settings.print_debug("End")

    compile_central = CompileCentral(start, end, settings)


    source = askdirectory(title="Select Image Folder")
    if source:
        destination = asksaveasfilename(title="Video File Name", filetypes=[("Video Files", f"*.avi")])
        compile_central.compile_to_video(source, destination)