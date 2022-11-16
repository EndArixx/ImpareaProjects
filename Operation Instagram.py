exec(compile(open('Collect Episodes.py', "rb").read(), 'Collect Episodes.py', 'exec'), globals, locals)
from PIL import Image
import os


def convert_to_Instagram(trim_image_Path):
	trim_image = Image.open(trim_image_Path)
	trim_image_width, trim_image_height = trim_image.size
	if trim_image_height > 4800:
		print('trimming:{}'.format(trim_image_Path.split('\\')[-1]))
		left = 0
		top = 1200
		right = trim_image_width
		bottom = trim_image_height
		trimmed_image = trim_image.crop((left, top, right, bottom))
		trimmed_image.save(trim_image_Path)

def crawl(files):
    globals.if_not_exist_make_folder('Insta')
    for image_path in files:
        convert_to_Instagram(image_path)

