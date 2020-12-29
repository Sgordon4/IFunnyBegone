import sys
import os
from PIL import Image, ImageChops



directoryToCheck = sys.argv[1]


# Make the output directory if not exists
cwd = os.getcwd()
strippedDir = os.path.join(cwd,'stripped')
if not os.path.exists(strippedDir):
    os.mkdir(strippedDir)
	

watermarkName = "watermark.jpg"
watermark = Image.open(watermarkName)
width, height = watermark.size
watermark = watermark.crop((width-136, height-20, width, height))


# Iterate through the names of contents of the folder
for image_name in os.listdir(directoryToCheck):
	try:
		# Create the full input path and read the file
		image_path = os.path.join(directoryToCheck, image_name)
		image = Image.open(image_path)
		width, height = image.size
		image = image.crop((width-136, height-20, width, height))
		
		# Calculate how similar the two images are
		diff = ImageChops.difference(watermark, image)
		average = sum( diff.resize((1, 1)).getpixel((0, 0)) )
		
		
		if(average < 40):
			image = Image.open(image_path)
			stripped_img = image.crop((0, 0, width, height-20))
			new_image = os.path.join(strippedDir, image_name)
			stripped_img.save(new_image)
			
	except:
		print(sys.exc_info()[0])