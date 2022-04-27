import sys
import os
import argparse
from PIL import Image, ImageChops


parser = argparse.ArgumentParser(description = "Argument parser")
parser.add_argument("filepath", help = "location of the images to be de-watermarked")
parser.add_argument("-s", "--separate", action='store_true', help = "separate the stripped images into a new folder")

argument = parser.parse_args()



directoryToCheck = argument.filepath

if argument.separate:
    # Make the output directory if it doesn't already exist
    outputDir = os.path.join(directoryToCheck,'stripped')

    if not os.path.exists(outputDir):
        os.mkdir(outputDir)
else:
    outputDir = directoryToCheck



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

            new_image = os.path.join(outputDir, image_name)

            stripped_img.save(new_image)


    # Errors are generally from running into non-images in the folder to strip,
    #  so this just skips those items
    except:
        print(sys.exc_info()[0])
