import os, sys
import classify_image
import csv
import numpy as np
import tensorflow as tf

# A bunch of functions that manipulates csv vector files
# and images in database

# returns a list of image category folder paths from "database" folder
# eg. '...something.../database/alley'

def get_image_paths():
	i = 1
	file_path =  os.listdir(os.getcwd())[0]
	while file_path != "database":
		file_path =  os.listdir(os.getcwd())[i]
		i += 1

	data_path = os.path.join(os.getcwd(), file_path)
	image_paths = []

	for i in xrange(len(os.listdir(data_path))):
		image_paths.append(os.path.join(data_path, os.listdir(data_path)[i]))

	if (image_paths[0] == STUPID_DS_STORE):
		image_paths = image_paths[1::]
	
	return image_paths

# returns a list of full individual image directory path 
# from all the image category folders
# eg. '...something.../database/alley/0028_1070815604.jpg'

def get_jpg_paths():
	image_paths_array = get_image_paths()
	jpg_paths = []
	
	for i in xrange(len(image_paths_array)):
		a_image_path = os.listdir(image_paths_array[i])
		for j in xrange(len(a_image_path)):
			jpg_paths.append(os.path.join(image_paths_array[i], a_image_path[j]))

	return jpg_paths

# returns a list of image name + extension from each image
# eg. '0028_1070815604.jpg'

def get_image_ids():
	image_ids = []

	image_paths = get_image_paths()
	for i in xrange(len(image_paths)):
		a_image_path = os.listdir(image_paths[i])
		for j in xrange(len(a_image_path)):
			image_ids.append(a_image_path[j])

	return image_ids

# returns a list of image categories from the database
# eg. 'alley'

def get_image_groups():
	image_paths = get_image_paths()
	image_group = []
	for image in image_paths:
		image_group.append(os.path.basename(image))

	return image_group

#print get_image_paths()
#output_vectors()
#print "Done!"
		