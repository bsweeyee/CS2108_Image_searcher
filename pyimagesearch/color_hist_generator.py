# import the necessary packages
from pyimagesearch.colordescriptor import ColorDescriptor
import argparse
import glob
import cv2
import os, sys
import utility.util as util


#the appended list of directories
all_image_paths = util.image_paths()

# initialize the color descriptor
cd = ColorDescriptor((8, 12, 3))

# open the output index file for writing
output = open("color_hist.csv", "w")

# use glob to grab the image paths and loop over them
for an_image_path in all_image_paths:
	for imagePath in glob.glob(an_image_path + "/*.jpg"):
		# extract the image ID (i.e. the unique filename) from the image
		# path and load the image itself
		imageID = imagePath[imagePath.rfind("/") + 1:]
		image = cv2.imread(imagePath)

		# describe the image
		features = cd.describe(image)

		# write the features to file
		features = [str(f) for f in features]
		output.write("%s,%s\n" % (imageID, ",".join(features)))

# close the index file
output.close()