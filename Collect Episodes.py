import os
import pathlib
import shutil
from glob import glob
from PIL import Image
from optparse import OptionParser
parser = OptionParser()
parser.add_option("-i", "--insta", action="store_true", dest="insta", default=False)
(options, args) = parser.parse_args()

file_type = '.png'
insta_folder_name = 'Insta'
uncensored_folder_name = '(U)'
parent_dir = pathlib.Path(__file__).parent.resolve()
pages_dir = os.path.abspath(os.path.join(parent_dir, '..\\Pages\\'))
pages_files = [y for x in os.walk(pages_dir) for y in glob(os.path.join(x[0], '*{}'.format(file_type)))]
remove_files = [y for x in os.walk(parent_dir) for y in glob(os.path.join(x[0], '*{}'.format(file_type)))]

class coordinate:
	def __init__(self,left, top, right, bottom):
		self.left = left
		self.top = top
		self.right = right
		self.bottom = bottom


Overrides = {
	#coordinate(left, top, right, bottom)
	"004P2": coordinate(0,1200,1600,2800),
	"004P3": coordinate(0,2200,1600,3800),
	"004P4": coordinate(0,3200,1600,4800),
	"007P1": coordinate(0,0,1600,1600),
	"007P2": coordinate(0,1000,1600,2600),
	"007P3": coordinate(0,2200,1600,3800),
	"007P4": coordinate(0,3200,1600,4800),
	"009P1": coordinate(0,0,1600,1600),
	"009P3": coordinate(0,2200,1600,3800),
	"009P4": coordinate(0,3200,1600,4800),
	"012P2": coordinate(0,1000,1600,2600),
	"012P3": coordinate(0,2200,1600,3800),
}

doubles = [
	"004P3",
	"007P3",
	"014P3",
	"036P1",
	"036P3",
	"041P1",
	"041P3",
	"046P1",
	"046P3",
	"051P3",
	"052P3",
]

#delete existing
for remove_path in remove_files:
	print('deleting:{}'.format(remove_path.split('\\')[-1]))
	if not remove_path.__contains__('\\'+insta_folder_name+'\\') or options.insta:
		os.remove(remove_path)

def if_not_exist_make_folder(path):
	if not os.path.exists(path):
		os.mkdir(path)

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
	if_not_exist_make_folder(uncensored_folder_name)
	for image_path in files:
		image_path_split = image_path.split('\\')
		image_dir = image_path_split[-2]
		image_name = image_path_split[-1]
		image_destination = 'ERROR'
		trim_headers(image_path)
		if "{}{}".format(image_dir,file_type) == image_name:
			print('copying:{}'.format(image_name))
			image_destination = os.path.join(parent_dir, image_name)
		elif "{}(U){}".format(image_dir,file_type) == image_name:
			print('copying:{} (Uncensored)'.format(image_name))
			image_destination = os.path.join(parent_dir, uncensored_folder_name, image_name )
		if image_destination != 'ERROR':
			shutil.copy(image_path,image_destination)

def Slice_for_Instagram(instafiles, recreate = False):
	if_not_exist_make_folder(insta_folder_name)
	for image_path in instafiles:
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
				name = f"{image_name[0:3]}P{i+1}"
				file = os.path.join(parent_dir, insta_folder_name, f"{name}.png")
				if name in doubles:
					s = name.split('.')
					doubleFile = os.path.join(parent_dir, insta_folder_name, f"{name}D.png")
					panel = image.crop((0,   i*y,  x, (i+2)*y))
					panel = panel.crop((-400,   0, x+400,2400))
					print(f'Saving DOUBLE:{doubleFile}')
					panel.save(doubleFile)
				if name in Overrides.keys():
					ex = Overrides[name]
					panel = image.crop((ex.left, ex.top, ex.right, ex.bottom))
					print(f'Saving CUSTOM:{file}')
					panel.save(file)
				elif not os.path.exists(file) or recreate:
					#crop(left, top, right, bottom)
					panel = image.crop((0,   i*y,  x, (i+1)*y))
					panel = panel.crop((0,   -gap, x, y+gap))
					print(f'Saving:{file}')
					panel.save(file)

def Slice_for_Instagram_V2(instafiles, recreate = False):
	if_not_exist_make_folder(insta_folder_name)
	for image_path in instafiles:
		image_path_split = image_path.split('\\')
		image_dir = image_path_split[-2]
		image_name = image_path_split[-1]
		image = Image.open(image_path)
		if "{}{}".format(image_dir,file_type) == image_name:
			x, height = image.size
			y = 2400
			gap = (x-y)/2
			panels = []
			for i in range(height//y):
				name = f"{image_name[0:3]}P{i+1}"
				file = os.path.join(parent_dir, insta_folder_name, f"{name}.png")
				if not os.path.exists(file) or recreate:
					panel = image.crop((0, i*y,  x, (i+2)*y))
					panel = panel.crop((-400, 0, x+400,2400))
					print(f'Saving:{file}')
					panel.save(file)

def Execute():
	copy_stuff(pages_files)
	if options.insta:
		Slice_for_Instagram_V2(pages_files)

if __name__=="__main__":
	Execute()