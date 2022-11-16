import os
import pathlib
from glob import glob
from PIL import Image


file_type = '.png'
folder_name = 'Insta'
parent_dir = pathlib.Path(__file__).parent.resolve()
pages_dir = os.path.abspath(os.path.join(parent_dir, '..\\Pages\\'))
files = [y for x in os.walk(pages_dir) for y in glob(os.path.join(x[0], '*{}'.format(file_type)))]

if not os.path.exists(folder_name):os.mkdir(folder_name)

for image_path in files:
	image_path_split = image_path.split('\\')
	image_dir = image_path_split[-2]
	image_name = image_path_split[-1]
	image = Image.open(image_path)
	if "{}{}".format(image_dir,file_type) == image_name:
		x, height = image.size
		y = 1200
		gap = (x-y)/2
		panels = []
		for i in range(height//y):
			file = os.path.join(parent_dir, folder_name, "{0}P{1}.png".format(image_name[0:3], i+1))
						 #crop((left, top, right, bottom))
			panel = image.crop((0,   i*y,  x, (i+1)*y))
			panel = panel.crop((0,   -gap, x, y+gap))
			print('Saving:{}'.format(file))
			panel.save(file)