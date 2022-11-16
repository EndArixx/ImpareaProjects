import tkinter as tk
from tkinter import simpledialog
import os
import pathlib
import shutil

ROOT = tk.Tk()
ROOT.withdraw()

page_title = simpledialog.askstring(title="Page Name?", prompt="Page Name?")
if page_title is not None and len(page_title.strip()) > 0:
	parent_dir = pathlib.Path(__file__).parent.resolve()
	page_number = len(next(os.walk(parent_dir))[1]) + 1
	page_name = '{:03d} {}'.format(page_number,page_title.strip())
	page_path = os.path.join(parent_dir, page_name)
	page_file_name = os.path.join(page_path, '{}.oci'.format(page_name))
	page_template_path = os.path.abspath(os.path.join(parent_dir, '..\Resources\Templates\webstyle.oci'))

	#Create and copy
	os.makedirs(page_path, exist_ok = True)
	shutil.copy(page_template_path,page_file_name)