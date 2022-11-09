import os
import pathlib
import shutil
from glob import glob
from PIL import Image

file_type = '.png'
parent_dir = pathlib.Path(__file__).parent.resolve()
pages_dir = os.path.abspath(os.path.join(parent_dir, '..\\Pages\\'))
pages_files = [y for x in os.walk(pages_dir) for y in glob(os.path.join(x[0], '*{}'.format(file_type)))]
remove_files = [y for x in os.walk(parent_dir) for y in glob(os.path.join(x[0], '*{}'.format(file_type)))]

#delete existing
for remove_path in remove_files:
	print('deleting:{}'.format(remove_path.split('\\')[-1]))
	os.remove(remove_path)

def trim_headers(trim_image_Path):
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

#copy over files
def copy_stuff(files):
	for image_path in files:
		image_path_split = image_path.split('\\')
		image_dir = image_path_split[-2]
		image_name = image_path_split[-1]
		image_destination = 'ERROR'
		if "{}{}".format(image_dir,file_type) == image_name:
			print('copying:{}'.format(image_name))
			image_destination = os.path.join(parent_dir, image_name)
		elif "{}(U){}".format(image_dir,file_type) == image_name:
			print('copying:{} (Uncensored)'.format(image_name))
			image_destination = os.path.join(parent_dir, '(U)', image_name )
		if image_destination is not 'ERROR':
			shutil.copy(image_path,image_destination)
			trim_headers(image_destination)
	

			
copy_stuff(pages_files)